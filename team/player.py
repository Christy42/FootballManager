import yaml
from random import randint

from enums import Attribute
from team.attributes import MatchAttributes
# from team.attributes import MatchAttributes


class PlayerBase:
    def __init__(self, name, id_no):
        self._name = name
        self._id = id_no

    @classmethod
    def from_file(cls, file_name):
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
    def __init__(self, passing, tackling, elusiveness, strength, speed, catching, jumping, vision, fitness, weight,
                 height, age, optimal_age, coverage, blocking, awareness, route_running, carrying, name, id_no):
        super().__init__(name, id_no)
        self.attributes = MatchAttributes(passing, tackling, elusiveness, strength, speed, catching, jumping, vision,
                                          fitness, weight, height, age, optimal_age, coverage, blocking,
                                          carrying, route_running, awareness)

        self.state = PlayerState()

    @classmethod
    def from_file(cls, file_name):
        with open(file_name, "r") as file:
            stats = yaml.safe_load(file)
        return cls(stats["PASSING"], stats["TACKLING"], stats["ELUSIVENESS"], stats["STRENGTH"], stats["SPEED"],
                   stats["CATCHING"], stats["JUMPING"], stats["VISION"], stats["FITNESS"], stats["WEIGHT"],
                   stats["HEIGHT"], stats["AGE"], stats["OPTIMAL_AGE"], stats["COVERAGE"], stats["BLOCKING"],
                   stats["AWARENESS"], stats["ROUTE_RUNNING"], stats["CARRYING"], stats["NAME"], stats["ID"])


class PractisePlayer(MatchPlayer):
    def __init__(self, age, serve, shot_selection, accuracy, strength, strength_optimal, mobility, mobility_optimal,
                 fitness, fitness_optimal, stamina, serve_aggression, second_serve_aggression,
                 aggression, tactic, name, id_no):
        super().__init__(age, serve, shot_selection, accuracy, strength, strength_optimal, mobility, mobility_optimal,
                         fitness, fitness_optimal, stamina, serve_aggression, second_serve_aggression,
                         aggression, tactic, name, id_no)
        self.attributes.strength.set_mult_value(randint(0, 20) + 80)
        self.attributes.accuracy.set_mult_value(randint(0, 20) + 80)
        self.attributes.shot_selection.set_mult_value(randint(0, 20) + 80)
        self.attributes.mobility.set_mult_value(randint(0, 20) + 80)
        self.attributes.serve.set_mult_value(randint(0, 20) + 80)
        self.attributes.fitness.set_mult_value(randint(0, 20) + 100)


class PlayerState:
    def __init__(self):
        self._sets_won = 0
        self._games_won = 0
        self._points_won = 0
        self._points_won_old_games = []
        self._games_won_old_sets = [0]


# b = MatchPlayer.from_file("..//sample//players//player.yaml")
# print(b.attributes.passing)
# print(b.attributes.strength)
