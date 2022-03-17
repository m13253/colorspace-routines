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

- `coords.py`: Defines RGB, XYZ, xyY, xy.
- `gammas.py`: Defines EOTF (gamma function) and OETF (inverse gamma function).
- `primaries.py`: Relative colorimetric conversion between RGB-based color spaces (sRGB, P3, BT.2020, ACES).
- `whites.py`: Relative colorimetric conversion between white points (aka. chromatic adaptation).

## Example usage

```python
>>> from mpmath import mp
>>> mp.prec = 64  # Set precision in bits, see below
>>>
>>> from primaries import *
>>> RGB_to_RGB(sRGB, ACES2065_1)
matrix(
[['0.439632981919491366', '0.382988698151553879', '0.177378319928954755'],
 ['0.0897764429588423266', '0.813439428748980621', '0.0967841282921770527'],
 ['0.0175411703831727361', '0.111546553302387013', '0.870912276314440251']])
>>>
>>> RGB_to_RGB(DisplayP3, BT_2020)
matrix(
[['0.75383303436172182', '0.198597369052616304', '0.0475695965856618765'],
 ['0.0457438489653583301', '0.941777219811693547', '0.0124789312229481225'],
 ['-0.00121034035451832443', '0.0176017173010898941', '0.98360862305342843']])
```

## Missing features

There is no support for LAB colorspaces (CIELAB, [Oklab](https://bottosson.github.io/posts/oklab/)) because:
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
code into your own software, feel free to lower the precision to 53-bit,
32-bit, or even 24-bit.

Note: Code in `gammas.py` uses standard 53-bit precision only, in order to be
compatible with `numpy`.
