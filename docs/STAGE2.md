# Stage 2 Plan: Building on the 1995 Thesis

> **Proposal, open for revision.** Stage 1 recovered the thesis, code and feature data. This page
> sets out how to build on them, in phases. Each phase has a goal, its inputs, what it produces,
> and a check that says whether it worked.

## Starting point

What survives from 1995:

- **The thesis**, fully recovered and checked against the printed copy.
- **The code:** the 1995 MATLAB 4.0 programs and the author's 2015 refactor.
- **The RMC Speech Database feature files:** 2,547 formant tracks (F1–F3) from 14
  speakers saying eight phrases, recorded on microphone and over telephone.

What does not:

- **The raw recordings.** The 1995 floppies hold only the period software (MS-DOS 6.22, Windows for
  Workgroups 3.11, MATLAB 4.0 and toolboxes, shareware audio tools). The `.WAV` archive did not
  survive. New audio is therefore needed for anything upstream of the formant tracks.

The formant tracks are exactly the input to the recognizer (`FARTMAPT.M`), which computes the
formant ratios, normalizes them, warps them to a standard length and classifies them. The
thesis's classification results can therefore be reproduced without the audio.

---

## Phase 0: Reproduce the 1995 results

**Goal.** Port the recognizer and confirm that the recovered data reproduces Chapter 6. This is
the baseline for everything after it, and it proves that Stage 1's recovery is complete.

**Work.**
- Port `FARTMAPT.M` (Fuzzy ARTMAP, with the TFRV and BFRV representations) and the backprop
  benchmark (`BPMAPPER.M`, `BPTESTER.M`) to Python and numpy. The 2015 refactor, run under GNU
  Octave, serves as a cross-check.
- Rebuild the Chapter 6 protocol (§6.2):
  - **Speaker-dependent:** the first half of each speaker's samples train and the second half
    test, in recording order.
  - **Speaker-independent:** five tokens of each of phrases 2–9 per speaker, trained on ten
    speakers and tested on the eleventh, rotated eleven times.
  - Only the eleven speakers with at least 40 samples are used.
- Run the one experiment §6.2.2 left undone: the **backprop benchmark on the TFRV**
  representation.

**Check.** Every test reproduces the thesis results within a few percent:

| Test | Microphone | Telephone |
|---|---|---|
| Fuzzy ARTMAP, TFRV, speaker-dependent (Tables 6.5-M, 6.5-T) | 98.2% | 91.5% |
| Fuzzy ARTMAP, TFRV, speaker-independent (6.6-M, 6.6-T) | 94.1% | 87.0% |
| Fuzzy ARTMAP, BFRV, speaker-dependent (6.3-M, 6.3-T) | 97.1% | 88.0% |
| Fuzzy ARTMAP, BFRV, speaker-independent (6.4-M, 6.4-T) | 94.1% | 85.2% |
| Backprop, BFRV, speaker-dependent / independent (6.1, 6.2) | 91.7% / 88.7% | — |

Any test that does not reproduce gets an explanation, not a tuned parameter.

---

## Phase 1: New audio

**Goal.** Audio for the eight thesis phrases from many more voices, accents and languages, in
both microphone and telephone form, with each source's licence and consent on record.

**Sources, real speech first.**

- **Real speech.**
  - **TIMIT.** Phrase 2, *"She had your dark suit in greasy wash water all year,"* is TIMIT
    sentence SA1, read by all 630 TIMIT speakers from eight US dialect regions. Phrase 3 is close
    to TIMIT's *"Don't ask me to carry an oily rag like that."* TIMIT is licensed through the LDC,
    which charges for it.
  - **Speech Accent Archive.** A single paragraph ("Please call Stella…") read by well over a
    thousand speakers of a few hundred native languages, covering accents of the same text. Free
    for non-commercial use with citation; confirm the current licence.
  - **Mozilla Common Voice.** Real read speech in well over 100 languages, released CC0. It does
    not contain the thesis phrases, so it serves language and accent work rather than phrase
    recognition.
- **New recordings.** The 1995 method still works: volunteers read the eight phrases, now with
  written consent and an open licence. A simple web recorder could collect them, giving an
  *RMC Speech Database 2* that can be published like the original.
- **Synthetic voices (augmentation only).**
  - TTS can generate the eight phrases in many voices, accents and languages cheaply. That is
    useful for stress-testing, but a recognizer trained only on synthetic speech generally does
    not transfer well to real speech.
  - **ElevenLabs cannot be used for this without permission.** Its Prohibited Use Policy forbids
    using its output to develop, train, fine-tune or improve any AI model, or including it in a
    dataset for those purposes, unless the applicable terms expressly allow it. Using it would
    need written agreement from ElevenLabs.
  - The alternative is an open-weight TTS model whose licence permits training use, checked model
    by model.
  - In either case the 1995 volunteers' voices are not cloned. They consented to being recorded,
    not to synthesis.

