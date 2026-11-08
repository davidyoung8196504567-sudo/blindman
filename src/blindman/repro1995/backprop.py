"""The benchmark network, ported from BPMAPPER.M (Annex F) and BPTESTER.M (Annex G).

A two-layer network: tan-sigmoid hidden layer of 50 nodes, linear output
layer of 8 nodes (one per phrase), batch backpropagation with momentum and an
adaptive learning rate. The toolbox functions it used (``tansig``,
``purelin``, ``deltatan``, ``deltalin``, ``learnbpm``, ``nwtan``) are
re-implemented here from their definitions; no toolbox code is copied.

Two things did not survive and are reconstructed:
- **Initial weights.** BPMAPPER.M loads hand-picked Nguyen-Widrow weights
  (``bpinit.mat``) and then a previously trained network (``bprtmapt.mat``).
  Both files are lost, so the port draws Nguyen-Widrow weights from a seed.
- **Epoch limit.** §6.2.2 says 1000 epochs; the code (and Annex F) says
  ``me = 900``. The port follows the code.

As in BPMAPPER.M, the training inputs are the Fuzzy ARTMAP weight matrix
with the complement half removed: the committed templates (equal to the
training vectors under fast learning) **plus the spare all-ones rows**,
whose target is all zeros.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .fuzzy_artmap import FuzzyARTMAP

HIDDEN = 50
MAX_EPOCHS = 900  # me
ERROR_GOAL = 0.1  # eg, on the sum squared error
LR = 0.0001  # lr
LR_INC = 1.05  # im
LR_DEC = 0.7  # dm
MOMENTUM = 0.95  # mc
ERROR_RATIO = 1.04  # er


def nguyen_widrow(s: int, r: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Nguyen-Widrow initial weights for a tan-sigmoid layer, inputs in [-1, 1]."""
    magw = 0.7 * s ** (1.0 / r)
    w = rng.uniform(-1, 1, (s, r))
    w = magw * w / np.linalg.norm(w, axis=1, keepdims=True)
    b = magw * rng.uniform(-1, 1, (s, 1))
    return w, b


@dataclass
class Backprop:
    phrases: tuple
    seed: int = 1995
    max_epochs: int = MAX_EPOCHS
    W1: np.ndarray = field(init=False, repr=False)
    B1: np.ndarray = field(init=False, repr=False)
    W2: np.ndarray = field(init=False, repr=False)
    B2: np.ndarray = field(init=False, repr=False)
    epochs: int = field(init=False, default=0)
    sse: float = field(init=False, default=np.nan)

    def fit_from_artmap(self, net: FuzzyARTMAP) -> "Backprop":
        half = net.M // 2
        P = net.W[:, :half].T  # columns are training vectors
        T = np.zeros((len(self.phrases), net.N))
        for col, label in enumerate(net.labels):
            T[self.phrases.index(label), col] = 1.0
        return self.fit(P, T)

    def fit(self, P: np.ndarray, T: np.ndarray) -> "Backprop":
        rng = np.random.default_rng(self.seed)
        R, Q = P.shape
        S2 = T.shape[0]
        W1, B1 = nguyen_widrow(HIDDEN, R, rng)
        W2 = rng.uniform(-1, 1, (S2, HIDDEN)) * 0.5
        B2 = rng.uniform(-1, 1, (S2, 1)) * 0.5
        dW1, dB1, dW2, dB2 = (np.zeros_like(a) for a in (W1, B1, W2, B2))
        MC, lr = 0.0, LR
        ones = np.ones((Q, 1))

        A1 = np.tanh(W1 @ P + B1)
        A2 = W2 @ A1 + B2
        E = T - A2
        SSE = float(np.sum(E**2))
        D2 = E  # deltalin
        D1 = (1 - A1**2) * (W2.T @ D2)  # deltatan

        epoch = 0
        for epoch in range(1, self.max_epochs + 1):
            if SSE < ERROR_GOAL:
                epoch -= 1
                break
            # learnbpm: dW = mc*dW + (1-mc)*lr*D*P'
            dW1 = MC * dW1 + (1 - MC) * lr * D1 @ P.T
            dB1 = MC * dB1 + (1 - MC) * lr * D1 @ ones
            dW2 = MC * dW2 + (1 - MC) * lr * D2 @ A1.T
            dB2 = MC * dB2 + (1 - MC) * lr * D2 @ ones
            MC = MOMENTUM
            TW1, TB1, TW2, TB2 = W1 + dW1, B1 + dB1, W2 + dW2, B2 + dB2
            TA1 = np.tanh(TW1 @ P + TB1)
            TA2 = TW2 @ TA1 + TB2
            TE = T - TA2
            TSSE = float(np.sum(TE**2))
            if TSSE > SSE * ERROR_RATIO:
                lr *= LR_DEC
                MC = 0.0
            else:
                if TSSE < SSE:
                    lr *= LR_INC
                W1, B1, W2, B2 = TW1, TB1, TW2, TB2
                A1, A2, E, SSE = TA1, TA2, TE, TSSE
                D2 = E
                D1 = (1 - A1**2) * (W2.T @ D2)
        self.W1, self.B1, self.W2, self.B2 = W1, B1, W2, B2
        self.epochs, self.sse = epoch, SSE
        return self

    def predict(self, x: np.ndarray):
        a2 = self.W2 @ np.tanh(self.W1 @ x[:, None] + self.B1) + self.B2
        return self.phrases[int(np.argmax(a2))]  # MAXNET
