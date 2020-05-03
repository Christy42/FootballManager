from enums import OffenseFormation, PlayStyle, Side, RunStyle, GenOff
from plays.offense_formation import SPREAD, SINGLEBACK, SHOTGUN, DOUBLE_TE_SET, I_FORM, KICK_OFF
from plays.route import *

# Ordering (changes slightly depending on formation, RB, TEs go in for later WRs
# OT, OG, C, OG, OT, WR1, WR2, WR3, WR4, RB1, QB
# OT, OG, C, OG, OT, WR1, WR2, WR3, RB1, TE1, QB
# K ......


class OffensePlay:
    def __init__(self, formation, style, assignments: RouteCombo, direction, runner, name, com_name):
        self._direction = direction
        self._assignments = assignments
        self._formation = formation
        self._name = name
        self._commentary_name = com_name
        self._runner = runner
        self._style = style
        self._reads = self._assignments.reads

    @property
    def formation(self):
        return self._formation

    @property
    def name(self):
        return self._name

    @property
    def routes(self):
        return self._assignments

    @property
    def side(self):
        return self._direction

    @property
    def runner(self):
        return self._runner

    @property
    def assignments(self):
        return self._assignments.assignments

    @property
    def style(self):
        return self._style


# This system of assigning players on a list seems badly thought out.  OL_1->OL_5 maybe???
# Or just have blocking style fill it all in really?  I guess some routes will have blocking info but just go through
# Seems much much cleaner.  Even if there is only one or two blocking styles.  Think on it


OFF_PLAY_LIST = {"ManCenterRun": OffensePlay(SINGLEBACK, PlayStyle.RUN, CENTER_RUN, Side.CENTER, GenOff.REC4,
                                             "Man Center Run", "Man Center Run"),
                 "DriveSingleback": OffensePlay(SINGLEBACK, PlayStyle.PASS, DRIVE_SINGLEBACK, Side.CENTER, GenOff.REC4,
                                                "Singleback Drive", "Singleback Drive"),
                 "KickOff": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                        KICK_ASSIGN, Side.CENTER, GenOff.REC4, "Kick Off", "Kick Off"),
                 "Kick": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                     KICK_ASSIGN, Side.CENTER, GenOff.REC4, "Kick", "Kick"),
                 "Punt": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                     KICK_ASSIGN, Side.CENTER, GenOff.REC4, "Punt", "Punt")
                 }
