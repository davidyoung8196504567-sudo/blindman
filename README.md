# BLINDMAN

**BLINDMAN** is the codename for an agent that navigates entirely by sound, with no visual or GUI
input.

It is built on the idea of an **AUI (Audio User Interface)**, a term coined by the author as the
audio counterpart to the GUI (Graphical User Interface) that computing still depends on so
heavily. Interfaces designed for hearing rather than sight are essential for people with visual
impairments. That is where the name comes from.

The AUI concept, including the sound dimensions it uses to carry meaning (frequency, volume,
waveform, timing, timbre, formant ratios and spatial direction), is described in
[`docs/AUI.md`](docs/AUI.md).

## Foundation: the 1995 thesis

The project resurrects and extends research begun in 1993–1995 during post-graduate studies at
the Royal Military College of Canada and Queen's University:

> **[A Fuzzy ART Map Neural Network Speech Recognition System Based on Formant Ratios](thesis-1995/)**
> Capt D.P. Young — M.Eng. thesis, Royal Military College of Canada, May 1995

The work used a Fuzzy ART Map neural network to recognize spoken phrases over telephone channels
from formant-ratio features. In 1995 it was limited by the hardware, by a 9600-baud Internet
connection, and by the lack of public speech datasets, so the author recorded his own. The
recovered thesis, the original MATLAB code and the speech feature database are all in
[`thesis-1995/`](thesis-1995/):

| | |
|---|---|
| Read the thesis (PDF) | [`thesis-1995/Young-1995-FuzzyARTMAP-ASR-Thesis.pdf`](thesis-1995/Young-1995-FuzzyARTMAP-ASR-Thesis.pdf) |
| Read on GitHub (Markdown) | [`thesis-1995/markdown/`](thesis-1995/markdown/) |
| 1995 source code and 2015 refactor | [`thesis-1995/code/`](thesis-1995/code/) |
| RMC Speech Database (formant features) | [`thesis-1995/data/`](thesis-1995/data/) |
| How it was recovered | [`thesis-1995/RECOVERY_NOTES.md`](thesis-1995/RECOVERY_NOTES.md) |

## Status

- **Stage 1: recover the 1995 research.** The thesis is recovered from its original Word 6.0
  files. Diagrams damaged in conversion have been corrected from scans of the printed copy. The
  search for the archived raw `.WAV` recordings is ongoing.
- **Stage 2: build on it.** Planned. Today's CPUs and storage allow far more of each recording's
  detail to be kept than the 1995 processing budget allowed.

## License

Code: MIT. Thesis and data: CC BY 4.0. See [LICENSE](LICENSE).
