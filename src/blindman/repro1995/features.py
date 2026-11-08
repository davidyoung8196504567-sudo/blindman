"""Feature representations, ported from FARTMAPT.M (Annex E) and §5.7.

All three steps follow the 1995 code exactly:

1. Formant ratios, each a vector over time, **concatenated** end to end
   (not interleaved): TFRV = [F3/F2, F2/F1, F3/F1] (eq. 5.5).
2. Normalized polar angle: NPA = arctan(ratio) / (pi/2) (eq. 5.4).
3. Linear time warp (LTW) to a standard length by index sampling.

The TFRV path (length 500) is a port of the surviving code. The BFRV path
(length 300) is **reconstructed from the text** (§5.7.2, eq. 5.3): no BFRV
version of the code survives.
"""

from __future__ import annotations

import numpy as np

TFRV_LENGTH = 500
BFRV_LENGTH = 300


def ltw(x: np.ndarray, length: int) -> np.ndarray:
    """Linear time warp, as in FARTMAPT.M.

    MATLAB: ``LTW(i) = X(ceil(L/length*i))`` for i = 1..length-1, and
    ``LTW(length) = X(L)``. The expression is evaluated in the same order,
    so the indices match MATLAB's double arithmetic bit for bit.
    """
    x = np.asarray(x, dtype=float)
    n = x.size
    i = np.arange(1, length, dtype=float)
    idx = np.ceil((n / length) * i).astype(int) - 1  # MATLAB is 1-based
    return np.concatenate([x[idx], x[-1:]])


def npa(ratios: np.ndarray) -> np.ndarray:
    return np.arctan(ratios) / (0.5 * np.pi)


def tfrv(formants: np.ndarray, length: int = TFRV_LENGTH) -> np.ndarray:
    f1, f2, f3 = formants
    return ltw(npa(np.concatenate([f3 / f2, f2 / f1, f3 / f1])), length)


def bfrv(formants: np.ndarray, length: int = BFRV_LENGTH) -> np.ndarray:
    f1, f2, f3 = formants
    return ltw(npa(np.concatenate([f3 / f2, f2 / f1])), length)


REPRESENTATIONS = {"TFRV": tfrv, "BFRV": bfrv}
