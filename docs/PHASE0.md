# Phase 0: the 1995 results, reproduced

**Status: done, 2026-11-08.** The 1995 recognizer is ported to Python
([`src/blindman/repro1995/`](../src/blindman/repro1995/)) and rerun on the recovered
formant files. **Every Fuzzy ARTMAP recognition rate reproduces exactly** where the data
survived complete, and four of those six tables match cell for cell. Every difference is
written up below; one is still unexplained. No parameter was tuned.
The components and their inputs and outputs are drawn in [COMPONENTS.md](COMPONENTS.md).

Run it:

```
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/python -m blindman.repro1995      # the table below, in about 15 seconds
.venv/bin/python -m pytest                  # including the score gate
```

## Results

| Table | Recognizer | Features | Test | Channel | Thesis | Port | Match |
|---|---|---|---|---|---|---|---|
| 6.3-M | Fuzzy ARTMAP | BFRV | speaker-dependent | microphone | 606/624 97.1% | 606/624 97.1% | Same total; 2 cells differ ([note 3](#3-two-phrase-7-files-open)) |
| 6.4-M | Fuzzy ARTMAP | BFRV | speaker-independent | microphone | 413/440 93.9% ([note 1](#1-two-arithmetic-slips-in-the-thesis)) | 413/440 93.9% | **Every cell** |
| 6.5-M | Fuzzy ARTMAP | TFRV | speaker-dependent | microphone | 613/624 98.2% | 613/624 98.2% | Same total; 2 cells differ ([note 3](#3-two-phrase-7-files-open)) |
| 6.6-M | Fuzzy ARTMAP | TFRV | speaker-independent | microphone | 414/440 94.1% | 414/440 94.1% | **Every cell** |
| 6.3-T | Fuzzy ARTMAP | BFRV | speaker-dependent | telephone | 549/624 88.0% | 547/615 88.9% | 9 test files lost ([note 4](#4-telephone-nine-test-files-did-not-survive)) |
| 6.4-T | Fuzzy ARTMAP | BFRV | speaker-independent | telephone | 375/440 85.2% | 375/440 85.2% | **Every cell** |
| 6.5-T | Fuzzy ARTMAP | TFRV | speaker-dependent | telephone | 571/624 91.5% | 560/615 91.1% | 9 test files lost ([note 4](#4-telephone-nine-test-files-did-not-survive)) |
| 6.6-T | Fuzzy ARTMAP | TFRV | speaker-independent | telephone | 383/440 87.0% | 383/440 87.0% | **Every cell** |
| 6.1 | Backprop | BFRV | speaker-dependent | microphone | 572/624 91.7% | 557/624 89.3% | Within the seed spread ([note 5](#5-backprop-the-starting-weights-are-lost)) |
| 6.2 | Backprop | BFRV | speaker-independent | microphone | 391/440 88.9% ([note 1](#1-two-arithmetic-slips-in-the-thesis)) | 388/440 88.2% | Within the seed spread |
| **new** | Backprop | **TFRV** | speaker-dependent | microphone | not tested | 574/624 92.0% | First run |
| **new** | Backprop | **TFRV** | speaker-independent | microphone | not tested | 397/440 90.2% | First run |

The full confusion matrices are in
[`results/chapter6-reproduction.json`](../results/chapter6-reproduction.json). The
thesis's own matrices are in
[`chapter6_targets.json`](../src/blindman/repro1995/chapter6_targets.json), extracted
from the recovered Chapter 6 by [`tools/extract_chapter6.py`](../tools/extract_chapter6.py)
and cross-checked against Table 6.7.

**The undone experiment.** §6.2.2 left the backprop benchmark on TFRV to future work.
It now gives 92.0% speaker-dependent and 90.2% speaker-independent (seed 1995; over nine
seeds, 90.9 ± 1.1% and 89.7 ± 1.1%). Fuzzy ARTMAP on the same features gives 98.2% and
94.1%. **The thesis's conclusion holds on TFRV too:** Fuzzy ARTMAP beats the backprop
benchmark by 4 to 7 points.

## What the port does

The port follows the code that survives, not textbook Fuzzy ARTMAP. Most of it
reproduces exactly because the 1995 network is deterministic:

- **Training vigilance 1.0 with fast learning and no recoding.** Every training vector
  that is not an exact duplicate founds its own category, set equal to the input.
- **Testing vigilance 0.5.** With complement coding, a category's similarity to the
  input is 1 minus their mean absolute difference, so the test vigilance almost never
  resets. The winner is in effect the nearest training template under the L1 distance.
  No test input was UNRECOGNIZED.
- **Features:** formant ratios **concatenated** over time ([F3/F2, F2/F1, F3/F1] for
  TFRV), converted to normalized polar angle (eq. 5.4), then linearly time-warped by
  index sampling to 500 (TFRV) or 300 (BFRV). A unit test checks the warp against a
  literal transcription of the MATLAB loop.
- **Backprop:** 50 tan-sigmoid hidden nodes and 8 linear outputs, batch training with
  momentum 0.95 and an adaptive learning rate. As in BPMAPPER.M, it trains on the
  Fuzzy ARTMAP weight matrix, **including its spare all-ones rows with all-zero
  targets**.

**The protocol** (§6.2), reconstructed and checked against the thesis's row totals
before any network ran:

- **Speakers:** the eleven recorded on both channels: AH, BT, DG, DH, DY, IH, JD, LP,
  LR, MJ and MO. DB has 40 microphone samples but no telephone copy; "the same training
  and test sets were used in all tests" (§6.2.1) therefore excludes DB.
- **Speaker-dependent:** each speaker's first half, by recording session, trains and the
  second half tests. DH (13 sessions) and LR (9) are split mid-session: phrases 2–5 of
  the middle session train and phrases 6–9 test. This gives exactly the thesis's row
  totals, 77 for phrases 2–5 and 79 for phrases 6–9, 624 in all.
- **Speaker-independent:** the first five tokens of each phrase per speaker; train on
  ten speakers (400 samples), test on the eleventh, rotated eleven times.
- **Sessions are numbered on the microphone schedule** for both channels, so the
  telephone sets are the same recordings. Some telephone sessions carry a different
  date from their microphone copy (DH 0919/0927, DG 1109/1108), and one microphone
  session straddles two dates (MJ 1107/1108).

## Notes on every difference

### 1. Two arithmetic slips in the thesis

Both are in the original Word files, not introduced by the recovery:
- **Table 6.4-M:** the diagonal sums to 413, but the table and Table 6.7 print 414
  (94.1%). The port gets 413, cell for cell, which confirms the slip. The true rate is
  93.9%.
- **Table 6.2:** 391/440 is 88.9%, but the thesis prints 88.7%.

So two of the thesis's quoted rates are slightly off: Fuzzy ARTMAP / BFRV /
speaker-independent / microphone is 93.9%, not 94.1%, and the benchmark's
speaker-independent rate is 88.9%, not 88.7%.

### 2. BFRV is reconstructed, not ported

No BFRV version of the code survives: FARTMAPT.M, BPTESTER.M and Annexes E and G all
compute TFRV. The BFRV path is built from §5.7.2 (eq. 5.3, length 300). It reproduces
Tables 6.4-M and 6.4-T cell for cell, which confirms the reconstruction.

### 3. Two phrase-7 files (open)

In Tables 6.3-M and 6.5-M the port matches the total, but sends phrase-7 test files
`FAH11237` and `FLP12057` to phrase 2. The thesis records phrase 3 for the same row:
two files in 6.3-M, one in 6.5-M. Its column totals agree with its own placement.

What the port shows:
- Both decisions are close. The three best templates lie within 0.5 points of
  similarity of each other.
- **No phrase-3 template is among the three best** for either file, so one changed
  template is an unlikely explanation.

The cause is still open. It has no effect on any recognition rate.

### 4. Telephone: nine test files did not survive

DY's 1104 session has no telephone copy, and MO's 1123 phrase 6 is missing. All nine
fall in the speaker-dependent test half, so those two tests have 615 test files instead
of 624. Their rates stay within 1 point of the thesis. The speaker-independent
telephone tests use only early sessions, so they are unaffected and match cell for cell.

### 5. Backprop: the starting weights are lost

BPMAPPER.M loads hand-picked Nguyen-Widrow weights (`bpinit.mat`, "the set that
produced the quickest convergence was kept", §6.2.2) and then a previously trained
network (`bprtmapt.mat`). Neither file survives, so the port draws Nguyen-Widrow weights
from a seed. Over nine seeds:

| Test | Thesis | Port, seed 1995 | Port, nine seeds |
|---|---|---|---|
| 6.1 BFRV speaker-dependent | 91.7% | 89.3% | 89.8 ± 1.2% (88.5–91.5) |
| 6.2 BFRV speaker-independent | 88.9% | 88.2% | 88.3 ± 1.1% (86.1–89.8) |

These were measured on macOS (Apple M4 Pro, numpy 2.3.5). A different BLAS library
can change the training trajectory much as a new seed does, so results on other
machines should fall in the same range rather than repeat these figures.

The thesis's 6.1 result is at the top of the seed range, which fits a hand-picked
initialization. The epoch limit follows the code (`me = 900`, also in Annex F); §6.2.2's
text says 1000.

## The score gate

[`tests/test_reproduction.py`](../tests/test_reproduction.py) runs the full
reproduction (about 15 seconds) and encodes the expectations above:
- every cell, for the four tables that match exactly;
- the known two-cell difference, for 6.3-M and 6.5-M;
- 615 files and a rate within 1 point, for the telephone speaker-dependent tests;
- within 4 points, for backprop at seed 1995. That bound is the spread over nine seeds
  (largest deviation 3.2 points), not a claim about the thesis.

CI runs it on every push and pull request, and nightly. A change that moves any result
fails the build.

## Not done in Phase 0

- **The Octave cross-check of the 2015 refactor.** It is no longer needed to validate
  the port, since the port matches the thesis directly, but it would confirm that the
  2015 refactor behaves the same.
- **Docker image, metrics dashboard, MCP harness.** These belong with Phase 1 and later,
  when there is more than one result to track.
