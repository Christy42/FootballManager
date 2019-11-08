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
