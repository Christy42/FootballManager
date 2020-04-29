from enums import OffenseFormation, PlayStyle, Side, OffAssign, RunStyle, GenericOff
from plays.offense_formation import SPREAD, SINGLEBACK, SHOTGUN, DOUBLE_TE_SET, I_FORM, KICK_OFF
from plays.route import DRIVE_SINGLEBACK

# Ordering (changes slightly depending on formation, RB, TEs go in for later WRs
# OT, OG, C, OG, OT, WR1, WR2, WR3, WR4, RB1, QB
# OT, OG, C, OG, OT, WR1, WR2, WR3, RB1, TE1, QB
# K ......


class OffensePlay:
    def __init__(self, formation, style, assignments, direction, runner, name, com_name, block_style, route=None):
        self._assignments = {GenericOff.OT_L: assignments[0], GenericOff.OG_L: assignments[1],
                             GenericOff.C: assignments[2], GenericOff.OG_R: assignments[3],
                             GenericOff.OT_R: assignments[4], GenericOff.REC1: assignments[5],
                             GenericOff.REC2: assignments[6], GenericOff.REC3: assignments[7],
                             GenericOff.REC4: assignments[8], GenericOff.REC5: assignments[9],
                             GenericOff.QB: assignments[10]}
        self._direction = direction
        self._runner = 0
        self._formation = formation
        self._name = name
        self._commentary_name = com_name
        self._runner = runner
        self._style = style
        self._block_style = block_style
        self._route = route

    @property
    def formation(self):
        return self._formation

    @property
    def name(self):
        return self._name

    @property
    def side(self):
        return self._direction

    @property
    def runner(self):
        return self._runner

    @property
    def assignments(self):
        return self._assignments

    @property
    def style(self):
        return self._style

    @property
    def block_style(self):
        return self._block_style

# This system of assigning players on a list seems badly thought out.  OL_1->OL_5 maybe???
# Or just have blocking style fill it all in really?  I guess some routes will have blocking info but just go through
# Seems much much cleaner.  Even if there is only one or two blocking styles.  Think on it


OFF_PLAY_LIST = {"ManCenterRun": OffensePlay(SINGLEBACK, PlayStyle.RUN,
                                             [OffAssign.LEFT_BLOCK, OffAssign.CENTER_BLOCK,
                                              OffAssign.CENTER_BLOCK, OffAssign.CENTER_BLOCK,
                                              OffAssign.RIGHT_BLOCK, OffAssign.ROUTE_RUNNING,
                                              OffAssign.ROUTE_RUNNING, OffAssign.ROUTE_RUNNING,
                                              OffAssign.RUNNING, OffAssign.RIGHT_BLOCK,
                                              OffAssign.QB], Side.CENTER, GenericOff.REC4, "Man Center Run",
                                             "Man Center Run", RunStyle.MAN),
                 "DriveSingleback": OffensePlay(SINGLEBACK, PlayStyle.PASS,
                                         [OffAssign.LEFT_BLOCK, OffAssign.CENTER_BLOCK,
                                          OffAssign.CENTER_BLOCK, OffAssign.CENTER_BLOCK,
                                          OffAssign.RIGHT_BLOCK, OffAssign.ROUTE_RUNNING,
                                          OffAssign.ROUTE_RUNNING, OffAssign.ROUTE_RUNNING,
                                          OffAssign.SCAN_BLOCK, OffAssign.ROUTE_RUNNING,
                                          OffAssign.QB], Side.CENTER, GenericOff.REC4, "Man Center Run",
                                                "Man Center Run", RunStyle.MAN, route=DRIVE_SINGLEBACK),
                 "KickOff": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                        [OffAssign.LEFT_BLOCK, OffAssign.CENTER_BLOCK,
                                         OffAssign.CENTER_BLOCK, OffAssign.CENTER_BLOCK,
                                         OffAssign.RIGHT_BLOCK, OffAssign.ROUTE_RUNNING,
                                         OffAssign.ROUTE_RUNNING, OffAssign.ROUTE_RUNNING,
                                         OffAssign.RUNNING, OffAssign.RIGHT_BLOCK,
                                         OffAssign.KICK], Side.CENTER, GenericOff.REC4, "Kick Off",
                                        "Kick Off", None),
                 "Kick": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                     [OffAssign.LEFT_BLOCK, OffAssign.CENTER_BLOCK,
                                      OffAssign.CENTER_BLOCK, OffAssign.CENTER_BLOCK,
                                      OffAssign.RIGHT_BLOCK, OffAssign.ROUTE_RUNNING,
                                      OffAssign.ROUTE_RUNNING, OffAssign.ROUTE_RUNNING,
                                      OffAssign.RUNNING, OffAssign.RIGHT_BLOCK,
                                      OffAssign.KICK], Side.CENTER, GenericOff.REC4, "Kick", "Kick", None),
                 "Punt": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                     [OffAssign.LEFT_BLOCK, OffAssign.CENTER_BLOCK,
                                      OffAssign.CENTER_BLOCK, OffAssign.CENTER_BLOCK,
                                      OffAssign.RIGHT_BLOCK, OffAssign.ROUTE_RUNNING,
                                      OffAssign.ROUTE_RUNNING, OffAssign.ROUTE_RUNNING,
                                      OffAssign.RUNNING, OffAssign.RIGHT_BLOCK,
                                      OffAssign.KICK], Side.CENTER, GenericOff.REC4, "Punt", "Punt", None)
                 }
