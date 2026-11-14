"""Shared timing for intake benchmarks.

Samples are wall time around one call of the target function. The first call
is a warmup and is not recorded. Noise is the full min-to-max spread as a
percentage of the median.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any


def measure(fn: Callable[[], Any], repeats: int = 5) -> tuple[list[float], Any]:
    fn()
    samples_ms: list[float] = []
    result: Any = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn()
        samples_ms.append((time.perf_counter() - start) * 1000.0)
    return samples_ms, result


def report(name: str, samples_ms: list[float], checksum: str) -> None:
    ordered = sorted(samples_ms)
    median = ordered[len(ordered) // 2]
    noise_pct = (ordered[-1] - ordered[0]) / median * 100.0
    payload = {
        "name": name,
        "repeats": len(samples_ms),
        "baseline_median_ms": round(median, 3),
        "baseline_noise_pct": round(noise_pct, 3),
        "min_ms": round(ordered[0], 3),
        "max_ms": round(ordered[-1], 3),
        "samples_ms": [round(sample, 3) for sample in samples_ms],
        "checksum": checksum,
    }
    print(json.dumps(payload, sort_keys=True))
