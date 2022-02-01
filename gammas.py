import numpy as np


# https://www.itu.int/rec/R-REC-BT.2100
def HLG_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for HLG.

    Input range is [0, 12] (ARIB STD-B67). If your input is in range [0, 1], multiply by 12.
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    r = 0.5
    a = 0.17883277
    b = 1 - 4 * a
    c = 0.5 - a * np.log(4 * a)
    buf_abs = np.abs(buf)
    return np.where(buf_abs <= 1, r * np.sqrt(buf_abs), a * np.log(buf_abs - b) + c) * np.sign(buf)


# https://www.itu.int/rec/R-REC-BT.2100
def HLG_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for HLG.

    Input range is [0, 1].
    Output range is [0, 12] (ARIB STD-B67). If you want to convert to [0, 1], divide by 12.

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    r = 0.5
    a = 0.17883277
    b = 1 - 4 * a
    c = 0.5 - a * np.log(4 * a)
    buf_abs = np.abs(buf)
    return np.where(buf_abs <= r, np.square(buf_abs / r), np.exp((buf_abs - c) / a) + b) * np.sign(buf)


# https://scholarworks.rit.edu/theses/2858/
def IPT_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for IPT.

    Input range is [0, 1].
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    buf_abs = np.abs(buf)
    return buf_abs**0.43 * np.sign(buf)


# https://scholarworks.rit.edu/theses/2858/
def IPT_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for IPT.

    Input range is [0, 1].
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    buf_abs = np.abs(buf)
    return buf_abs**(1 / 0.43) * np.sign(buf)


# http://cie.co.at/publications/colorimetry-part-4-cie-1976-lab-colour-space-1
def Lstar_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for L* (CIE L*a*b*).

    Input range is [0, 100].
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    delta = 6 / 29
    buf_abs = np.abs(buf)
    f = (buf_abs + 16) / 116
    return np.where(f <= delta, (f - 4 / 29) * (3 * np.square(delta)), f**3) * np.sign(buf)


# http://cie.co.at/publications/colorimetry-part-4-cie-1976-lab-colour-space-1
def Lstar_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for L* (CIE L*a*b*).

    Input range is [0, 1].
    Output range is [0, 100].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    delta = 6 / 29
    buf_abs = np.abs(buf)
    f = np.where(buf_abs <= delta**3, buf_abs / (3 * np.square(delta)) + 4 / 29, np.cbrt(buf_abs))
    return (116 * f - 16) * np.sign(buf)


# https://bottosson.github.io/posts/oklab/
def Oklab_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for Oklab.

    Input range is [0, 1].
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    return np.cbrt(buf)


# https://bottosson.github.io/posts/oklab/
def Oklab_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for Oklab.

    Input range is [0, 1].
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    return buf**3


# https://www.itu.int/rec/R-REC-BT.2100
def PQ_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for PQ (SMPTE ST 2084).

    Input range is [0, 10000], in unit cd/m^2.
    Output range is [0, 1].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    m1 = 2610 / 16384
    m2 = 2523 / 4096 * 128
    c1 = 3424 / 4096
    c2 = 2413 / 4096 * 32
    c3 = 2392 / 4096 * 32
    Y = np.abs(buf) / 10000
    return ((c1 + c2 * Y**m1) / (1 + c3 * Y**m1))**m2 * np.sign(buf)


# https://www.itu.int/rec/R-REC-BT.2100
def PQ_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for PQ (SMPTE ST 2084).

    Output range is [0, 1].
    Input range is [0, 10000], in unit cd/m^2.

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    m1 = 2610 / 16384
    m2 = 2523 / 4096 * 128
    c1 = 3424 / 4096
    c2 = 2413 / 4096 * 32
    c3 = 2392 / 4096 * 32
    buf_abs = np.abs(buf)
    return 10000 * (np.maximum(buf_abs**(1 / m2) - c1, 0) / (c2 - c3 * buf_abs**(1 / m2)))**(1 / m1) * np.sign(buf)


# https://www.w3.org/TR/css-color-4/#color-conversion-code
def sRGB_OETF(buf: np.ndarray) -> np.ndarray:
    '''
    OETF curve for scRGB, sRGB, Display P3, etc.

    For sRGB and Display P3, input range is [0, 1], output range is [0, 1].
    For scRGB, input range is [-0.5, 7.5], output range is [-0.7353569830524495, 2.387650431415108].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    buf_abs = np.abs(buf)
    return np.where(buf_abs <= 0.0031308, 12.92 * buf_abs, 1.055 * buf_abs**(1 / 2.4) - 0.055) * np.sign(buf)


# https://www.w3.org/TR/css-color-4/#color-conversion-code
def sRGB_EOTF(buf: np.ndarray) -> np.ndarray:
    '''
    EOTF curve for scRGB, sRGB, Display P3, etc.

    For sRGB and Display P3, input range is [0, 1], output range is [0, 1].
    For scRGB, input range is [-0.7353569830524495, 2.387650431415108], output range is [-0.5, 7.5].

    In case of negative input, the function takes its absolute value and returns the negative output.
    '''
    buf_abs = np.abs(buf)
    return np.where(buf_abs <= 0.04045, buf_abs / 12.92, ((buf_abs + 0.055) / 1.055)**2.4) * np.sign(buf)
