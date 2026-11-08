"""Extract the Chapter 6 confusion matrices from the recovered thesis Markdown.

In the thesis each table's caption sits *below* its table, so every caption is
paired with the table that precedes it. The result is checked against Table 6.7,
the summary, before it is written.

Usage: python tools/extract_chapter6.py > src/blindman/repro1995/chapter6_targets.json
"""

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAP6 = ROOT / "thesis-1995" / "markdown" / "CHAP6.md"

# Table id -> (recognizer, representation, protocol, channel)
TABLES = {
    "6.1": ("backprop", "BFRV", "SD", "microphone"),
    "6.2": ("backprop", "BFRV", "SI", "microphone"),
    "6.3-M": ("fuzzy_artmap", "BFRV", "SD", "microphone"),
    "6.3-T": ("fuzzy_artmap", "BFRV", "SD", "telephone"),
    "6.4-M": ("fuzzy_artmap", "BFRV", "SI", "microphone"),
    "6.4-T": ("fuzzy_artmap", "BFRV", "SI", "telephone"),
    "6.5-M": ("fuzzy_artmap", "TFRV", "SD", "microphone"),
    "6.5-T": ("fuzzy_artmap", "TFRV", "SD", "telephone"),
    "6.6-M": ("fuzzy_artmap", "TFRV", "SI", "microphone"),
    "6.6-T": ("fuzzy_artmap", "TFRV", "SI", "telephone"),
}

# Arithmetic slips in the thesis's own tables: table id -> note. They are in
# the original Word files; they were not introduced by the recovery.
KNOWN_SLIPS = {
    "6.2": "391/440 is 88.9%, but the table and Table 6.7 print 88.7%.",
    "6.4-M": "The diagonal sums to 413, but the table's total cell and Table 6.7 both "
             "print 414 (94.1%). 413/440 is 93.9%.",
}

# Table 6.7 (summary), as printed: table id -> (correct, total, percent)
SUMMARY = {
    "6.1": (572, 624, 91.7), "6.2": (391, 440, 88.7),
    "6.3-M": (606, 624, 97.1), "6.4-M": (414, 440, 94.1),
    "6.5-M": (613, 624, 98.2), "6.6-M": (414, 440, 94.1),
    "6.3-T": (549, 624, 88.0), "6.4-T": (375, 440, 85.2),
    "6.5-T": (571, 624, 91.5), "6.6-T": (383, 440, 87.0),
}


def cells(row):
    return [html.unescape(re.sub(r"<[^>]*>", "", c)).strip()
            for c in re.findall(r"<t[dh].*?</t[dh]>", row, re.S)]


def main():
    text = CHAP6.read_text(encoding="utf-8")
    tables = [(m.start(), m.group(0)) for m in re.finditer(r"<table.*?</table>", text, re.S)]
    out = {"source": "thesis-1995/markdown/CHAP6.md", "phrases": list(range(2, 10)),
           "rows": "spoken phrase", "cols": "recognized phrase", "tables": {}}
    for m in re.finditer(r"\*\*Table (6\.[1-6](?:-[MT])?) ", text):
        tid = m.group(1)
        before = [t for pos, t in tables if pos < m.start()]
        rows = re.findall(r"<tr.*?</tr>", before[-1], re.S)
        matrix = []
        for r in rows[1:9]:
            c = cells(r)
            assert c[0] == str(len(matrix) + 2), (tid, c)
            matrix.append([int(v) if v else 0 for v in c[1:9]])
        correct = sum(matrix[i][i] for i in range(8))
        total = sum(map(sum, matrix))
        printed = SUMMARY[tid]
        if (correct, total) != printed[:2] and tid not in KNOWN_SLIPS:
            sys.exit(f"Table {tid}: matrix gives {correct}/{total}, Table 6.7 says {SUMMARY[tid]}")
        rec, rep, proto, chan = TABLES[tid]
        out["tables"][tid] = {"recognizer": rec, "representation": rep, "protocol": proto,
                              "channel": chan, "correct": correct, "total": total,
                              "rate": round(100 * correct / total, 1),
                              "printed_correct": printed[0],
                              "printed_rate": printed[2],
                              "confusion": matrix}
        if tid in KNOWN_SLIPS:
            out["tables"][tid]["slip"] = KNOWN_SLIPS[tid]
    assert set(out["tables"]) == set(TABLES), sorted(out["tables"])
    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
