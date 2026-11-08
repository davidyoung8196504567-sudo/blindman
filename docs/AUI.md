# The Audio User Interface (AUI)

> **Draft, being rewritten from memory.** The original paper was not preserved. This page
> records the core idea as the author recalls it, as a starting point for the rewrite.

## The idea

A GUI (Graphical User Interface) shows information through visual properties: position, size,
colour, shape and motion. An **AUI (Audio User Interface)** does the same through the properties
of sound that the human brain can tell apart. Each of these properties is an independent
channel, or *dimension*, that can carry meaning or data.

An interface designed this way can be used without sight. That makes it essential for people
with visual impairments, and it also makes it the natural interface for an agent like BLINDMAN,
which navigates by sound alone.

## Dimensions of sound

| Dimension | What the ear and brain perceive |
|---|---|
| **Frequency** | Pitch |
| **Volume** | Loudness |
| **Waveform** | The shape of the vibration (e.g. sine, square, sawtooth) |
| **Timing** | Rhythm, duration, order and spacing of sounds |
| **Timbre** | Tone colour: what distinguishes a flute from a violin playing the same note |
| **Formant ratios** | The relative positions of resonant peaks; how we identify vowels |
| **Spatial direction** | Where a sound comes from, sensed through differences in pressure and arrival time between the two ears |

### Link to the 1995 thesis

Formant ratios are the feature the thesis was built on (see
[Chapter 4, §4.6 Formant Ratio Theory](../thesis-1995/markdown/CHAP4.md)). The *ratios* between
formants identify a vowel independently of whether a man, woman or child speaks it. That
speaker-independence is what makes them useful as an AUI dimension: their meaning survives a
change of voice.

---

## For the rewrite: questions to recall

*These are prompts for the author, not content from the original paper.*

- When and where was the paper written, and for what (course, conference, internal report)?
- For each dimension: what example mapping did the paper give? For instance, which kind of data
  went to pitch, and which went to spatial direction?
- How many dimensions did the paper suggest a listener can follow at once before they interfere
  with each other?
- Did it discuss the reverse direction, i.e. a machine *recognizing* these dimensions in sound,
  as BLINDMAN must?
- Which applications were proposed (telephone services, accessibility, others)?
