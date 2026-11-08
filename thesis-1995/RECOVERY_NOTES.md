# Recovery Notes

Recovered November 2026.

## Source

The thesis was written in **Microsoft Word 6.0** under Windows for Workgroups 3.11 and saved as
16 files (`CHAP0`–`CHAP7`, `REFS`, `ANNEXA`–`ANNEXG`). The internal "last saved" timestamps run
from 3 to 15 May 1995, when the thesis went to print. The files were later copied from floppy disk
to CD-ROM and then to a portable hard drive. Filesystem dates changed during those copies, but
the save dates recorded inside the documents did not.

Three copies existed: loose `.DOC` files in two folders, plus `THESIS.ZIP` (dated 17 May 1995).
**All three are byte-for-byte identical**, and every archive passed a ZIP integrity check. The
files in [`original/`](original/) are those originals, unmodified. Verify them with:

```
shasum -a 256 -c CHECKSUMS.sha256
```

## Conversion

| Step | Tool |
|---|---|
| Word 6.0 → `.docx`, `.pdf` | LibreOffice 26.8 (headless). Current Microsoft Word for Mac no longer opens Word 6.0 files. |
| `.docx` → Markdown | pandoc 3.8 |
| Embedded figures (Windows EMF) → PNG | LibreOffice → PDF → PyMuPDF, cropped to content at 200 dpi |
| Vector drawings (Word 6 drawing layer) → PNG | Cropped from the rendered PDF pages at 200 dpi. pandoc drops these objects. |
| Annex code listings → Markdown code blocks | macOS `textutil` plain-text extraction |

Fonts: the documents use Times New Roman. LibreOffice substituted the metrically identical
Liberation Serif, so line breaks and page layout are preserved. Greek and mathematical symbols
(ρ, α, Σ, ≡, →) converted correctly.

## Known defects

Five vector drawings used Word 6 floating text boxes and frames. LibreOffice does not position
these correctly, and the converted versions are damaged:

| Figure | Original page | Defect |
|---|---|---|
| Fig 2.1 Simplified Biological Neural Network | 5 | Labels ("Incoming Axons…", "Dendrites", "Cell Body") displaced |
| Table 2.1 / Fig 2.3 (activation functions) | 8–9 | Table 2.1 title and the Fig 2.1/2.3 captions pushed into table cells |
| Fig 3.4 Fuzzy ARTMAP architecture | 37 | Stray "Field 2 (F2) – N Nodes…" label overlaps the diagram |
| Fig 5.1 RMC Speech Database File Naming Convention | 62–63 | Callout box runs off the page; caption lands on the next page |
| Fig 5.21 Modified Fuzzy ART Map ANN | 84 | A paragraph of body text is overprinted on itself above the figure |

The diagrams themselves (boxes, arrows, labels) are intact; only the layout around them is wrong.
**Planned fix:** scan these pages from the printed thesis and use the scans to replace or correct
the figures.

Every other figure was checked visually and is correct. That includes the screen captures,
spectrograms, waveforms, formant plots, block diagrams, Figs 2.2, 2.4, 3.1, 3.2, 4.1–4.5, 5.2–5.20
and 6.1–6.2, and all results tables.

### Markdown limitations

The **PDF is the faithful version**. The Markdown is for reading on GitHub and has these limits:

- **Stacked fractions** in equations (e.g. 3.10, the choice function) were typeset in Word 6 as
  an underlined numerator above a denominator line. In Markdown they appear as two consecutive
  lines.
- **Vector drawings** (Figs 2.1–2.4, 3.1, 3.2, 3.4, 4.2, 5.1, 5.2, 5.21) are included as images
  cropped from the PDF, placed after the paragraph that first mentions each one. The circled-word
  alignment illustration in §6.4.5 appears as plain text only.
- **Tables with merged cells** (including the Chapter 6 confusion matrices) are written as HTML
  tables, which GitHub renders.

Page breaks can differ slightly from the 1995 printing. Fig 5.1 is the only case where this
separates a figure from its caption.

## Source code

Annexes B–G print the program source as submitted in May 1995. Two further versions survive:

- **1995 working files** ([`code/1995/`](code/1995/)), taken from the April 1995 ASR demo disk,
  mostly from inside `ASR_DEMO.EXE`. They match the annex listings apart from comment
  line-wrapping and minor edits.
- **The 2015 refactor** ([`code/2015-refactor/`](code/2015-refactor/)). The author revisited the
  work in MATLAB R2015 (February–October 2015) and modernized the code. Their filesystem dates
  (2018) are copy artefacts.

## Not included

- **Third-party software** used in 1995: MS-DOS 6.22, Windows for Workgroups 3.11, MATLAB 4.0
  and toolboxes, Cognos Scenario, GoldWave 2.11, Stdemo Player 1.5, WazWav 0.1 and FORM1968.
  It is proprietary or shareware and runs only on that era of hardware. `LOADWAV.M`
  (© C.W. Therrien, 1994) is also excluded.
- **The raw `.WAV` recordings.** They were archived in 1995 on custom-formatted floppy disks and
  are being looked for. The derived formant features *are* included, in [`data/`](data/).
