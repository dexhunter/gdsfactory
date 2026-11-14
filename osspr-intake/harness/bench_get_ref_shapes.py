"""Baseline for boolean.get_ref_shapes on a regular instance array.

A 160 by 160 array of rectangles is the kind of fill or via field boolean
subtraction walks. The timed call is get_ref_shapes only.
"""

from __future__ import annotations

import gdsfactory as gf
from gdsfactory.boolean import get_ref_shapes

from timing import measure, report


def build_array():
    gf.gpdk.PDK.activate()
    rectangle = gf.components.rectangle(size=(2, 2), layer=(1, 0))
    parent = gf.Component()
    reference = parent.add_ref(
        rectangle, columns=160, rows=160, column_pitch=4, row_pitch=4
    )
    reference.move((7, -2))
    return reference, gf.get_layer((1, 0))


def main() -> None:
    reference, layer = build_array()

    def run():
        return get_ref_shapes(reference, layer)

    samples, region = measure(run)
    report(
        "boolean.get_ref_shapes",
        samples,
        f"{region.count()}:{region.area()}",
    )


if __name__ == "__main__":
    main()
