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
| Word 6.0 → `.docx`, `.pdf` | LibreOffice 26.8 (headless). Current Microsoft Word for Mac no longer opens Word 6.0 files. Chapters 3–5 were rendered via flat OpenDocument (`.fodt`) with page breaks added; see Pagination. |
| `.docx` → Markdown | pandoc 3.8 |
| Embedded figures (Windows EMF) → PNG | LibreOffice → PDF → PyMuPDF, cropped to content at 200 dpi |
| Vector drawings (Word 6 drawing layer) → PNG | Cropped from the rendered PDF pages at 200 dpi. pandoc drops these objects. |
| Annex code listings → Markdown code blocks | macOS `textutil` plain-text extraction |

Fonts: the documents use Times New Roman. LibreOffice substituted the metrically identical
Liberation Serif, so line breaks and page layout are preserved. Greek and mathematical symbols
(ρ, α, Σ, ≡, →) converted correctly.

## Figures corrected from the printed copy

Several vector drawings used Word 6 floating text boxes and frames. LibreOffice does not position
these correctly, so the converted versions were damaged. In November 2026 the affected pages were
scanned from the author's printed copy of the thesis (flatbed, 600 dpi greyscale). The figures
were cropped from the scans, levelled to remove show-through from the reverse side of the page,
and downsampled to 200 dpi to match the other figures.

| Figure | Printed page | Conversion defect | Fix |
|---|---|---|---|
| Fig 2.1 Simplified Biological Neural Network | 5 | Labels ("Incoming Axons…", "Dendrites", "Cell Body") displaced | Replaced with scan |
| Table 2.1 Comparison of Conventional and Neural Network Computation | 8 | Caption pushed into the Fig 2.3 table; a stray label left below the table | Caption restored as text; stray label removed |
| Fig 2.3 Typical Neuron Activation Functions | 9 | Table cells filled with displaced captions and labels | Replaced with scan |
| Fig 2.4 ANN Architecture Nomenclature | 12 | Layer guide lines, layer arrows and connections drawn differently from the original | Replaced with scan |
| Fig 3.3 The Fuzzy ART ANN Model | 34 | Almost entirely lost; one callout left on a blank page, and the figure missing from the Markdown | Replaced with scan |
| Fig 3.4 Fuzzy ARTMAP architecture | 37 | Stray "Field 2 (F2) – N Nodes…" label overlaps the diagram | Replaced with scan |
| Fig 5.1 RMC Speech Database File Naming Convention | 62–63 | Callout box ran off the page; caption landed on the next page | Diagram replaced with scan, placed above its caption on p. 63 |
| Fig 5.2 ASR System Hardware Components | 65 | Fig 5.1's "Speaker's Initials" label overprinted where "telephone recording" belongs | Replaced with scan |
| Fig 5.21 Modified Fuzzy ART Map ANN | 84 | A paragraph was overprinted on itself above the figure | Replaced with scan; the paragraph reset as normal text above it |

In the PDFs the damaged region of each page was blanked and the scan inserted in its place. The
surrounding text and the searchable text layer are unchanged. On p. 84 the opening of the
paragraph "The network learns the mapping…" now sits above the figure, where the conversion put
it; in the printed copy it follows the figure on p. 85. The `docx/` files are the unedited
conversion and still contain these defects.

The other figures were checked visually against the converted text, not against the printed copy.
Fig 2.4 passed that check but differed from the print, so the remaining drawing-layer diagrams
(Figs 3.1, 3.2 and 4.2) may also differ in detail. The embedded pictures (screen captures,
spectrograms, waveforms, formant plots and Fig 2.2) come from the documents' own image data rather
than the drawing layer, and are much less likely to be affected.

## Pagination

The thesis's own table of contents records the printed page of all 83 section headings, which
gives an exact check on the PDF's page breaks. In the first conversion, eight headings
(§§3.4, 3.8.3, 3.9, 3.10, 4.2.3, 5.6.2, 5.6.4 and 5.9) sat at the foot of the page before the one
the printed copy starts them on, often with no text under them. Chapter 4 also ran one page long
from §4.4 on, because two lines of §4.3 spilled onto a page of their own.

Chapters 3, 4 and 5 were therefore re-rendered with a page break before each of those eight
headings. In chapter 4 the blank lines between the four bullets of §4.3 were made shorter so the
section fits on its page, as it does in print. The Fig 3.2 drawing, which Word anchored to the
§3.4 heading, was re-anchored so it stays on its page. All 83 headings in the PDF now fall on
their printed page, and the combined PDF has 178 pages.

The re-rendering went through LibreOffice's OpenDocument format, so a few lines in chapters 3–5
wrap one word differently from the first conversion. Neither version is line-for-line identical
to the 1995 printing, which used different font metrics. The page breaks are not reflected in the
`docx/` files.

## Markdown limitations

The **PDF is the faithful version**. The Markdown is for reading on GitHub and has these limits:

- **Stacked fractions** in equations (e.g. 3.10, the choice function) were typeset in Word 6 as
  an underlined numerator above a denominator line. In Markdown they appear as two consecutive
  lines.
- **Vector drawings** (Figs 3.1, 3.2, 4.2) are included as images cropped from the PDF, and
  Figs 2.1, 2.3, 2.4, 3.3, 3.4, 5.1, 5.2 and 5.21 as scans of the printed copy. Each is placed after the
  paragraph that first mentions it. The circled-word alignment illustration in §6.4.5 appears
  as plain text only.
- **Tables with merged cells** (including the Chapter 6 confusion matrices) are written as HTML
  tables, which GitHub renders.

Page breaks can differ slightly from the 1995 printing.

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
