import yaml

from enums import OffenseFormation, DefenseFormation, Position
from player import MatchPlayer


class BaseTeam:
    def __init__(self):
        pass

    # TODO: This should be that class creation method
    @classmethod
    def from_file(cls, file):
        pass


class MatchTeam(BaseTeam):
    def __init__(self, players, rota):
        super().__init__()
        # TODO: Upload from the match file
        self._timing = 35
        # TODO: Need checks that the rotas make sense (eventually)
        self.players = []
        for p in players:
            self.players.append(MatchPlayer.from_file("..//sample//players//" + p + ".yaml"))
        # Format {player: %} how does this interact with the roster???  Seems to be two issues at play
        self._position_rotation = {Position.QB: rota["QB"], Position.RB: rota["RB"], Position.C: rota["C"],
                                   Position.CB: rota["CB"], Position.DE: rota["DE"], Position.DT: rota["DT"],
                                   Position.FB: rota["FB"], Position.GNR: rota["GNR"], Position.K: rota["K"],
                                   Position.KR: rota["KR"], Position.MLB: rota["MLB"], Position.NICKEL: rota["NICKEL"],
                                   Position.OG: rota["OG"], Position.OLB: rota["OLB"], Position.OT: rota["OT"],
                                   Position.P: rota["P"], Position.PR: rota["PR"], Position.SF: rota["SF"],
                                   Position.TE: rota["TE"], Position.WR: rota["WR"], Position.DIME: rota["DIME"]}
        self._state = TeamState()
        self._tactics = []
        # TODO: Something to do with tactics, how does the decision making process

    @classmethod
    def from_file(cls, file):
        with open(file, "r") as file:
            stats = yaml.safe_load(file)
        return cls(stats["players"], stats["rota"])


class TeamState:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    def add_score(self, new_score):
        self._score += new_score


MatchTeam.from_file("..//sample//team1.yaml")
MatchTeam.from_file("..//sample//team2.yaml")
