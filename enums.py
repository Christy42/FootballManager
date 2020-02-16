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


class OffensiveAssignments(Enum):
    RUNNING = 1
    LEFT_BLOCK = 2
    RIGHT_BLOCK = 3
    CENTER_BLOCK = 4
    THROWING = 5
    HITCH_LEFT = 6
    HITCH_RIGHT = 7
    TE_HITCH_LEFT = 8
    TE_HITCH_RIGHT = 9
    COMEBACK_LEFT = 10
    COMEBACK_RIGHT = 11
    CURL_LEFT = 12
    CURL_RIGHT = 13
    OUT_LEFT = 14
    OUT_RIGHT = 15
    DIG_LEFT = 16
    DIG_RIGHT = 17
    SLANT_LEFT = 18
    SLANT_RIGHT = 19
    FADE_RIGHT = 20
    FADE_LEFT = 21
    POST_LEFT = 22
    POST_RIGHT = 23


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
