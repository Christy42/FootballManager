from enums import FieldPoints, Receivers


class RouteRead:
    def __init__(self, name, read_1, read_2, read_3, reads, read_1_attack,
                 read_2_attack, read_3_attack, check_down, check_down_attack, closed, man):
        # Need to read these into offensive play
        # Works differently
        self._read_1 = read_1
        self._read_2 = read_2
        self._read_3 = read_3
        self._check_down = check_down
        self._name = name
        self._reads = reads
        self._read_1_attack = read_1_attack
        self._read_2_attack = read_2_attack
        self._read_3_attack = read_3_attack
        self._check_down_attack = check_down_attack
        self._closed = closed
        self._man = man


class Route:
    def __init__(self, route_closed_man, route_closed_zone, route_open_man, route_open_zone):
        self._route_clsd_man = route_closed_man
        self._route_clsd_zone = route_closed_zone
        self._route_open_man = route_open_man
        self._route_open_zone = route_open_zone


# How to deal with players and not use numbers?  Need something else or I will get mixed up
_DRIVE_MAN = RouteRead("Drive", Receivers.REC2, Receivers.REC1, Receivers.REC4, Receivers.REC5, 3,
                       FieldPoints.MID_LEFT, FieldPoints.SHORT_LEFT, FieldPoints.MID_CENTER,
                       FieldPoints.SHORT_RIGHT, True, True)

DRIVE_SINGLEBACK = Route(_DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN, _DRIVE_MAN)

