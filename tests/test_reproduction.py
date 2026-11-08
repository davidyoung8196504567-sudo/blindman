"""The Chapter 6 reproduction. This is the score gate CI runs on every change.

Expectations differ by test, for the reasons in docs/PHASE0.md:
- Fuzzy ARTMAP is deterministic, so where the data survived complete the
  confusion matrix must match the thesis cell for cell.
- Two microphone speaker-dependent tables match in total but move the same
  two phrase-7 test files from column 3 to column 2 (open item).
- The telephone speaker-dependent tests lost 9 test files, so only the rate
  is compared.
- Backprop's 1995 starting weights are lost; with the fixed seed it must land
  within 4 points of the thesis. The bound is the spread observed over nine
  seeds (largest deviation 3.2 points), not a claim about the thesis: a
  different BLAS library can change the training trajectory as a new seed
  would.
"""

import numpy as np
import pytest

from blindman.repro1995.experiments import TESTS, run_all, targets

pytestmark = pytest.mark.slow

EXACT = {"6.4-M", "6.4-T", "6.6-M", "6.6-T"}
SAME_TOTAL = {"6.3-M": 2, "6.5-M": 1}  # table -> phrase-7 files moved from column 3 to 2
TELEPHONE_SD = {"6.3-T", "6.5-T"}
BACKPROP = {"6.1", "6.2"}


@pytest.fixture(scope="module")
def results():
    return {r["table"]: r for r in run_all()}


def test_every_test_ran(results):
    assert set(results) == {t.table for t in TESTS}
    assert all(r["unrecognized"] == 0 for r in results.values())  # the thesis tables have no such column


@pytest.mark.parametrize("table", sorted(EXACT))
def test_fuzzy_artmap_reproduces_cell_for_cell(results, table):
    assert results[table]["confusion"] == targets()["tables"][table]["confusion"]


@pytest.mark.parametrize("table", sorted(SAME_TOTAL))
def test_fuzzy_artmap_same_total_known_difference(results, table):
    thesis = np.array(targets()["tables"][table]["confusion"])
    port = np.array(results[table]["confusion"])
    moved = SAME_TOTAL[table]
    expected = thesis.copy()
    expected[5, 0] += moved  # row = spoken phrase 7, col 0 = phrase 2
    expected[5, 1] -= moved  # col 1 = phrase 3
    assert np.array_equal(port, expected)


@pytest.mark.parametrize("table", sorted(TELEPHONE_SD))
def test_telephone_speaker_dependent_rate(results, table):
    assert results[table]["total"] == 615
    assert abs(results[table]["rate"] - targets()["tables"][table]["rate"]) <= 1.0


@pytest.mark.parametrize("table", sorted(BACKPROP))
def test_backprop_benchmark_within_seed_spread(results, table):
    assert abs(results[table]["rate"] - targets()["tables"][table]["rate"]) <= 4.0
