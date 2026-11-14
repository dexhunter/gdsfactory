"""Baseline for path.smooth on a long manhattan meander.

350 corners at a fixed radius is a delay-line style waypoint path. Every
corner is a +/-90 degree euler bend, which is the default smooth bend.
"""

from __future__ import annotations

import hashlib

import gdsfactory as gf

from timing import measure, report


def meander(corners: int = 350) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = [(0.0, 0.0)]
    x = 0.0
    y = 0.0
    for index in range(corners):
        y = 40.0 if index % 2 == 0 else 0.0
        points.append((x, y))
        x += 40.0
        points.append((x, y))
    return points


def main() -> None:
    gf.gpdk.PDK.activate()
    points = meander()

    def run():
        return gf.path.smooth(points, radius=8)

    samples, path = measure(run)
    digest = hashlib.sha256(path.points.tobytes()).hexdigest()[:16]
    report(
        "smooth",
        samples,
        f"{len(path.points)}:{path.start_angle}:{path.end_angle}:{digest}",
    )


if __name__ == "__main__":
    main()
