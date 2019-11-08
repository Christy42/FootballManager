class BaseTeam:
    def __init__(self):
        pass


class MatchTeam(BaseTeam):
    def __init__(self, match_file):
        super().__init__()
        # TODO: Upload from the match file
        self._match_roster = []
        self._offense_roster = []
        self._defense_roster = []
        self._kicker = 0
        self._punter = 0
        self._state = TeamState()
        # TODO: Something to do with tactics


class TeamState:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    def add_score(self, new_score):
        self._score += new_score
