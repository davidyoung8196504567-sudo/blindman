# Source code

## `1995/` — the code as used for the thesis

These are the working files from the April 1995 ASR demonstration disk. Most were preserved
inside `ASR_DEMO.EXE`, a self-extracting ZIP; the rest were loose files on the same disk. They
were written for **MATLAB 4.0** under Windows for Workgroups 3.11, orchestrated by *Stdemo
Player 1.5* scripts (`.STD`).

| File | Stage | Purpose | Annex |
|---|---|---|---|
| `VOXRECFL.STD`, `VOXRECFT.STD`, `VOXRECGL.STD`, `VOXRECGT.STD` | — | Stdemo scripts: fast/graphic learn and test | B |
| `MAKESPEC.M` | 2 | Build the spectrogram in chunks (limited RAM) | C |
| `FORMANT3.M` | 3 | Noise masking, silence reduction, peak picking, formant extraction | D |
| `FARTMAPT.M` | 4 | Fuzzy ART Map network: learn and recognize | E |
| `FASTMAPT.M` | 4 | Learn-only, no-plot variant of `FARTMAPT.M` | — |
| `BPMAPPER.M`, `BPTESTER.M` | 4 | Backpropagation benchmark network: train and test | F, G |
| `README.TXT` | — | Instructions from the demo disk | — |

These files differ from the listings printed in the annexes only in comment line-wrapping and a
few small edits (for example, `whitebg` is commented out in some files). The annexes reflect the
text as submitted in May 1995.

**Not included:** `LOADWAV.M`, a 1994 `.WAV` reader © Charles W. Therrien, which the demo used
to load recordings. It is third-party code. Modern MATLAB (`audioread`) and Python
(`scipy.io.wavfile`) replace it.

## `2015-refactor/` — the author's 2015 revisit

These are the same programs, refactored by the author in **MATLAB R2015** (February–October
2015) while revisiting the thesis work. The edits include upper-case function names, `end;` →
`end`, and single-line `if` statements split onto separate lines.

Licensed under the MIT License (see [LICENSE](../../LICENSE)).
