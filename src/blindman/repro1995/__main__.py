"""``python -m blindman.repro1995``: reproduce Chapter 6 and compare with the thesis."""

from __future__ import annotations

import argparse
import json
import platform
import sys

import numpy as np

from .experiments import TESTS, run_all, targets


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", help="write the full results, with confusion matrices, here")
    ap.add_argument("--seed", type=int, default=1995, help="backprop initial-weight seed")
    args = ap.parse_args(argv)

    results = run_all(seed=args.seed)
    thesis = targets()["tables"]
    print(f"{'Table':<12} {'Recognizer':<13} {'Repr':<5} {'Prot':<4} {'Channel':<11}"
          f" {'Thesis':>14} {'Port':>14} {'Diff':>6}")
    for r in results:
        t = thesis.get(r["table"])
        printed = f"{t['correct']}/{t['total']} {t['rate']:5.1f}%" if t else "not tested"
        port = f"{r['correct']}/{r['total']} {r['rate']:5.1f}%"
        diff = f"{r['rate'] - t['rate']:+5.1f}" if t else ""
        print(f"{r['table']:<12} {r['recognizer']:<13} {r['representation']:<5} {r['protocol']:<4}"
              f" {r['channel']:<11} {printed:>14} {port:>14} {diff:>6}")
    if args.json:
        with open(args.json, "w") as f:
            env = {"python": platform.python_version(), "numpy": np.__version__,
                   "platform": platform.platform(), "machine": platform.machine()}
            json.dump({"seed": args.seed, "environment": env, "results": results}, f, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
