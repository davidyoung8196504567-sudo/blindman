import math

import numpy as np

from blindman.repro1995.features import BFRV_LENGTH, TFRV_LENGTH, bfrv, ltw, npa, tfrv


def matlab_ltw(x, length):
    """FARTMAPT.M's loop, transcribed literally with 1-based indices."""
    L = len(x)
    out = [x[math.ceil(L / length * i) - 1] for i in range(1, length)]
    return out + [x[L - 1]]


def test_ltw_matches_the_matlab_loop():
    rng = np.random.default_rng(0)
    for n in [24, 72, 100, 249 * 3, 747, 500, 1000, 3]:
        x = rng.random(n)
        for length in (TFRV_LENGTH, BFRV_LENGTH):
            assert np.array_equal(ltw(x, length), np.array(matlab_ltw(list(x), length)))


def test_npa_range_and_fixed_points():
    assert npa(np.array([1.0]))[0] == 0.5  # a ratio of 1 is 45 degrees
    r = npa(np.array([1e-9, 1.5, 10.0, 1e9]))
    assert ((r > 0) & (r < 1)).all()


def test_ratios_are_concatenated_not_interleaved():
    F = np.array([[500.0, 600.0], [1500.0, 1800.0], [2500.0, 2400.0]])  # rows F1, F2, F3
    expect = npa(np.array([2500 / 1500, 2400 / 1800, 1500 / 500, 1800 / 600, 2500 / 500, 2400 / 600]))
    assert np.allclose(tfrv(F, 6), expect)
    assert np.allclose(bfrv(F, 4), expect[:4])


def test_ratios_are_scale_invariant():
    """The point of formant ratios: a uniform shift in vocal-tract size cancels."""
    F = np.array([[400.0, 700.0, 300.0], [1900.0, 1200.0, 2200.0], [2600.0, 2500.0, 2900.0]])
    assert np.allclose(tfrv(F), tfrv(1.2 * F))
