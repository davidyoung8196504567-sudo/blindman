# RMC Speech Database — formant feature files

These are the formant-track features extracted from the RMC Speech Database used in the thesis.
The data are described in Chapter 5 (§5.2–5.6) and Tables 5.1–5.2.

- **Recorded:** 2 September – 22 December 1994, Room 5018, Sawyer Building, RMC Kingston.
  The speakers were staff and post-graduate students of the Department of Electrical and
  Computer Engineering, who volunteered their voices.
- **Speakers:** 14 (12 male, 2 female), identified here by initials.
- **Phrases:** the eight phonetically rich phrases numbered 2–9 in Table 5.2. Phrases 0 and 1
  (date/time and name) were used only to register the session and are not included.

| Folder | Channel | Sampling | Files |
|---|---|---|---|
| [`microphone/`](microphone/) | Realistic Super Cardioid microphone, batch recorded via tape | 22050 Hz, 16-bit | 1,310 |
| [`telephone/`](telephone/) | Same recordings played over a local telephone call, picked up at the far end | 8000 Hz, 16-bit | 1,237 |

The raw `.WAV` recordings are not included. In 1995 they were compressed (WazWav 4:1),
archived with ARJ, and stored on custom 1.92 MB-formatted floppy disks; those archives did not
survive. These formant tracks are the input to the recognizer (`FARTMAPT.M`), so the thesis's
classification results can be reproduced from them.

## File format

Each file is a **MATLAB v4 `.MAT`** file and opens directly in MATLAB, Octave, or Python
(`scipy.io.loadmat`). It contains two variables:

| Variable | Shape | Contents |
|---|---|---|
| `Formant` | 3 × N, double | Formant frequency tracks in Hz. Row 1 = F1, row 2 = F2, row 3 = F3, one column per retained time-slice. Values are limited to the 300–3300 Hz telephone band. Produced by `FORMANT3.M` (Annex D). |
| `WaveFile` | string | Name of the source recording, e.g. `mdy09022.wav` (microphone) or `tdy09022.wav` (telephone) |

## File naming

`F DY 09 02 2 .MAT`, following the convention in Figure 5.1:

| Part | Meaning |
|---|---|
| `F` | Formant file. The source WAV name begins with `M` (microphone) or `T` (telephone) here. |
| `DY` | Speaker initials |
| `09 02` | Recording date, month and day (1994) |
| `2` | Phrase number (Table 5.2) |

## Files per speaker

| Speaker | AH | BT | CW | DB | DG | DH | DY | IH | JD | LP | LR | MJ | MO | WB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| microphone | 111 | 64 | 8 | 40 | 128 | 104 | 383 | 48 | 80 | 112 | 72 | 64 | 80 | 16 |
| telephone | 111 | 64 | — | — | 128 | 104 | 375 | 48 | 80 | 112 | 72 | 64 | 79 | — |

## Loading example (Python)

```python
from scipy.io import loadmat
m = loadmat("microphone/DY/FDY09022.MAT")
f1, f2, f3 = m["Formant"]      # Hz
print(m["WaveFile"][0], m["Formant"].shape)
```

Licensed CC BY 4.0. Please cite the thesis (see the repository [LICENSE](../../LICENSE)).
