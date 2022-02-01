from coords import xy
import whites
import mpmath


class Primaries:
    '''
    A set of primary colors (red, green, blue) and a white point for an RGB based color space.
    '''

    def __init__(self, R: xy, G: xy, B: xy, W: xy):
        self.R = R
        self.G = G
        self.B = B
        self.W = W


# http://j.mp/TB-2014-004
# https://acescentral.com/aces-documentation/
ACES2065_1 = Primaries(
    R=xy('0.73470', '0.26530'),
    G=xy('0.00000', '1.00000'),
    B=xy('0.00010', '-0.07700'),
    W=whites.ACES,
)
# http://j.mp/S-2014-004
# https://acescentral.com/aces-documentation/
ACEScg = Primaries(
    R=xy('0.713', '0.293'),
    G=xy('0.165', '0.830'),
    B=xy('0.128', '0.044'),
    W=whites.ACES,
)
# https://www.itu.int/rec/R-REC-BT.2020/en
BT_2020 = Primaries(
    R=xy('0.708', '0.292'),
    G=xy('0.170', '0.797'),
    B=xy('0.131', '0.046'),
    W=whites.D65,
)
# https://www.color.org/chardata/rgb/DCIP3.xalter
DCI_P3 = Primaries(
    R=xy('0.680', '0.320'),
    G=xy('0.265', '0.690'),
    B=xy('0.150', '0.060'),
    W=whites.DCI,
)
# https://www.color.org/chardata/rgb/DCIP3.xalter
DisplayP3 = Primaries(
    R=xy('0.680', '0.320'),
    G=xy('0.265', '0.690'),
    B=xy('0.150', '0.060'),
    W=whites.D65,
)
# https://www.color.org/chardata/rgb/sRGB.xalter
sRGB = Primaries(
    R=xy('0.64', '0.33'),
    G=xy('0.30', '0.60'),
    B=xy('0.15', '0.06'),
    W=whites.D65,
)


# http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
def RGB_to_XYZ(rgb: Primaries) -> mpmath.matrix:
    '''
    Convert linear RGB to chromatic-adapted XYZ

    import primaries
    M = primaries.RGB_to_XYZ(primaries.sRGB)
    XYZ_D65 = M * sRGB_linear
    '''
    R_XYZ = rgb.R.to_XYZ()
    G_XYZ = rgb.G.to_XYZ()
    B_XYZ = rgb.B.to_XYZ()
    W_XYZ = rgb.W.to_XYZ()
    S = mpmath.inverse(mpmath.matrix([
        [R_XYZ.X, G_XYZ.X, B_XYZ.X],
        [R_XYZ.Y, G_XYZ.Y, B_XYZ.Y],
        [R_XYZ.Z, G_XYZ.Z, B_XYZ.Z],
    ])) * W_XYZ.to_matrix()
    M = mpmath.matrix([
        [S[0] * R_XYZ.X, S[1] * G_XYZ.X, S[2] * B_XYZ.X],
        [S[0] * R_XYZ.Y, S[1] * G_XYZ.Y, S[2] * B_XYZ.Y],
        [S[0] * R_XYZ.Z, S[1] * G_XYZ.Z, S[2] * B_XYZ.Z],
    ])

    return M


def RGB_to_RGB(from_rgb: Primaries, to_rgb: Primaries) -> mpmath.matrix:
    '''
    Convert one linear RGB to another linear RGB

    import primaries
    M = primaries.RGB_to_RGB(primaries.sRGB, primaries.BT_2020)
    BT_2020_linear = M * sRGB_linear
    '''

    M_1 = RGB_to_XYZ(from_rgb)
    if from_rgb.W != to_rgb.W:
        M_A = whites.chromatic_adaptation(from_rgb.W, to_rgb.W)
    else:
        M_A = 1
    M_2 = XYZ_to_RGB(to_rgb)

    return M_2 * M_A * M_1


def XYZ_to_RGB(rgb: Primaries) -> mpmath.matrix:
    '''
    Convert chromatic-adapted XYZ to linear RGB

    import primaries
    M_inv = primaries.XYZ_to_RGB(primaries.sRGB)
    sRGB_linear = M_inv * XYZ_D65
    '''
    return mpmath.inverse(RGB_to_XYZ(rgb))
