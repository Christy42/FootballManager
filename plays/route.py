from enums import FieldPoints, GenericOff, OffensiveAssignments


class RouteRead:
    def __init__(self, name, reads, assignments, check_down):
        # Need to read these into offensive play
        # Works differently
        self._check_down = check_down
        self._name = name
        self._reads = reads
        self._assignments = assignments

    @property
    def reads(self):
        return self._reads


class Route:
    def __init__(self, route_closed_man, route_closed_zone, route_open_man, route_open_zone):
        self._route_clsd_man = route_closed_man
        self._route_clsd_zone = route_closed_zone
        self._route_open_man = route_open_man
        self._route_open_zone = route_open_zone


# How to deal with players and not use numbers?  Need something else or I will get mixed up.  # Need to include blocking
_DRIVE_MAN = RouteRead("Drive", [GenericOff.REC2, GenericOff.REC1, GenericOff.REC4], GenericOff.REC5,
                       {GenericOff.REC2: FieldPoints.MID_LEFT, GenericOff.REC1: FieldPoints.SHORT_LEFT,
                        GenericOff.REC4: FieldPoints.MID_CENTER, GenericOff.REC5: FieldPoints.SHORT_RIGHT,
                        GenericOff.REC3: OffensiveAssignments.RIGHT_BLOCK})

DRIVE_SINGLEBACK = Route(_DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN)

