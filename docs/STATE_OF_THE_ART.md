# State of the art: speech recognition and speech databases, 2026

> **Draft for review, 2026-11-08.** The world in 2026 compared with 1995: what exists, what is
> free to use, and where open problems remain. The aim is to rebaseline Stage 2 before building
> anything, so that it does not reinvent what is already solved. Leaderboards change monthly;
> every figure here is dated, and any marked *check* still needs a primary source.

## 1. The short version

- **Transcribing speech is a solved commodity for major languages.** Open models with free
  weights transcribe English at about 5% average word error rate across mixed test sets. They
  identify the language, and cover from about 100 languages (Whisper) to more than 1,600
  (Meta's Omnilingual ASR).
- **The 1995 task and the 2026 task are different problems.** The thesis classified one of
  eight known phrases. Today's systems transcribe any words. A 98% phrase-classification rate
  and a 5% word error rate cannot be compared directly.
- **Free data is plentiful.** LibriSpeech, Common Voice, FLEURS and Speech Commands are all
  free, and together cover read speech, crowd-sourced speech in more than 100 languages, and
  spoken digits.
- **The open problems are where this project's ideas already point:** accents, today's mix of
  telephone channels, short commands, learning without forgetting, and the same speaker decades
  apart. Section 5 maps each one.

## 2. Checking two claims

Two claims came from a conversation with Amazon's Alexa assistant.

| Claim | Verdict |
|---|---|
| "Whisper was released as open source by OpenAI." | **Correct.** Code and weights are under the MIT licence ([GitHub](https://github.com/openai/whisper)). It was released in September 2022; `large-v3-turbo` followed in October 2024. |
| "Whisper handles accent detection in the first 30 seconds." | **Partly wrong.** Whisper detects the **language**, not the accent, from the first 30-second window, and then transcribes the whole file in that language ([detection guide](https://www.mintlify.com/openai/whisper/guides/language-detection), [Phonexia comparison](https://docs.phonexia.com/products/speech-platform-4/technologies/language-identification/lid-vs-whisper-autodetect)). It has no accent output. Strong accents can in fact make it pick the wrong language (section 5.1). |
| "LibriSpeech is available for free." | **Correct.** About 1,000 hours of read English from LibriVox audiobooks, CC BY 4.0, from [OpenSLR SLR12](https://openslr.org/12) (Panayotov et al., ICASSP 2015). |

## 3. Speech recognition models

### Open models

The usual yardstick is the [Hugging Face Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard).
It averages word error rate (WER) over several English test sets. Its leader changed several
times in 2026. Snapshots reported in May–November 2026 put the top models between about 4.8%
and 5.5% average WER, with Whisper large-v3 near 7% ([dev.to analysis, 2026-11-07](https://dev.to/ward_ed_6b5e6aa8ded94a987/open-asr-leaderboard-on-hugging-face-ranks-1-and-2-swap-on-a-common-mean-and-8-of-65-rows-skip-453n),
[MarkTechPost, 2026-07](https://www.marktechpost.com/2026/07/23/best-open-speech-recognition-asr-models-in-2026-wer-languages-latency-and-license-compared/)).
Read the live board before quoting a ranking.

| Model | From | Languages | Licence | Why it matters here |
|---|---|---|---|---|
| **Whisper** large-v3, large-v3-turbo | OpenAI, 2022–2024 | ~100 | MIT | The reference baseline everyone compares with. Built-in language ID. |
| **Omnilingual ASR** (300M–7B) | Meta, Nov 2025 | 1,600+, extendable by a few examples | Apache 2.0 (model), CC BY 4.0 (corpus) | The widest coverage; the closest thing to a "universal" recognizer ([model card](https://huggingface.co/facebook/omniASR-LLM-7B/blob/main/README.md)) |
| **Cohere Transcribe**, **Granite Speech 4.1**, **Qwen3-ASR**, **Parakeet / Canary** | Cohere, IBM, Alibaba, NVIDIA | mostly English plus a few | Cohere Transcribe Apache 2.0; others *check* | The 2026 accuracy leaders |
| **wav2vec 2.0, HuBERT, WavLM** | Meta, Microsoft | — | various | Self-supervised encoders: the feature extractors to compare formant ratios against (Phase 2) |
| **VoxLingua107** models | — | 107 | CC BY 4.0 (data) | Language-ID baseline (Phase 3) |

### What changed since 1995

| 1995 | 2026 |
|---|---|
| Hand-built features (formants, ratios) | Features learned from the raw waveform |
| One small network per speaker or vocabulary | One model for many languages and all speakers |
| Hundreds of recordings, made by the author | Hundreds of thousands of hours (Whisper's paper: 680,000) |
| Closed vocabulary, whole-utterance classification | Open vocabulary, word-by-word transcription |
| Minutes to train on a PC | Weeks on GPU clusters; but free to download and run |

What 1995's approach still has that the giants lack: it learns from a handful of examples,
it learns new classes **without forgetting old ones** (ART's stability–plasticity property), and
it is small enough to explain. Those are the angles worth pursuing, not raw accuracy.

## 4. Speech databases

**Free to use**

| Database | What | Size | Licence | Use in this project |
|---|---|---|---|---|
| [LibriSpeech](https://openslr.org/12) | Read English audiobooks | ~1,000 h | CC BY 4.0 | Standard English benchmark |
| Multilingual LibriSpeech | Read audiobooks, 8 languages | ~50,000 h | CC BY (*check*) | Multilingual read speech |
| [Common Voice](https://commonvoice.mozilla.org) | Crowd-sourced read sentences, with self-reported accent | 137 languages (v22) | CC0 | Languages and accents |
| [FLEURS](https://arxiv.org/abs/2205.12446) | The same sentences read in 102 languages | ~12 h per language | CC BY | Language ID; like-for-like comparison across languages |
| [People's Speech](https://arxiv.org/abs/2111.09344) | Diverse English, commercial use allowed | ~30,000 h | CC BY-SA / CC BY | Large English training set |
| [Speech Commands](https://arxiv.org/abs/1804.03209) | One-second words, **including the digits zero to nine** | ~65,000 clips, 35 words (v2) | CC BY 4.0 | Short-utterance and digit benchmark |
| [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) | Spoken digits 0–9 | ~2,000 clips, few speakers | CC BY-SA 4.0 (*check*) | Small digit sanity test |
| [Speech Accent Archive](https://accent.gmu.edu) | One paragraph read by speakers of 200+ native languages | ~2,000+ speakers | CC BY-NC-SA (*check*) | Accent comparison on identical text |
| [L2-ARCTIC](https://psi.engr.tamu.edu/l2-arctic-corpus/) | Non-native English: 24 speakers, 6 first languages | ~27,000 utterances | CC BY-NC 4.0 (*check*) | Controlled accent identification |
| [EdAcc](https://arxiv.org/abs/2303.18110) | Conversations in English with diverse accents | 40 h | *check* | Accented conversational speech |
| CommonAccent | Accent-labelled subset of Common Voice, with a SpeechBrain recipe | — | CC0 (from Common Voice) | Accent-ID baseline |
| VoxLingua107 | YouTube speech in 107 languages | ~6,600 h | CC BY 4.0 | Language-ID training |

**Licensed (paid, through the LDC)**

| Database | What | Note |
|---|---|---|
| TIMIT | 630 speakers, 8 US dialect regions | Contains phrase 2 of the thesis (sentence SA1) |
| [TIDIGITS](https://catalog.ldc.upenn.edu/LDC93S10) | Digit strings, 300+ speakers, ~13 h | The classic digit benchmark |
| Switchboard, Fisher, CallHome | Telephone conversations | Still the standard telephone benchmarks, but recorded 25–35 years ago on the old network |

## 5. Where the open problems are

Each idea raised in this project, against what exists:

### 5.1 Accent identification (from the 1995 defence demonstration)

- **Exists:** accent classifiers (SpeechBrain's CommonAccent recipe) and labelled data
  (L2-ARCTIC, EdAcc, Common Voice, Speech Accent Archive).
- **Open:** a 2025 study found that **language-ID models are in effect accent classifiers**
  ([arXiv 2506.00628](https://arxiv.org/abs/2506.00628)). Heavily accented speech can be routed
  to the wrong language, so the wrong model loads. It is the 1995 demonstration's failure in a
  modern form: speaker independence did not mean accent independence then, and language ID does
  not mean accent robustness now.
- **Don't reinvent:** the classifier. **Do:** test the routing problem with the same phrases
  read in many accents.

### 5.2 Today's telephone channels

- **Exists:** reported effects of narrowband audio on modern models **disagree**, from almost no
  effect on Whisper large-v3-turbo ([ru-asr-telephony](https://github.com/samishekhalard/ru-asr-telephony))
  to 8–12 points of WER ([Deepgram](https://deepgram.com/blog/noise-robust-speech-recognition-techniques)).
  Some benchmarks exist for real call audio ([call-asr-bench](https://github.com/leekery/call-asr-bench)).
  The standard telephone corpora are decades old.
- **Open:** no controlled, open comparison across **today's codec mix**: G.711, G.729, AMR-NB,
  AMR-WB, EVS and Opus, and real mobile and VoIP calls. That is the most clearly unclaimed gap in
  this survey, and the 1994 telephone database gives it a 30-year baseline.

### 5.3 Short utterances and spoken digits

- **Exists:** keyword spotting on Speech Commands is a mature benchmark, and digit recognition
  by modern models is routine.
- **Open for this project, not for the field:** making the formant-ratio front end work on
  one-word inputs. This is worth doing because the IVR goal (saying 0–9, * and # instead of
  pressing them) needs it, not because it would beat the state of the art.

### 5.4 Learning without forgetting

- **Exists:** large models are adapted with fine-tuning and adapters (LoRA), which can erase
  earlier skills ("catastrophic forgetting").
- **Open:** adding a speaker, accent or language **without retraining and without forgetting**
  remains an active research problem. Fuzzy ARTMAP's original selling point fits it directly.

### 5.5 The same voice 30 years apart

- **Exists:** speaker-ageing research uses mostly a few years' gap, or public figures' archival
  recordings.
- **Open:** a controlled same-speaker, same-phrase, same-microphone recording 32 years apart
  (1994 against 2026) is rare. The author's new recordings would make it a small but genuinely
  new data point.

### 5.6 Universal vocalization (Phase 4)

Already surveyed in [STAGE2.md](STAGE2.md) (NatureLM-audio, Project CETI, the Prat et al.
fruit-bat dataset). Omnilingual ASR's few-example extension to new languages is the nearest
human-speech analogue.

## 6. What this means for the plan

- **Use, don't build:**
  - Whisper and Omnilingual ASR as baselines;
  - LibriSpeech, Common Voice, FLEURS and Speech Commands as data;
  - the Open ASR Leaderboard's evaluation code for word error rates.
- **Build only where the gaps are:**
  - accent routing;
  - the modern telephone-channel comparison;
  - learning without forgetting;
  - the 30-year same-speaker recordings.
- **Report honestly:** the 1995 recognizer is a historical baseline. Its value now is in the
  questions it raises, not in competing on transcription accuracy.

## Sources

- OpenAI Whisper: <https://github.com/openai/whisper>; Radford et al., "Robust Speech Recognition via Large-Scale Weak Supervision", 2022
- Whisper language detection: <https://www.mintlify.com/openai/whisper/guides/language-detection>; <https://docs.phonexia.com/products/speech-platform-4/technologies/language-identification/lid-vs-whisper-autodetect>
- Whisper with accent-aware language ID, Interspeech 2023: <https://www.isca-archive.org/interspeech_2023/vachhani23_interspeech.pdf>
- Open ASR Leaderboard: <https://huggingface.co/spaces/hf-audio/open_asr_leaderboard>; snapshots: <https://dev.to/ward_ed_6b5e6aa8ded94a987/open-asr-leaderboard-on-hugging-face-ranks-1-and-2-swap-on-a-common-mean-and-8-of-65-rows-skip-453n>, <https://www.marktechpost.com/2026/07/23/best-open-speech-recognition-asr-models-in-2026-wer-languages-latency-and-license-compared/>, <https://pinggy.io/blog/best_open_source_self_hosted_speech_to_text_models/>, <https://www.appen.com/blog/hugging-face-open-llm-leaderboard>
- Meta Omnilingual ASR: <https://huggingface.co/facebook/omniASR-LLM-7B/blob/main/README.md>; <https://venturebeat.com/ai/meta-returns-to-open-source-ai-with-omnilingual-asr-models-that-can>; <https://the-decoder.com/metas-omnilingual-asr-brings-speech-recognition-to-1600-languages/>
- LibriSpeech: <https://openslr.org/12>
- FLEURS: <https://arxiv.org/abs/2205.12446>; People's Speech: <https://arxiv.org/abs/2111.09344>
- Speech Commands: <https://arxiv.org/abs/1804.03209>; Free Spoken Digit Dataset: <https://github.com/Jakobovski/free-spoken-digit-dataset>; TIDIGITS: <https://catalog.ldc.upenn.edu/LDC93S10>
- Accents: EdAcc <https://arxiv.org/abs/2303.18110>; "LID Models are Actually Accent Classifiers" <https://arxiv.org/abs/2506.00628>
- Telephone channel: <https://github.com/samishekhalard/ru-asr-telephony>; <https://github.com/leekery/call-asr-bench>; <https://deepgram.com/blog/noise-robust-speech-recognition-techniques>; <https://kili-technology.com/blog/asr-models-guide-word-error-rate-benchmarks-and-failure-modes-2026>
