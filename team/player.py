import yaml

from enums import Attribute


class PlayerBase:
    def __init__(self, name, id_no):
        self._name = name
        self._id = id_no

    @classmethod
    def from_file(cls, file_name, second_file):
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
                 height, stamina, age, optimal_age, positioning, blocking,
                 carrying, name, id_no):
        super().__init__(name, id_no)
        self.attributes = MatchAttributes(passing, tackling, elusiveness, strength, speed, catching, jumping, vision,
                                          fitness, weight, height, stamina, age, optimal_age, positioning, blocking,
                                          carrying)
        self.statistics = PlayerStatistics(name)
        self.state = PlayerState()

    @classmethod
    def from_file(cls, file_name, match_file):
        with open(file_name, "r") as file:
            stats = yaml.safe_load(file)
        with open(match_file, "r") as file:
            tactics = yaml.safe_load(file)
        return cls(stats[Attribute.AGE], stats[Attribute.AGE_OPTIMAL], stats[Attribute.BLOCKING],
                   stats[Attribute.CARRYING], stats["strength_basis"],
                   stats["strength_optimal_age"], stats["mobility_basis"], stats["mobility_optimal_age"],
                   stats["fitness_basis"], stats["fitness_optimal_age"], stats["stamina"], tactics["serve_aggression"],
                   tactics["second_serve_aggression"], tactics["aggression"], tactics["tactic"], stats["name"],
                   stats["id"])

    @property
    def tactic(self):
        return self._tactic


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
