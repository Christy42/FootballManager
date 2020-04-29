from enums import OffAssign, GenOff
from plays.field_loc import *


class RouteRead:
    def __init__(self, name, reads, assignments, check_down, timing):
        # Need to read these into offensive play
        # Works differently
        self._check_down = check_down
        self._name = name
        self._reads = reads
        self._assignments = assignments
        self._timing = timing
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


class Route:
    def __init__(self, route_closed_man, route_closed_zone, route_open_man, route_open_zone):
        self._route_clsd_man = route_closed_man
        self._route_clsd_zone = route_closed_zone
        self._route_open_man = route_open_man
        self._route_open_zone = route_open_zone


# How to deal with players and not use numbers?  Need something else or I will get mixed up.  # Need to include blocking
_DRIVE_MAN = RouteRead("Drive", [GenOff.REC2, GenOff.REC1, GenOff.REC4],
                       {GenOff.REC2: MID_LEFT, GenOff.REC1: SHORT_LEFT, GenOff.REC4: MID_CENTER,
                        GenOff.REC5: SHORT_RIGHT, GenOff.REC3: OffAssign.RIGHT_BLOCK}, GenOff.REC5,
                       {GenOff.REC1: 2, GenOff.REC2: 2.5, GenOff.REC3: 0, GenOff.REC4: 2, GenOff.REC5: 1.5})

DRIVE_SINGLEBACK = Route(_DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN)
