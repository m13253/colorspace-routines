# colorspace-routines

This repository contains a collection of routines for you to compute matrices
to convert between different color spaces.

Matrices from Wikipedia may not always be accurate, since they may suffer from
multiple round-off errors.

## Licensing

The sources of the algorithms, constants, coefficients, and formulas are noted
in the program code. Unless restricted by applicable low, the source code in
this repository is released to the **Public Domain**.

Feel free to copy-paste my code into yours, or rewrite it into your favorite
programming language. I would be very happy if every piece of software in the
world can use the correct formula to calculate colors and be free from
forgetting to perform gamma-correction.

## Contents

- coords.py: Defines RGB, XYZ, xyY, xy.
- gammas.py: Defines EOTF (gamma function) and OETF (inverse gamma function).
- primaries.py: Relative colorimetric conversion between RGB-based color spaces (sRGB, P3, BT.2020, ACES).
- whites.py: Relative colorimetric conversion between white points (aka. chromatic adaptation).

## Precision

Most code in this repository relies on [mpmath](https://mpmath.org) to perform
arbitrary-precision floating point calculations. Refer to its documentation to
learn how to set the precision prior to calculation.

This is because the common usage of this repository is to generate a conversion
matrix, and you want to minimize round-off errors. If you need to copy-paste my
code into your own software, feel free to lower the precision to 64-bit or even
32-bit.
