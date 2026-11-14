"""Baseline for functions.get_polygons_points on curved polygons.

Matches the repository's complex-polygon layout benchmark: 50 outlines of
about 10k vertices, the shape of a ring or spiral boundary after extrusion.
"""

from __future__ import annotations

import hashlib
import math

import numpy as np

import gdsfactory as gf
from gdsfactory.functions import get_polygons_points

from timing import measure, report


def build_component() -> gf.Component:
    gf.gpdk.PDK.activate()
    component = gf.Component()
    count = 50
    npoints = 10_000
    theta = np.linspace(0, 2 * np.pi, npoints, endpoint=False)
    radius = 1 + 0.05 * np.sin(17 * theta) + 0.02 * np.sin(41 * theta)
    unit = np.column_stack((radius * np.cos(theta), radius * np.sin(theta)))
    columns = math.ceil(math.sqrt(count))
    for index in range(count):
        polygon = unit * (10.0 + (index % 5))
        polygon = polygon.copy()
        polygon[:, 0] += (index % columns) * 40.0
        polygon[:, 1] += (index // columns) * 40.0
        component.add_polygon(polygon, layer=(1, 0))
    return component


def main() -> None:
    component = build_component()

    def run():
        return get_polygons_points(component, by="tuple", layers=((1, 0),))

    samples, points = measure(run)
    arrays = points[(1, 0)]
    digest = hashlib.sha256(b"".join(array.tobytes() for array in arrays)).hexdigest()
    report(
        "get_polygons_points",
        samples,
        f"{len(arrays)}:{arrays[0].shape[0]}:{digest[:16]}",
    )


if __name__ == "__main__":
    main()
