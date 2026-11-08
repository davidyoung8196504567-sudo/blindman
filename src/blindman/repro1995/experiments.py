"""Run the ten Chapter 6 test sessions, plus the TFRV benchmark §6.2.2 left undone."""

from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import numpy as np

from . import data
from .backprop import Backprop
from .features import REPRESENTATIONS
from .fuzzy_artmap import UNRECOGNIZED, FuzzyARTMAP

PHRASES = data.PHRASES


@dataclass(frozen=True)
class Test:
    table: str  # thesis table id, or "new-..." for tests the thesis did not run
    recognizer: str  # fuzzy_artmap | backprop
    representation: str  # TFRV | BFRV
    protocol: str  # SD | SI
    channel: str  # microphone | telephone


TESTS = [
    Test("6.1", "backprop", "BFRV", "SD", "microphone"),
    Test("6.2", "backprop", "BFRV", "SI", "microphone"),
    Test("6.3-M", "fuzzy_artmap", "BFRV", "SD", "microphone"),
    Test("6.3-T", "fuzzy_artmap", "BFRV", "SD", "telephone"),
    Test("6.4-M", "fuzzy_artmap", "BFRV", "SI", "microphone"),
    Test("6.4-T", "fuzzy_artmap", "BFRV", "SI", "telephone"),
    Test("6.5-M", "fuzzy_artmap", "TFRV", "SD", "microphone"),
    Test("6.5-T", "fuzzy_artmap", "TFRV", "SD", "telephone"),
    Test("6.6-M", "fuzzy_artmap", "TFRV", "SI", "microphone"),
    Test("6.6-T", "fuzzy_artmap", "TFRV", "SI", "telephone"),
    Test("new-TFRV-SD", "backprop", "TFRV", "SD", "microphone"),
    Test("new-TFRV-SI", "backprop", "TFRV", "SI", "microphone"),
]


def targets() -> dict:
    return json.loads(resources.files(__package__).joinpath("chapter6_targets.json").read_text())


class _Features:
    """Load each formant file once, and each representation once."""

    def __init__(self):
        self._cache: dict = {}

    def __call__(self, sample: data.Sample, representation: str) -> np.ndarray:
        key = (sample.path, representation)
        if key not in self._cache:
            self._cache[key] = REPRESENTATIONS[representation](sample.formants())
        return self._cache[key]


def _folds(test: Test, root: Path):
    """Yield (train samples, test samples) for each network the protocol trains."""
    speakers = {s: data.load_speaker(root, test.channel, s) for s in data.SPEAKERS}
    if test.protocol == "SD":
        for s in data.SPEAKERS:
            yield data.split_speaker_dependent(speakers[s], data.n_sessions(root, s))
    else:
        chosen = {s: data.select_speaker_independent(speakers[s]) for s in data.SPEAKERS}
        for held_out in data.SPEAKERS:
            train = [x for s in data.SPEAKERS if s != held_out for x in chosen[s]]
            yield train, chosen[held_out]


def run(test: Test, root: Path | None = None, features: _Features | None = None,
        seed: int = 1995) -> dict:
    root = root or data.default_data_root()
    features = features or _Features()
    confusion = np.zeros((len(PHRASES), len(PHRASES)), dtype=int)
    unrecognized = [0] * len(PHRASES)
    n_train = 0
    for train, test_set in _folds(test, root):
        n_train += len(train)
        net = FuzzyARTMAP(len(features(train[0], test.representation)))
        for s in train:
            net.train(features(s, test.representation), s.phrase)
        model = net
        if test.recognizer == "backprop":
            model = Backprop(PHRASES, seed=seed).fit_from_artmap(net)
        for s in test_set:
            out = model.predict(features(s, test.representation))
            label = out[0] if isinstance(out, tuple) else out
            if label is UNRECOGNIZED:
                unrecognized[PHRASES.index(s.phrase)] += 1
            else:
                confusion[PHRASES.index(s.phrase), PHRASES.index(label)] += 1
    correct = int(np.trace(confusion))
    total = int(confusion.sum()) + sum(unrecognized)
    return {"table": test.table, "recognizer": test.recognizer,
            "representation": test.representation, "protocol": test.protocol,
            "channel": test.channel, "correct": correct, "total": total,
            "rate": round(100 * correct / total, 1), "unrecognized": sum(unrecognized),
            "train_samples": n_train, "confusion": confusion.tolist()}


def run_all(root: Path | None = None, seed: int = 1995) -> list[dict]:
    features = _Features()
    return [run(t, root, features, seed) for t in TESTS]
