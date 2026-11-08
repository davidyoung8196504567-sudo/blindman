# Research Journal

Log for BLINDMAN Stage 2. One entry per working session, newest at the top.
The plan is in [docs/STAGE2.md](docs/STAGE2.md). The template is shared with
[bug-bash](https://github.com/davidyoung8196504567-sudo/bug-bash).

Entry template:

```
## YYYY-MM-DD | Phase X | ~H hours
**Goal:** what this session set out to do
**Done:** what actually got done
**Findings:** anything surprising, measured, or worth putting in the report
**Caught in review:** AI-written code or tests rejected or corrected, and why
**Blockers / risks:**
**Next:** the first thing to do next session
```

---

## 2026-11-08 | Phase 0 | one session

**Goal:** Port the 1995 recognizer to Python and reproduce Chapter 6 from the recovered
formant files.

**Done:**
- Python package `blindman.repro1995`:
  - features (TFRV ported, BFRV reconstructed from §5.7.2);
  - Fuzzy ARTMAP as written in FARTMAPT.M;
  - the backprop benchmark from BPMAPPER.M and BPTESTER.M;
  - the §6.2 protocol and a command-line runner.
- The thesis's ten confusion matrices extracted to JSON and cross-checked against
  Table 6.7.
- 26 tests, including a score gate on the reproduction. CI on Python 3.12 and 3.14,
  plus a nightly run.
- Results and every discrepancy written up in [docs/PHASE0.md](docs/PHASE0.md).

**Findings:**
- **Fuzzy ARTMAP reproduces exactly.** Four tables match cell for cell. Two more match
  in total, with two cells moved (unexplained). The telephone speaker-dependent tests are within 1
  point, after losing nine test files.
- **Two arithmetic slips in the 1995 thesis.**
  - Table 6.4-M sums to 413, not the printed 414; the port gets 413.
  - Table 6.2's 391/440 is 88.9%, not the printed 88.7%.
- **The split was recovered from the row totals alone.** The thesis's 77/79 per-phrase
  test counts pin down the speaker set (DB excluded) and the mid-session split for
  the two odd-session speakers, before any network ran.
- **New result:** backprop on TFRV gives 92.0% speaker-dependent and 90.2%
  speaker-independent, against Fuzzy ARTMAP's 98.2% and 94.1%. The 1995 conclusion
  holds.
- **Backprop varies by about ±1.1 points with the seed**, and by up to 3.2 points from
  the thesis. The CI tolerance was first set at 3 points, which two of the nine seeds
  break; widened to 4 before the first push. The thesis's 91.7% sits at
  the top of the range, which fits its hand-picked initial weights.

**Caught in review:**
- My first look at the tables paired each caption with the table *after* it. In the
  thesis captions sit *below* their tables, so every matrix was off by one. A reviewer
  model flagged it before the extraction tool was written. The tool now checks every
  matrix against Table 6.7, and that check then caught the 6.4-M slip.
- Sessions were first split wherever the phrase number failed to increase. That cut MJ's
  1107/1108 session in two. Now sessions are grouped by date, and a date one day later
  that holds only the missing phrases is merged in.
- Speaker-independent selection was first "the first five sessions". AH's session 4
  lacks phrase 2, which left 54 tokens instead of 55. Changed to the first five tokens
  of each phrase, which matches the text.
- A draft explanation for the two moved phrase-7 files was speculation. The port's own
  numbers argue against it (no phrase-3 template is near). Rewritten as an open item.

**Blockers / risks:**
- The 1995 backprop starting weights are lost, so the benchmark can only be reproduced
  statistically.
- The two moved phrase-7 files are unexplained.

**Next:**
- The *Author and tools* statement for the Phase 0 code.
- Phase 1 data decisions: a TIMIT licence or a new volunteer recording drive,
and an open text-to-speech model rather than ElevenLabs.
