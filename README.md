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

## Example usage

```python
>>> from mpmath import mp
>>> mp.prec = 53  # Set precision in bits, see below
>>> from primaries import *
>>> RGB_to_RGB(sRGB, ACES2065_1)
matrix(
[['0.439632981919491', '0.382988698151554', '0.177378319928955'],
 ['0.0897764429588423', '0.813439428748981', '0.0967841282921771'],
 ['0.0175411703831727', '0.111546553302387', '0.87091227631444']])
```

## Missing features

There is no support for LAB colorspaces (CIELAB, [OkLAB](https://bottosson.github.io/posts/oklab/)) because:
- It is almost impossible to use an incorrect formula.
- The conversion cannot be expressed with a single matrix.
- You can [`import colour`](https://www.colour-science.org) to perform the conversion.

There is no support for CMYK colorspaces (FOGRA39, SWOP, etc.) because:
- CMYK is too complicated. It requires a look-up table, [Sakamoto's interpolation method](https://patents.google.com/patent/US6178007B1) and some complex formulas for calculating dot-gain.
- You might need to use [Little CMS](https://www.littlecms.com) or [Argyll CMS](http://www.argyllcms.com).

## Precision

Most code in this repository relies on [mpmath](https://mpmath.org) to perform
arbitrary-precision floating point calculations. Refer to its documentation to
learn how to set the precision prior to calculation.

This is because the common usage of this repository is to generate a conversion
matrix, and you want to minimize round-off errors. If you need to copy-paste my
code into your own software, feel free to lower the precision to 64-bit or even
32-bit.
