"""Baseline for functions.get_polygons on an instance array.

Same 160 by 160 rectangle field as the boolean harness. get_polygons is what
callers use to pull placed geometry back out of an array reference.
"""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.functions import get_polygons

from timing import measure, report


def build_reference():
    gf.gpdk.PDK.activate()
    rectangle = gf.components.rectangle(size=(2, 2), layer=(1, 0))
    parent = gf.Component()
    reference = parent.add_ref(
        rectangle, columns=160, rows=160, column_pitch=4, row_pitch=4
    )
    reference.move((7, -2))
    return reference


def main() -> None:
    reference = build_reference()

    def run():
        return get_polygons(reference, layers=((1, 0),), by="tuple")

    samples, polygons = measure(run)
    shapes = polygons[(1, 0)]
    first = shapes[0].bbox()
    last = shapes[-1].bbox()
    report(
        "get_polygons",
        samples,
        f"{len(shapes)}:{first.left},{first.bottom}:{last.right},{last.top}",
    )


if __name__ == "__main__":
    main()
