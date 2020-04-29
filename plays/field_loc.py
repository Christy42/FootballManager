from math import sqrt

from enums import Depth, Side


class FieldLocation:
    def __init__(self, depth: Depth, side: Side, yards: int):
        self._depth = depth
        self._side = side
        self._yards = yards

    @property
    def yards(self):
        return self._yards

    @property
    def depth(self):
        return self._depth

    @property
    def side(self):
        return self._side

    def distance(self, location) -> float:
        return sqrt((self.depth.value - location.depth.value) ** 2 + (self.side.value - location.side.value) ** 2)


# All done from offense point of view
# Back -5 -> 0, SHORT 1 -> 5, MID 6 -> 10, LONG 11 -> 15, FAR 16 -> 20, DEEP -> 21 - 25
BACK_RIGHT = FieldLocation(Depth.BACK, Side.RIGHT, -2)
BACK_CENT_R = FieldLocation(Depth.BACK, Side.CENT_R, -2)
BACK_CENTER = FieldLocation(Depth.BACK, Side.CENTER, -2)
BACK_CENT_L = FieldLocation(Depth.BACK, Side.CENT_L, -2)
BACK_LEFT = FieldLocation(Depth.BACK, Side.LEFT, -2)
SHORT_RIGHT = FieldLocation(Depth.SHORT, Side.RIGHT, 3)
SHORT_CENT_R = FieldLocation(Depth.SHORT, Side.CENT_R, 3)
SHORT_CENTER = FieldLocation(Depth.SHORT, Side.CENTER, 3)
SHORT_CENT_L = FieldLocation(Depth.SHORT, Side.CENT_L, 3)
SHORT_LEFT = FieldLocation(Depth.SHORT, Side.LEFT, 3)
MID_RIGHT = FieldLocation(Depth.MID, Side.RIGHT, 8)
MID_CENT_R = FieldLocation(Depth.MID, Side.CENT_R, 8)
MID_CENTER = FieldLocation(Depth.MID, Side.CENTER, 8)
MID_CENT_L = FieldLocation(Depth.MID, Side.CENT_L, 8)
MID_LEFT = FieldLocation(Depth.MID, Side.LEFT, 8)
LONG_RIGHT = FieldLocation(Depth.LONG, Side.RIGHT, 13)
LONG_CENT_R = FieldLocation(Depth.LONG, Side.CENT_R, 13)
LONG_CENTER = FieldLocation(Depth.LONG, Side.CENTER, 13)
LONG_CENT_L = FieldLocation(Depth.LONG, Side.CENT_L, 13)
LONG_LEFT = FieldLocation(Depth.LONG, Side.LEFT, 13)
FAR_RIGHT = FieldLocation(Depth.FAR, Side.RIGHT, 18)
FAR_CENT_R = FieldLocation(Depth.FAR, Side.CENT_R, 18)
FAR_CENTER = FieldLocation(Depth.FAR, Side.CENTER, 18)
FAR_CENT_L = FieldLocation(Depth.FAR, Side.CENT_L, 18)
FAR_LEFT = FieldLocation(Depth.FAR, Side.LEFT, 18)
DEEP_RIGHT = FieldLocation(Depth.DEEP, Side.RIGHT, 23)
DEEP_CENT_R = FieldLocation(Depth.DEEP, Side.CENT_R, 23)
DEEP_CENTER = FieldLocation(Depth.DEEP, Side.CENTER, 23)
DEEP_CENT_L = FieldLocation(Depth.DEEP, Side.CENT_L, 23)
DEEP_LEFT = FieldLocation(Depth.DEEP, Side.LEFT, 23)