**Telephone channel.** Any wideband recording can be given a telephone version by simulation: a
300–3300 Hz band-limit, resampling to 8 kHz, and μ-law (G.711) coding, optionally with line
noise. Every new sample can then exist on both channels, as in 1995.

**Check.**
- A data card for each source: licence, consent, speaker count and accent coverage.
- A synthetic-to-real transfer test: train on synthetic speech, test on real speech, and report
  the drop in accuracy.

---

## Phase 2: Formant ratios at full resolution, and against modern features

**Goal.** Answer the question the thesis left open: does the speaker-independence of formant
ratios hold up with many more speakers, accents and languages?

**Work.**
- **Re-run the full 1995 pipeline on new audio** (spectrogram, noise mask, silence reduction,
  formant tracking, TFRV), keeping the detail the 1995 processing budget discarded. That means
  finer time and frequency resolution, more formants, and no fixed-length cut.
- **Add the §7.3 future-work items:**
  - frequency normalization that adapts to each telephone connection;
  - a noise mask tailored to each sample;
  - a higher sampling rate on the telephone channel.
- **Compare on the same splits:**
  - TFRV + Fuzzy ARTMAP;
  - MFCCs with a standard classifier;
  - a self-supervised speech embedding (a wav2vec 2.0, HuBERT or WavLM-type model).

**Check.** A results table across speakers, accents and channels. The thesis claim stands if
TFRV's accuracy drop from speaker-dependent to speaker-independent testing stays small as the
speaker pool grows.

---

## Phase 3: Language identification first, then a language-specific recognizer

**Goal.** The architecture the author intended in 1995: identify the language first, then load
that language's recognizer.

The written thesis plants the seed rather than stating the design:
- §4.4.1 calls for a system that learns "independent of speaker type or spoken language";
- §7.2 credits Fuzzy ARTMAP's localized memory with supporting "modular packaging and
  reconfiguration of active vocabulary."

Spoken language identification itself is now mature, with public models and datasets such as
VoxLingua107 (107 languages, CC BY 4.0). It is the **baseline here, not the contribution**.

**Work.**
- An existing language-identification model as the front end.
- One Fuzzy ARTMAP module per language, loaded on demand, using ARTMAP's incremental learning to
  add a language or vocabulary without retraining the others.

**Check.** End-to-end accuracy against a single multilingual recognizer. Then add a new language
and measure how much the accuracy on the existing languages changes; with ARTMAP it should not
fall.

---

## Phase 4: Toward a universal vocalization model (exploratory)

**The vision.** Recognize communicative sound across humans and other animals, and infer meaning
from the situations in which a pattern is used.

**Where the field is.** This is an active research frontier, not open ground:

- **Earth Species Project's NatureLM-audio (2024)** classifies, detects and captions animal
  sounds across species. Its makers say plainly that it is not a translator.
- **Project CETI (2024)** found combinatorial structure in sperm-whale codas, a "phonetic
  alphabet," but not yet their meaning.
- **Prat et al. (2017)** published about 90,000 Egyptian fruit bat calls annotated with who was
  involved, what they were doing and the context. This is exactly the kind of data that ties sound
  to situation.

**What this project could add.** Two threads come straight from the thesis:

1. **Size-invariant features across species (a hypothesis).**
   - Formant ratios cancel out vocal-tract length between human speakers.
   - Across animals, vocal-tract length scales with body size, and formant spacing tracks it
     (Fitch 1997, *JASA* 102:1213). The same normalization might therefore carry across species
     and body sizes.
   - This is untested and worth testing.
2. **Open-ended learning.**
   - Adaptive Resonance Theory was built to solve the stability–plasticity dilemma: it learns new
     categories without forgetting old ones.
   - That fits discovering unknown call types in data that never stops arriving.

**First experiment.** On the fruit-bat dataset, predict the annotated context from the call's
acoustics, with and without ratio-type features, using Fuzzy ARTMAP and a modern classifier. Keep
the claim to what the result shows.

---

## How this serves BLINDMAN

The [AUI](AUI.md) uses dimensions of sound to carry meaning to a listener. BLINDMAN must do the
reverse: hear those dimensions and recover the meaning. Each phase builds part of that ear:

- recognizing phrases on any voice and channel (Phases 0–2);
- knowing which language it is hearing (Phase 3);
- eventually, interpreting sound it was never taught (Phase 4).

## Open decisions

- **Language for the port:** Python and numpy, with Octave as a cross-check (proposed), or MATLAB.
- **Synthetic speech:** seek written permission from ElevenLabs, or use an open-weight TTS model
  whose licence allows training.
- **Data budget:** whether to license TIMIT through the LDC, and whether to run a new
  volunteer-recording drive.
