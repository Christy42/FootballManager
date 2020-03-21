from enums import OffenseFormation, PlayStyle, Side, OffensiveAssignments, RunStyle
from plays.offense_formation import SPREAD, SINGLEBACK, SHOTGUN, DOUBLE_TE_SET, I_FORM, KICK_OFF


# Ordering (changes slightly depending on formation, RB, TEs go in for later WRs
# OT, OG, C, OG, OT, WR1, WR2, WR3, WR4, RB1, QB
# OT, OG, C, OG, OT, WR1, WR2, WR3, RB1, TE1, QB
# K ......
class OffensePlay:
    def __init__(self, formation, style, assignments, direction, runner, primary, name, com_name, block_style):
        self._assignments = assignments
        self._direction = direction
        self._runner = 0
        self._primary = primary
        self._formation = formation
        self._name = name
        self._commentary_name = com_name
        self._runner = runner
        self._style = style
        self._block_style = block_style

    @property
    def formation(self):
        return self._formation

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


OFF_PLAY_LIST = {"ManCenterRun": OffensePlay(SINGLEBACK, PlayStyle.RUN,
                                         [OffensiveAssignments.LEFT_BLOCK, OffensiveAssignments.CENTER_BLOCK,
                                          OffensiveAssignments.CENTER_BLOCK, OffensiveAssignments.CENTER_BLOCK,
                                          OffensiveAssignments.RIGHT_BLOCK, OffensiveAssignments.FADE_LEFT,
                                          OffensiveAssignments.FADE_LEFT, OffensiveAssignments.FADE_RIGHT,
                                          OffensiveAssignments.RUNNING, OffensiveAssignments.RIGHT_BLOCK,
                                          OffensiveAssignments.QB],
                                          Side.CENTER, 7, 7, "Man Center Run",
                                          "Man Center Run", RunStyle.MAN),
                 "KickOff": OffensePlay(KICK_OFF, PlayStyle.SPECIAL,
                                        [OffensiveAssignments.LEFT_BLOCK, OffensiveAssignments.CENTER_BLOCK,
                                         OffensiveAssignments.CENTER_BLOCK, OffensiveAssignments.CENTER_BLOCK,
                                         OffensiveAssignments.RIGHT_BLOCK, OffensiveAssignments.FADE_LEFT,
                                         OffensiveAssignments.FADE_LEFT, OffensiveAssignments.FADE_RIGHT,
                                         OffensiveAssignments.RUNNING, OffensiveAssignments.RIGHT_BLOCK,
                                         OffensiveAssignments.KICK], Side.CENTER, 7, 7, "Kick Off", "Kick Off",
                                        None)}
