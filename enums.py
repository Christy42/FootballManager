from enum import Enum


class Outcome:
    # TODO: Utilise this more instead of the big tables
    def __init__(self, outcome, value=0, player=None, secondary=None, score=None):
        self._outcome = outcome
        self._value = value
        self._player = player
        self._secondary = secondary
        self._score = score

    @property
    def outcome(self):
        return self._outcome

    @property
    def secondary(self):
        return self._secondary

    @property
    def value(self):
        return self._value

    @property
    def player(self):
        return self._player

    @property
    def score(self):
        return self._score

    def update_score(self, score):
        self._score = score

    def to_yaml(self):
        return {"name": self._outcome.name, "score": self._score,
                "team": self._player.name if self._player is not None else None,
                "team id": self._player.id if self._player is not None else None,
                "value": self._value, "secondary": self._secondary.name if self._secondary is not None else None}


class Possession(Enum):
    TEAM_1 = 1
    TEAM_2 = 2


class OffenseFormation(Enum):
    SINGLEBACK = 1
    SHOTGUN = 2
    I_FORM = 3
    DOUBLE_TE = 4
    SPREAD = 5
    PUNT = 6
    KICK_OFF = 7
    FIELD_GOAL = 8


class DefenseFormation(Enum):
    FOUR_THREE = 1
    THREE_FOUR = 2
    NICKEL = 3
    DIME = 4
    FOUR_FOUR = 5
    KICK_RETURN = 6
    PUNT_RETURN = 7
    KICK_BLOCK = 8


class Position(Enum):
    QB = 1
    RB = 2
    WR = 3
    TE = 4
    C = 5
    OT = 6
    OG = 7
    FB = 8
    DT = 9
    DE = 10
    OLB = 11
    MLB = 12
    CB = 13
    NICKEL = 14
    SF = 15
    K = 16
    P = 17
    GNR = 18
    KR = 19
    PR = 20
    SLOT = 21
    DIME = 22


class PlayStyle(Enum):
    RUN = 1
    PASS = 2
    SPECIAL = 3


class Side(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3


class RunStyle(Enum):
    ZONE = 1
    MAN = 2


class Attribute(Enum):
    PASSING = 1
    TACKLING = 2
    ELUSIVENESS = 3
    STRENGTH = 4
    SPEED = 5
    CATCHING = 6
    JUMPING = 7
    VISION = 8
    FITNESS = 9
    WEIGHT = 10
    HEIGHT = 11
    STAMINA = 12
    AGE = 13
    STRENGTH_OPTIMAL = 14
    MOBILITY_OPTIMAL = 15
    AGE_OPTIMAL = 16
    FITNESS_OPTIMAL = 17
    POSITIONING = 18
    BLOCKING = 19
    CARRYING = 20
    ROUTE_RUNNING = 21
    RUSHING = 22


class OffAssignments(Enum):
    RUNNING = 1
    LEFT_BLOCK = 2
    RIGHT_BLOCK = 3
    CENTER_BLOCK = 4
    ROUTE_RUNNING = 5
    QB = 6
    KICK = 7
    SCAN_BLOCK = 8


class DefensiveAssignments(Enum):
    CENTER_RUSH = 1
    LEFT_RUSH = 2
    RIGHT_RUSH = 3
    MAN_1 = 4
    MAN_2 = 5
    MAN_3 = 6
    MAN_4 = 7
    MAN_5 = 8
    MAN_6 = 9  # Spy on the QB
    SHORT_LEFT_COVER = 10
    SHORT_CENTER_COVER = 11
    SHORT_RIGHT_COVER = 12
    MIDDLE_LEFT_COVER = 13
    MIDDLE_CENTER_COVER = 14
    MIDDLE_RIGHT_COVER = 15
    LONG_LEFT_COVER = 16
    LONG_CENTER_COVER = 17
    LONG_RIGHT_COVER = 18


class FieldPoints(Enum):  # All done from offense point of view
    # Back -5 -> 0, SHORT 1 -> 5, MID 6 -> 10, LONG 11 -> 15, FAR 16 -> 20, DEEP -> 21 - 25
    BACK_RIGHT = 1
    BACK_CENT_R = 2
    BACK_CENTER = 3
    BACK_CENT_L = 4
    BACK_LEFT = 5
    SHORT_RIGHT = 6
    SHORT_CENT_R = 7
    SHORT_CENTER = 8
    SHORT_CENT_L = 9
    SHORT_LEFT = 10
    MID_RIGHT = 11
    MID_CENT_R = 12
    MID_CENTER = 13
    MID_CENT_L = 14
    MID_LEFT = 15
    LONG_RIGHT = 16
    LONG_CENT_R = 17
    LONG_CENTER = 18
    LONG_CENT_L = 19
    LONG_LEFT = 20
    FAR_RIGHT = 16
    FAR_CENT_R = 17
    FAR_CENTER = 18
    FAR_CENT_L = 19
    FAR_LEFT = 20
    DEEP_RIGHT = 21
    DEEP_CENT_R = 22
    DEEP_CENTER = 23
    DEEP_CENT_L = 24
    DEEP_LEFT = 25


class GenericOff(Enum):
    REC1 = 1
    REC2 = 2
    REC3 = 3
    REC4 = 4
    REC5 = 5
    OT_L = 6
    OG_L = 7
    C = 8
    OG_R = 9
    OT_R = 10
    QB = 11
