from enums import OffAssign, GenOff
from plays.field_loc import *


class SingleRoute:
    def __init__(self, side, depth=Depth.BACK, blocking=False, qb=False, rusher=False, route=False):
        self.side = side
        self.depth = depth
        self.blocking = blocking
        self.qb = qb
        self.rusher = rusher
        self.route = route


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
        self._yards = {a: 0 if type(a) != FieldLocation else a.yards for a in self._assignments}

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
BLOCK_LEFT = SingleRoute(side=Side.LEFT, blocking=True)
BLOCK_CENTER = SingleRoute(side=Side.CENTER, blocking=True)
BLOCK_RIGHT = SingleRoute(side=Side.RIGHT, blocking=True)
RUN_LEFT = SingleRoute(side=Side.LEFT, rusher=True)
RUN_CENTER = SingleRoute(side=Side.CENTER, rusher=True)
RUN_RIGHT = SingleRoute(side=Side.RIGHT, rusher=True)
SHORT_LEFT_R = SingleRoute(side=Side.LEFT, depth=Depth.SHORT, route=True)
MID_LEFT_R = SingleRoute(side=Side.LEFT, depth=Depth.MID, route=True)
MID_CENTER_R = SingleRoute(side=Side.CENTER, depth=Depth.MID, route=True)
SHORT_RIGHT_R = SingleRoute(side=Side.RIGHT, depth=Depth.SHORT, route=True)
PASSING = SingleRoute(side=Side.CENTER, depth=Depth.BACK, qb=True)


# How to deal with players and not use numbers?  Need something else or I will get mixed up.  # Need to include blocking
DRIVE_SINGLEBACK = RouteCombo("Drive",
                       {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_RIGHT, GenOff.C: BLOCK_CENTER,
                        GenOff.OG_L: BLOCK_LEFT, GenOff.OT_L: BLOCK_LEFT, GenOff.REC2: MID_LEFT,
                        GenOff.REC1: SHORT_LEFT, GenOff.REC4: MID_CENTER, GenOff.QB: PASSING,
                        GenOff.REC5: SHORT_RIGHT, GenOff.REC3: BLOCK_RIGHT},
                       {GenOff.REC1: 2, GenOff.REC2: 2.5, GenOff.REC3: 0, GenOff.REC4: 2, GenOff.REC5: 1.5},
                       [GenOff.REC2, GenOff.REC1, GenOff.REC4], GenOff.REC5)

CENTER_RUN = RouteCombo("Center Run",
                        {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_RIGHT, GenOff.C: BLOCK_CENTER,
                         GenOff.OG_L: BLOCK_LEFT,  GenOff.OT_L: BLOCK_LEFT,  GenOff.REC2: FAR_CENT_R,
                         GenOff.REC1: FAR_LEFT,    GenOff.REC4: BLOCK_RIGHT,  GenOff.QB: PASSING,
                         GenOff.REC5: RUN_CENTER,  GenOff.REC3: FAR_CENT_L},
                        {GenOff.REC1: 0, GenOff.REC2: 0, GenOff.REC3: 0, GenOff.REC4: 0, GenOff.REC5: 0},
                        [], None)

KICK_ASSIGN = RouteCombo("Kick Orders",
                        {GenOff.OT_R: BLOCK_RIGHT, GenOff.OG_R: BLOCK_RIGHT, GenOff.C: BLOCK_CENTER,
                         GenOff.OG_L: BLOCK_LEFT,  GenOff.OT_L: BLOCK_LEFT,  GenOff.REC2: BLOCK_RIGHT,
                         GenOff.REC1: BLOCK_LEFT,    GenOff.REC4: BLOCK_RIGHT,  GenOff.QB: PASSING,
                         GenOff.REC5: BLOCK_CENTER,  GenOff.REC3: BLOCK_LEFT},
                        {GenOff.REC1: 0, GenOff.REC2: 0, GenOff.REC3: 0, GenOff.REC4: 0, GenOff.REC5: 0},
                        [], None)
