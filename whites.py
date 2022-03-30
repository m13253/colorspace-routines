from coords import xy, XYZ
import mpmath

# D50, rounding XYZ values to 4 significant digits
# https://color.org/whyd50.xalter
PCS = XYZ('96.42', '100', '82.49')

# D50, rounding xy values to 4 significant digits
# https://www.color.org/chardata/rgb/ROMMRGB.xalter
D50 = xy('0.3457', '0.3585')

# D65, rounding xy values to 4 significant digits
# https://www.color.org/chardata/rgb/sRGB.xalter
D65 = xy('0.3127', '0.3290')

# ACES D60-like white point, not exactly D60
# https://j.mp/TB-2018-001
# https://acescentral.com/aces-documentation/
ACES = xy('0.32168', '0.33767')

# https://www.color.org/chardata/rgb/DCIP3.xalter
DCI = xy('0.3140', '0.3510')


# http://www.brucelindbloom.com/index.html?Eqn_ChromAdapt.html
def chromatic_adaptation(from_white: xy, to_white: xy) -> mpmath.matrix:
    '''
    Bradford chromatic adaptation algorithm

    import whites
    M = whites.chromatic_adaptation(whites.D65, whites.D50)
    XYZ_D50 = M * XYZ_D65
    '''

    M_A = mpmath.matrix([
        ['0.8951000', '0.2664000', '-0.1614000'],
        ['-0.7502000', '1.7135000', '0.0367000'],
        ['0.0389000', '-0.0685000', '1.0296000'],
    ])

    from_white_XYZ = from_white.to_XYZ()
    to_white_XYZ = to_white.to_XYZ()
    from_cone_response = M_A * from_white_XYZ.to_matrix()
    to_cone_response = M_A * to_white_XYZ.to_matrix()
    scale_cone_response = mpmath.matrix([
        [to_cone_response[0] / from_cone_response[0], '0', '0'],
        ['0', to_cone_response[1] / from_cone_response[1], '0'],
        ['0', '0', to_cone_response[2] / from_cone_response[2]],
    ])
    M = mpmath.inverse(M_A) * scale_cone_response * M_A

    return M
