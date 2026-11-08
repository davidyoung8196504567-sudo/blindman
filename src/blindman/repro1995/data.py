"""Load the RMC Speech Database formant files and build the Chapter 6 splits.

File names follow Figure 5.1: ``F<initials><MMDD><phrase>.MAT``. Sorting a
speaker's files by name therefore sorts them chronologically, and by phrase
within a session.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.io import loadmat

PHRASES = tuple(range(2, 10))
CHANNELS = ("microphone", "telephone")

# §6.2.1: only speakers with at least 40 samples, and the same sets in all
# tests. DB has 40 microphone samples but no telephone recordings, so the
# eleven speakers are the ones recorded on both channels.
SPEAKERS = ("AH", "BT", "DG", "DH", "DY", "IH", "JD", "LP", "LR", "MJ", "MO")

_NAME = re.compile(r"^F([A-Z]{2})(\d{4})(\d)\.MAT$", re.IGNORECASE)


def default_data_root() -> Path:
    return Path(__file__).resolve().parents[3] / "thesis-1995" / "data"


@dataclass(frozen=True)
class Sample:
    speaker: str
    date: str  # MMDD, 1994
    phrase: int
    session: int  # 0-based index of the speaker's recording session
    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    def formants(self) -> np.ndarray:
        """The 3 x N formant tracks in Hz (rows F1, F2, F3)."""
        return np.asarray(loadmat(self.path)["Formant"], dtype=float)


def _list(root: Path, channel: str, speaker: str) -> list[tuple[str, int, Path]]:
    files = sorted((root / channel / speaker).glob("*.[Mm][Aa][Tt]"), key=lambda p: p.name.upper())
    out = []
    for path in files:
        m = _NAME.match(path.name)
        if not m or m.group(1).upper() != speaker:
            raise ValueError(f"unexpected file name {path}")
        if int(m.group(3)) in PHRASES:
            out.append((m.group(2), int(m.group(3)), path))
    return out


def _sessions(files: list[tuple[str, int, Path]]) -> list[list[tuple[str, int, Path]]]:
    """Group files by recording date. A date holding only phrases missing from
    the previous date, one day earlier, is the same session (MJ 1107/1108)."""
    groups: list[list[tuple[str, int, Path]]] = []
    for f in files:
        if groups and groups[-1][-1][0] == f[0]:
            groups[-1].append(f)
            continue
        if groups:
            prev = groups[-1]
            prev_phrases = {p for _, p, _ in prev}
            same_day_after = int(f[0]) - int(prev[-1][0]) == 1
            if same_day_after and len(prev) < len(PHRASES) and f[1] not in prev_phrases:
                prev.append(f)
                continue
        groups.append([f])
    for g in groups:
        g.sort(key=lambda f: f[1])
    return groups


def load_speaker(root: Path, channel: str, speaker: str) -> list[Sample]:
    """A speaker's samples in recording order, numbered by microphone session.

    §6.2.1 uses the same training and test sets in all tests, so sessions are
    numbered on the microphone schedule for both channels. A telephone session
    is paired with the microphone session of the same date or, failing that,
    with the next unpaired one in order: some telephone sessions carry a
    different date (DH 0919/0927, DG 1109/1108), and DY's 1104 session has no
    telephone copy.
    """
    mic = _sessions(_list(root, "microphone", speaker))
    own = mic if channel == "microphone" else _sessions(_list(root, channel, speaker))
    index: dict[int, int] = {}
    if own is mic:
        index = {i: i for i in range(len(mic))}
    else:
        mic_dates = [{d for d, _, _ in g} for g in mic]
        for i, g in enumerate(own):
            dates = {d for d, _, _ in g}
            hit = [j for j, md in enumerate(mic_dates) if md & dates]
            if hit:
                index[i] = hit[0]
        free = [j for j in range(len(mic)) if j not in index.values()]
        for i in range(len(own)):
            if i not in index:
                before = max((index[k] for k in index if k < i), default=-1)
                after = min((index[k] for k in index if k > i), default=len(mic))
                cand = [j for j in free if before < j < after]
                if not cand:
                    raise ValueError(f"cannot pair {channel} session {own[i][0][0]} of {speaker}")
                index[i] = cand[0]
                free.remove(cand[0])
    return [Sample(speaker, d, p, index[i], path)
            for i, g in enumerate(own) for d, p, path in g]


def n_sessions(root: Path, speaker: str) -> int:
    return len(_sessions(_list(root, "microphone", speaker)))


def split_speaker_dependent(samples: list[Sample], sessions: int) -> tuple[list[Sample], list[Sample]]:
    """§6.2.2: the first half of a speaker's samples train, the second half test.

    The half is taken on the recording schedule (sessions x 8 phrases), so a
    speaker with an odd number of sessions is split mid-session: phrases 2-5
    of the middle session train and phrases 6-9 test.
    """
    cut = sessions * len(PHRASES) / 2
    train = [s for s in samples if s.session * len(PHRASES) + (s.phrase - 2) < cut]
    test = [s for s in samples if s.session * len(PHRASES) + (s.phrase - 2) >= cut]
    return train, test


def select_speaker_independent(samples: list[Sample], tokens: int = 5) -> list[Sample]:
    """§6.2.2: five tokens of each of the eight phrases per speaker, the
    earliest recorded (§6.2.1 chooses sets chronologically)."""
    chosen: list[Sample] = []
    for phrase in PHRASES:
        chosen += [s for s in samples if s.phrase == phrase][:tokens]
    return sorted(chosen, key=lambda s: (s.session, s.phrase))
