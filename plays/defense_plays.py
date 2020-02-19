from enums import DefensiveAssignments
from plays.defense_formation import FOUR_THREE, FOUR_FOUR, THREE_FOUR, DIME, NICKEL


# Ordering is DL, LB, CB, SF going left to right, always from offense viewpoint (make Plays a parent?)
class DefensePlays:
    def __init__(self, formation, assignments):
        self._formation = formation
        self._assignments = assignments

    @property
    def formation(self):
        return self._formation


DEF_PLAY_LIST = {"Cover2Man": DefensePlays(FOUR_THREE,
                                           [DefensiveAssignments.LEFT_RUSH, DefensiveAssignments.CENTER_RUSH,
                                            DefensiveAssignments.CENTER_RUSH, DefensiveAssignments.RIGHT_RUSH,
                                            DefensiveAssignments.MAN_3, DefensiveAssignments.MAN_5,
                                            DefensiveAssignments.MAN_4, DefensiveAssignments.MAN_1,
                                            DefensiveAssignments.MAN_2, DefensiveAssignments.LONG_LEFT_COVER,
                                            DefensiveAssignments.LONG_RIGHT_COVER])}
