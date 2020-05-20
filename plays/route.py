from enums import GenOff
from plays.field_loc import *


class SingleRoute:
    def __init__(self, field_loc, blocking=False, qb=False, rusher=False, route=False):
        self.field_loc = field_loc
        self.blocking = blocking
        self.qb = qb
        self.rusher = rusher
        self.route = route

    @property
    def yards(self):
        return self.field_loc.yards

    @property
    def side(self):
        return self.field_loc.side

    @property
    def depth(self):
        return self.field_loc.depth


class RouteCombo:
    def __init__(self, name: str, assignments, timing, reads, checkdown):
        # Need to read these into offensive play
        # Works differently
        # Work in different reads based off of coverage
        self._name = name
        self._assignments = assignments
        self._timing = timing
        self._reads = reads
        self._checkdown = checkdown
        self._yards = {a: assignments[a].yards for a in self._assignments}

    @property
    def checkdown(self):
        return self._checkdown

    @property
    def yards(self):
        return self._yards

    @property
    def reads(self):
        return self._reads

    @property
    def timing(self):
        return self._timing

    @property
    def assignments(self):
        return self._assignments


# TODO: SCAN block
BLOCK_LEFT = SingleRoute(field_loc=BACK_LEFT, blocking=True)
BLOCK_CENTER = SingleRoute(field_loc=BACK_CENTER, blocking=True)
BLOCK_RIGHT = SingleRoute(field_loc=BACK_RIGHT, blocking=True)
BLOCK_SCAN = SingleRoute(field_loc=BACK_SCAN, blocking=True)
RUN_LEFT = SingleRoute(field_loc=BACK_LEFT, rusher=True)
RUN_CENTER = SingleRoute(field_loc=BACK_CENTER, rusher=True)
RUN_RIGHT = SingleRoute(field_loc=BACK_RIGHT, rusher=True)
SHORT_LEFT_R = SingleRoute(field_loc=SHORT_LEFT, route=True)
MID_LEFT_R = SingleRoute(field_loc=MID_LEFT, route=True)
MID_CENTER_R = SingleRoute(field_loc=MID_CENTER, route=True)
FAR_LEFT_R = SingleRoute(field_loc=FAR_LEFT, route=True)
FAR_CENT_L_R = SingleRoute(field_loc=FAR_CENT_L, route=True)
FAR_CENT_R_R = SingleRoute(field_loc=FAR_CENT_R, route=True)
FAR_RIGHT_R = SingleRoute(field_loc=FAR_RIGHT, route=True)
SHORT_RIGHT_R = SingleRoute(field_loc=SHORT_RIGHT, route=True)
PASSING = SingleRoute(field_loc=BACK_CENTER, qb=True)


# How to deal with players and not use numbers?  Need something else or I will get mixed up.  # Need to include blocking
DRIVE_SINGLEBACK = RouteCombo("Drive",
                       {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_CENTER, GenOff.C: BLOCK_CENTER,
                        GenOff.OG_L: BLOCK_CENTER, GenOff.OT_L: BLOCK_LEFT, GenOff.REC2: MID_LEFT_R,
                        GenOff.REC1: SHORT_LEFT_R, GenOff.REC4: MID_CENTER_R, GenOff.QB: PASSING,
                        GenOff.REC5: SHORT_RIGHT_R, GenOff.REC3: BLOCK_RIGHT},
                       {GenOff.REC1: 2, GenOff.REC2: 2.5, GenOff.REC3: 0, GenOff.REC4: 2, GenOff.REC5: 1.5},
                       [GenOff.REC2, GenOff.REC1, GenOff.REC4], GenOff.REC5)

CENTER_RUN = RouteCombo("Center Run",
                        {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_CENTER, GenOff.C: BLOCK_CENTER,
                         GenOff.OG_L: BLOCK_CENTER,  GenOff.OT_L: BLOCK_LEFT,  GenOff.REC2: FAR_CENT_R_R,
                         GenOff.REC1: FAR_LEFT_R,    GenOff.REC4: BLOCK_RIGHT,  GenOff.QB: PASSING,
                         GenOff.REC5: RUN_CENTER,  GenOff.REC3: FAR_CENT_L_R},
                        {GenOff.REC1: 0, GenOff.REC2: 0, GenOff.REC3: 0, GenOff.REC4: 0, GenOff.REC5: 0},
                        [], None)

KICK_ASSIGN = RouteCombo("Kick Orders",
                        {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_RIGHT, GenOff.C: BLOCK_CENTER,
                         GenOff.OG_L: BLOCK_LEFT,  GenOff.OT_L: BLOCK_LEFT,  GenOff.REC2: BLOCK_RIGHT,
                         GenOff.REC1: BLOCK_LEFT,    GenOff.REC4: BLOCK_RIGHT,  GenOff.QB: PASSING,
                         GenOff.REC5: BLOCK_CENTER,  GenOff.REC3: BLOCK_LEFT},
                        {GenOff.REC1: 0, GenOff.REC2: 0, GenOff.REC3: 0, GenOff.REC4: 0, GenOff.REC5: 0},
                        [], None)
