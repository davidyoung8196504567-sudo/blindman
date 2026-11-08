"""The split is checked against the thesis's own row totals, independent of any network."""

import collections
import json
import subprocess
import sys
from pathlib import Path

from blindman.repro1995 import data
from blindman.repro1995.experiments import targets

ROOT = data.default_data_root()


def test_target_file_is_regenerated_exactly_from_the_thesis():
    tool = Path(__file__).resolve().parents[1] / "tools" / "extract_chapter6.py"
    out = subprocess.run([sys.executable, "-I", str(tool)], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout) == targets()


def test_eleven_speakers_recorded_on_both_channels():
    for ch in data.CHANNELS:
        assert len(data.SPEAKERS) == 11
        for s in data.SPEAKERS:
            assert len(data.load_speaker(ROOT, ch, s)) >= 40


def _test_counts(channel):
    count = collections.Counter()
    for s in data.SPEAKERS:
        _, test = data.split_speaker_dependent(data.load_speaker(ROOT, channel, s), data.n_sessions(ROOT, s))
        count.update(x.phrase for x in test)
    return [count[p] for p in data.PHRASES]


def test_speaker_dependent_split_reproduces_the_thesis_row_totals():
    thesis = [sum(row) for row in targets()["tables"]["6.5-M"]["confusion"]]
    assert thesis == [77, 77, 77, 77, 79, 79, 79, 79]
    assert _test_counts("microphone") == thesis


def test_telephone_split_loses_only_the_missing_files():
    # DY's 1104 session (in the test half) and MO's 1123 phrase 6 have no telephone copy.
    assert _test_counts("telephone") == [76, 76, 76, 76, 77, 78, 78, 78]


def test_speaker_independent_selection_is_five_tokens_per_phrase():
    for ch in data.CHANNELS:
        for s in data.SPEAKERS:
            chosen = data.select_speaker_independent(data.load_speaker(ROOT, ch, s))
            assert collections.Counter(x.phrase for x in chosen) == {p: 5 for p in data.PHRASES}


def test_telephone_sessions_pair_with_microphone_sessions():
    dh_tel = data.load_speaker(ROOT, "telephone", "DH")
    assert {x.session for x in dh_tel if x.date == "0919"} == {0}  # the microphone copy is dated 0927
    dy_tel = data.load_speaker(ROOT, "telephone", "DY")
    dy_mic = data.load_speaker(ROOT, "microphone", "DY")
    missing = {x.session for x in dy_mic} - {x.session for x in dy_tel}
    assert {x.date for x in dy_mic if x.session in missing} == {"1104"}
