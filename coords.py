from typing_extensions import Self
import mpmath
from mpmath import mpf


class RGB:

    def __init__(self, R: mpf, G: mpf, B: mpf) -> None:
        self.R = mpf(R)
        self.G = mpf(G)
        self.B = mpf(B)

    def __repr__(self) -> str:
        return f"RGB({self.R}, {self.G}, {self.B})"

    def to_matrix(self) -> mpmath.matrix:
        return mpmath.matrix([self.R, self.G, self.B])

    def to_RGB(self) -> Self:
        return self


class XYZ:

    def __init__(self, X: mpf, Y: mpf, Z: mpf) -> None:
        self.X = mpf(X)
        self.Y = mpf(Y)
        self.Z = mpf(Z)

    def __repr__(self) -> str:
        return f"XYZ({self.X}, {self.Y}, {self.Z})"

    def to_matrix(self) -> mpmath.matrix:
        return mpmath.matrix([self.X, self.Y, self.Z])

    def to_XYZ(self) -> Self:
        return self

    def to_xy(self) -> 'xy':
        sum_XYZ = self.X + self.Y + self.Z
        x = self.X / sum_XYZ
        y = self.Y / sum_XYZ
        return xy(x, y)

    def to_xyY(self) -> 'xyY':
        sum_XYZ = self.X + self.Y + self.Z
        x = self.X / sum_XYZ
        y = self.Y / sum_XYZ
        Y = self.Y
        return xyY(x, y, Y)


class xy:

    def __init__(self, x: mpf, y: mpf) -> None:
        self.x = mpf(x)
        self.y = mpf(y)

    def __repr__(self) -> str:
        return f"xy({self.x}, {self.y})"

    def to_matrix(self) -> mpmath.matrix:
        return mpmath.matrix([self.x, self.y])

    def to_XYZ(self, Y: mpf = 1) -> 'XYZ':
        X = self.x * Y / self.y
        Z = (1 - self.x - self.y) * Y / self.y
        return XYZ(X, Y, Z)

    def to_xy(self) -> Self:
        return self

    def to_xyY(self, Y: mpf = 1) -> 'xyY':
        return xyY(self.x, self.y, Y)


class xyY:

    def __init__(self, x: mpf, y: mpf, Y: mpf) -> None:
        self.x = mpf(x)
        self.y = mpf(y)
        self.Y = mpf(Y)

    def __repr__(self) -> str:
        return f"xyY({self.x}, {self.y}, {self.Y})"

    def to_XYZ(self) -> 'XYZ':
        X = self.x * self.Y / self.y
        Y = self.Y
        Z = (1 - self.x - self.y) * self.Y / self.y
        return XYZ(X, Y, Z)

    def to_xy(self) -> 'xy':
        return xy(self.x, self.y)

    def to_xyY(self) -> Self:
        return self
