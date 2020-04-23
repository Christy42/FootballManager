import yaml
import random

from utils import get_pos
from enums import OffenseFormation, DefenseFormation, Position, GenericOff
from team.player import MatchPlayer
from plays.defense_plays import DEF_PLAY_LIST
from plays.offense_plays import OFF_PLAY_LIST
from plays import defense_formation as df
from plays import offense_formation as of


class BaseTeam:
    def __init__(self):
        pass

    # TODO: This should be that class creation method
    @classmethod
    def from_file(cls, file, tactics_file):
        pass


class MatchTeam(BaseTeam):
    def __init__(self, players, rota, id_no, tactics):
        super().__init__()
        self._id = id_no
        # TODO: Upload from the match file
        self._timing = 35
        # TODO: Need checks that the rotas make sense (eventually)
        # TODO: Need to actually upload the players.  Need to check rotas properly
        self.players = []
        self.state = TeamState()
        for p in players:
            self.players.append(MatchPlayer.from_file("sample//players//" + p + ".yaml"))
        # Format {player: %} how does this interact with the roster???  Seems to be two issues at play
        self._pos_rota = {Position.QB: self.set_rota(rota["QB"]), Position.RB: self.set_rota(rota["RB"]),
                          Position.C: self.set_rota(rota["C"]), Position.CB: self.set_rota(rota["CB"]),
                          Position.DE: self.set_rota(rota["DE"]), Position.DT: self.set_rota(rota["DT"]),
                          Position.FB: self.set_rota(rota["FB"]), Position.GNR: self.set_rota(rota["GNR"]),
                          Position.K: self.set_rota(rota["K"]), Position.KR: self.set_rota(rota["KR"]),
                          Position.MLB: self.set_rota(rota["MLB"]), Position.NICKEL: self.set_rota(rota["NICKEL"]),
                          Position.OG: self.set_rota(rota["OG"]), Position.OLB: self.set_rota(rota["OLB"]),
                          Position.OT: self.set_rota(rota["OT"]), Position.P: self.set_rota(rota["P"]),
                          Position.PR: self.set_rota(rota["PR"]), Position.SF: self.set_rota(rota["SF"]),
                          Position.TE: self.set_rota(rota["TE"]), Position.WR: self.set_rota(rota["WR"]),
                          Position.DIME: self.set_rota(rota["DIME"]), Position.SLOT: self.set_rota(rota["SLOT"])}
        print(self._pos_rota)
        self._state = TeamState()
        self._tactics = tactics
        # TODO: Something to do with tactics, how does the decision making process

    @staticmethod
    def set_rota(rota):
        player_list = {}
        stem = "sample//players//"
        for player in rota:
            # player_list.update({player: [MatchPlayer.from_file(stem + player + ".yaml"), rota[player]]})
            player_list.update({MatchPlayer.from_file(stem + player + ".yaml"): rota[player]})
        return player_list

    @classmethod
    def from_file(cls, file, tactics_file):
        with open(file, "r") as file:
            stats = yaml.safe_load(file)
        with open(tactics_file, "r") as file:
            tactics = yaml.safe_load(file)
        return cls(stats["players"], stats["rota"], stats["id"], tactics)

    @property
    def id_no(self):
        return self._id

    # TODO: Probably add in down/distance stuff but leave for now
    def choose_play_offense(self, down, kick=False):
        if kick:
            return OFF_PLAY_LIST["KickOff"]
        print(self._tactics["offense"])
        choice = random.choices(list(self._tactics["offense"][down].keys()),
                                weights=list(self._tactics["offense"][down].values()))
        return OFF_PLAY_LIST[choice[0]]

    def choose_play_defense(self):
        choice = random.choices(list(self._tactics["defense"].keys()), weights=list(self._tactics["defense"].values()))
        return DEF_PLAY_LIST[choice[0]]

    def choose_offense(self, formation: of.OffenseFormation):
        # how are we ordering this.  Kind of want to do the optional stuff first.  Still just assuming it works
        # which is bad.  Soooo lets go with FB, SLOT2, TE2, SLOT1, TE1, RB1, WR1, WR2, OT1, OT2, OG1, OG2, C, QB
        # Then order like OT, OG, C, OG, OT, WR1, WR2, WR3, WR4, RB1, QB
        # Maybe go with the REC1 REC2 things etc.
        # TODO: Kicking
        # Need to assure no duplicates
        # While True is emulating a do loop
        # This is all overly long and weird, need a better way of doing this
        cur_list = []
        k = get_pos(cur_list, self._pos_rota[Position.K]) if formation.no_k > 0 else None
        cur_list.append(k)
        gnr2 = get_pos(cur_list, self._pos_rota[Position.GNR]) if formation.no_gnr > 1 else None
        cur_list.append(gnr2)
        gnr1 = get_pos(cur_list, self._pos_rota[Position.GNR]) if formation.no_gnr > 0 else None
        cur_list.append(gnr1)
        fb = get_pos(cur_list, self._pos_rota[Position.FB]) if formation.no_rbs > 1 else None
        cur_list.append(fb)
        wr4 = get_pos(cur_list, self._pos_rota[Position.SLOT]) if formation.no_wrs > 3 else None
        cur_list.append(wr4)
        te2 = get_pos(cur_list, self._pos_rota[Position.TE]) if formation.no_tes > 1 else None
        cur_list.append(te2)
        wr3 = get_pos(cur_list, self._pos_rota[Position.SLOT]) if formation.no_wrs > 2 else None
        cur_list.append(wr3)
        te = get_pos(cur_list, self._pos_rota[Position.TE]) if formation.no_tes > 0 else None
        cur_list.append(te)
        rb = get_pos(cur_list, self._pos_rota[Position.RB]) if formation.no_rbs > 0 else None
        cur_list.append(rb)
        wr2 = get_pos(cur_list, self._pos_rota[Position.WR]) if formation.no_wrs > 1 else None
        cur_list.append(wr2)
        wr1 = get_pos(cur_list, self._pos_rota[Position.WR]) if formation.no_wrs > 0 else None
        cur_list.append(wr1)
        ot2 = get_pos(cur_list, self._pos_rota[Position.OT])
        cur_list.append(ot2)
        ot1 = get_pos(cur_list, self._pos_rota[Position.OT])
        cur_list.append(ot1)
        og2 = get_pos(cur_list, self._pos_rota[Position.OG])
        cur_list.append(og2)
        og1 = get_pos(cur_list, self._pos_rota[Position.OG])
        cur_list.append(og1)
        c = get_pos(cur_list, self._pos_rota[Position.C])
        cur_list.append(c)
        qb = get_pos(cur_list, self._pos_rota[Position.QB]) if formation.no_k < 1 else None
        # Should eventually be a class really instead of relying on numbers.
        players = [ot2, og2, c, og1, ot1, wr1, wr2, wr3, wr4, rb, fb, te, te2, gnr1, gnr2, qb, k]
        plyrs = [x for x in players if x is not None]
        return {GenericOff.OT_L: plyrs[0], GenericOff.OG_L: plyrs[1], GenericOff.C: plyrs[2], GenericOff.OG_R: plyrs[3],
                GenericOff.OT_R: plyrs[4], GenericOff.REC1: plyrs[5], GenericOff.REC2: plyrs[6],
                GenericOff.REC3: plyrs[7], GenericOff.REC4: plyrs[8], GenericOff.REC5: plyrs[9],
                GenericOff.QB: plyrs[10]}

    # ordering of DE1, DT1, DT2, DE2, MLB1, MLB2, OLB1, OLB2, NICKEL, DIME, CB1, CB2, SF1, SF2 as appropriate
    def choose_defense(self, formation: df.DefenseFormation) -> list:
        cur_list = []
        dime = get_pos(cur_list, self._pos_rota[Position.DIME]) if formation.no_cb > 3 else None
        cur_list.append(dime)
        nick = get_pos(cur_list, self._pos_rota[Position.NICKEL]) if formation.no_cb > 2 else None
        cur_list.append(nick)
        mlb2 = get_pos(cur_list, self._pos_rota[Position.MLB]) if formation.no_lb > 3 else None
        cur_list.append(mlb2)
        olb1 = get_pos(cur_list, self._pos_rota[Position.OLB]) if formation.no_lb > 1 else None
        cur_list.append(olb1)
        olb2 = get_pos(cur_list, self._pos_rota[Position.OLB]) if formation.no_lb > 2 else None
        cur_list.append(olb2)
        dt2 = get_pos(cur_list, self._pos_rota[Position.DT]) if formation.no_dl > 3 else None
        cur_list.append(dt2)
        de2 = get_pos(cur_list, self._pos_rota[Position.DE])
        cur_list.append(de2)
        de1 = get_pos(cur_list, self._pos_rota[Position.DE])
        cur_list.append(de1)
        dt1 = get_pos(cur_list, self._pos_rota[Position.DT])
        cur_list.append(dt1)
        mlb1 = get_pos(cur_list, self._pos_rota[Position.MLB])
        cur_list.append(mlb1)
        cb1 = get_pos(cur_list, self._pos_rota[Position.CB])
        cur_list.append(cb1)
        cb2 = get_pos(cur_list, self._pos_rota[Position.CB])
        cur_list.append(cb2)
        sf1 = get_pos(cur_list, self._pos_rota[Position.SF])
        cur_list.append(sf1)
        sf2 = get_pos(cur_list, self._pos_rota[Position.SF])
        cur_list.append(sf2)
        players = [de1, dt1, dt2, de2, mlb1, mlb2, olb1, olb2, nick, dime, cb1, cb2, sf1, sf2]
        return [x for x in players if x is not None]


class TeamState:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    def add_score(self, new_score):
        self._score += new_score


# MatchTeam.from_file("..//sample//team1.yaml")
# MatchTeam.from_file("..//sample//team2.yaml")
