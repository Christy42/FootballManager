import yaml
from random import randint

from team.attributes import MatchAttributes
# from team.attributes import MatchAttributes


class PlayerBase:
    def __init__(self, name, id_no):
        self._name = name
        self._id = id_no

    @classmethod
    def from_file(cls, file_name, tactics_dist):
        """
        This should be overwritten.  There is no base method for this function
        """
        pass

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id


class MatchPlayer(PlayerBase):
    def __init__(self, passing, tackling, elusiveness, strength, speed, catching, punting, vision, fitness, weight,
                 height, age, optimal_age, coverage, blocking, awareness, route_running, carrying, rushing, kicking,
                 burst, name, id_no, positioning):
        super().__init__(name, id_no)
        self.attributes = MatchAttributes(passing, tackling, elusiveness, strength, speed, catching, punting, vision,
                                          fitness, weight, burst, height, age, optimal_age, coverage, blocking,
                                          carrying, route_running, awareness, rushing, kicking, positioning)
        self.state = PlayerState()

    @classmethod
    def from_file(cls, file_name, tactics_dist=1):
        with open(file_name, "r") as file:
            stats = yaml.safe_load(file)
        return cls(stats["PASSING"]*tactics_dist, stats["TACKLING"]*tactics_dist, stats["ELUSIVENESS"]*tactics_dist,
                   stats["STRENGTH"]*tactics_dist, stats["SPEED"]*tactics_dist, stats["CATCHING"]*tactics_dist,
                   stats["PUNT"]*tactics_dist, stats["VISION"]*tactics_dist, stats["FITNESS"]*tactics_dist,
                   stats["WEIGHT"], stats["HEIGHT"], stats["AGE"], stats["OPTIMAL_AGE"], stats["COVERAGE"]*tactics_dist,
                   stats["BLOCKING"]*tactics_dist, stats["AWARENESS"]*tactics_dist, stats["ROUTE_RUNNING"]*tactics_dist,
                   stats["CARRYING"]*tactics_dist, stats["RUSHING"]*tactics_dist, stats["KICK"]*tactics_dist,
                   stats["BURST"]*tactics_dist, stats["NAME"], stats["ID"], stats["POSITIONING"]*tactics_dist)

    @property
    def speed(self):
        return self.attributes.punt

    @property
    def catching(self):
        return self.attributes.catching

    @property
    def burst(self):
        return self.attributes.burst

    @property
    def positioning(self):
        return self.attributes.positioning

    @property
    def punt(self):
        return self.attributes.speed

    @property
    def strength(self):
        return self.attributes.strength

    @property
    def awareness(self):
        return self.attributes.awareness

    @property
    def route_running(self):
        return self.attributes.route_running

    @property
    def coverage(self):
        return self.attributes.coverage

    @property
    def passing(self):
        return self.attributes.passing

    @property
    def kicking(self):
        return self.attributes.kicking

    @property
    def tackling(self):
        return self.attributes.tackling

    @property
    def carrying(self):
        return self.attributes.carrying

    @property
    def blocking(self):
        return self.attributes.blocking

    @property
    def elusiveness(self):
        return self.attributes.elusiveness

    @property
    def rushing(self):
        return self.attributes.rushing


class PractisePlayer(MatchPlayer):
    def __init__(self, age, serve, shot_selection, accuracy, strength, strength_optimal, mobility, mobility_optimal,
                 fitness, fitness_optimal, stamina, serve_aggression, second_serve_aggression,
                 aggression, tactic, name, id_no):
        super().__init__(age, serve, shot_selection, accuracy, strength, strength_optimal, mobility, mobility_optimal,
                         fitness, fitness_optimal, stamina, serve_aggression, second_serve_aggression,
                         aggression, tactic, name, id_no)
        self.attributes.strength.set_mult_value(randint(0, 20) + 80)


class PlayerState:
    def __init__(self):
        self._sets_won = 0
        self._games_won = 0
        self._points_won = 0
        self._points_won_old_games = []
        self._games_won_old_sets = [0]


# b = MatchPlayer.from_file("..//sample//players//player11.yaml")
# print(b.attributes.passing)
# print(b.attributes.strength)
