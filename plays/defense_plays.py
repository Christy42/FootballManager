from plays.defense_formation import FOUR_THREE, FOUR_FOUR, THREE_FOUR, DIME, NICKEL
from plays.coverage import *


# Ordering is DL, LB, CB, SF going left to right, always from offense viewpoint (make Plays a parent?)
class DefensePlays:
    def __init__(self, formation, assignments, closed, zone):
        self._formation = formation
        self._assignments = assignments
        self._closed = closed
        self._zone = zone

    @property
    def closed(self):
        return self._closed

    @property
    def zone(self):
        return self._zone

    @property
    def formation(self):
        return self._formation

    @property
    def assignments(self):
        return self._assignments


DEF_PLAY_LIST = {"Cover2Man": DefensePlays(FOUR_THREE, [LEFT_RUSH, CENTER_RUSH, CENTER_RUSH, RIGHT_RUSH, MAN_3, MAN_5,
                                                        MAN_4, MAN_1, MAN_2, LONG_CENT_L_C, LONG_CENT_R_C],
                                           closed=True, zone=True)}
