"""Fuzzy ARTMAP as written in FARTMAPT.M (Annex E), not the textbook variant.

Differences from textbook Fuzzy ARTMAP that the port keeps:
- **Fast learning with no recoding:** a committed category's weights never
  change. A new category is set equal to its founding input.
- **Training vigilance 1.0, testing vigilance 0.5.**
- **The search accepts the last active node** whatever its similarity
  (``if similarity < vigilance & active_nodes > 1``).
- **Match tracking** raises vigilance to ``1.00000000000001 * similarity``.
- **Testing never learns.** If the search settles on the uncommitted node,
  the input is UNRECOGNIZED.
- The weight matrix grows by 20 spare (all-ones) rows whenever fewer than 2
  spares remain. The spares matter only to the backprop benchmark, which
  trains on the whole weight matrix (BPMAPPER.M).
"""

from __future__ import annotations

import numpy as np

CHOICE_PARAMETER = 0.001
TRAIN_VIGILANCE = 1.00
TEST_VIGILANCE = 0.50
MATCH_TRACKING_FACTOR = 1.00000000000001
UNRECOGNIZED = None


class FuzzyARTMAP:
    def __init__(self, feature_length: int):
        self.M = 2 * feature_length  # complement coding doubles the input
        self.N = 10
        self.W = np.ones((self.N, self.M))
        self.committed = 0  # max_cluster_number
        self.labels: list = []  # SIM: the phrase each committed category maps to

    @staticmethod
    def complement(x: np.ndarray) -> np.ndarray:
        return np.concatenate([x, 1.0 - x])

    def _search(self, I: np.ndarray, vigilance: float, label=None) -> tuple[int, float]:
        """Hypothesis testing over the committed nodes plus one uncommitted node."""
        active_W = self.W[: self.committed + 1]
        overlap = np.minimum(active_W, I).sum(axis=1)
        T = overlap / (CHOICE_PARAMETER + active_W.sum(axis=1))
        sum_I = I.sum()
        active = self.committed + 1
        guard = 0
        while True:  # MatchTracking
            while True:  # cluster_search
                j = int(np.argmax(T))  # lowest index wins a tie, as in MATLAB
                similarity = overlap[j] / sum_I
                if similarity < vigilance and active > 1:
                    T[j] = 0.0
                    active -= 1
                else:
                    break
            if label is None:  # testing: no match tracking
                return j, similarity
            if j < self.committed and self.labels[j] == label:
                return j, similarity
            if j >= self.committed:
                return j, similarity
            vigilance = MATCH_TRACKING_FACTOR * similarity
            guard += 1
            if guard > 10 * (self.committed + 1):
                raise RuntimeError("match tracking did not terminate")

    def train(self, x: np.ndarray, label) -> None:
        I = self.complement(x)
        j, _ = self._search(I, TRAIN_VIGILANCE, label)
        if j >= self.committed:  # new category, centred on the input
            self.W[j] = I
            self.labels.append(label)
            self.committed += 1
            if self.N - self.committed < 2:
                self.N += 20
                self.W = np.vstack([self.W, np.ones((20, self.M))])

    def predict(self, x: np.ndarray):
        """The phrase label, or UNRECOGNIZED. Also returns the similarity."""
        I = self.complement(x)
        j, similarity = self._search(I, TEST_VIGILANCE)
        if j >= self.committed:
            return UNRECOGNIZED, similarity
        return self.labels[j], similarity
