from enums import OffenseFormation, DefenseFormation, Position


class BaseTeam:
    def __init__(self):
        pass

    # TODO: This should be that class creation method
    @classmethod
    def from_file(cls, file, tactics):
        pass


class MatchTeam(BaseTeam):
    def __init__(self):
        super().__init__()
        # TODO: Upload from the match file
        self._timing = 35

        self._offense_roster = {OffenseFormation.DOUBLE_TE: [], OffenseFormation.FIELD_GOAL: [],
                                OffenseFormation.I_FORM: [], OffenseFormation.KICK_OFF: [], OffenseFormation.PUNT: [],
                                OffenseFormation.SHOTGUN: [], OffenseFormation.SINGLEBACK: [],
                                OffenseFormation.SPREAD: []}
        self._defense_roster = {DefenseFormation.DIME: [], DefenseFormation.FOUR_FOUR: [],
                                DefenseFormation.FOUR_THREE: [], DefenseFormation.KICK_BLOCK: [],
                                DefenseFormation.KICK_RETURN: [], DefenseFormation.NICKEL: [],
                                DefenseFormation.PUNT_RETURN: [], DefenseFormation.THREE_FOUR: []}
        # Format {player: %} how does this interact with the roster???  Seems to be two issues at play
        self._position_rotation = {Position.QB: {}, Position.RB: {}, Position.C: {}, Position.CB: {}, Position.DE: {},
                                   Position.DT: {}, Position.FB: {}, Position.G: {}, Position.K: {}, Position.KR: {},
                                   Position.MLB: {}, Position.N: {}, Position.OG: {}, Position.OLB: {}, Position.OT: {},
                                   Position.P: {}, Position.PR: {}, Position.S: {}, Position.TE: {}, Position.WR: {}}
        self._state = TeamState()
        self._tactics = []
        # TODO: Something to do with tactics, how does the decision making process


class TeamState:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    def add_score(self, new_score):
        self._score += new_score
