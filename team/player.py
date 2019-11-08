
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
    def __init__(self, speed, tackling, awareness, vision, positioning, elusiveness, carrying,
                 fitness, weight, blocking, passing, catching, name, id_no):
        super().__init__(name, id_no)
        self.attributes = MatchAttributes(accuracy, shot_selection, serve, strength, mobility,
                                          fitness, stamina, age, strength_optimal, mobility_optimal, fitness_optimal)
        self.statistics = PlayerStatistics(name)
        self._serve_aggression = serve_aggression
        self._aggression = aggression
        self._second_serve_aggression = second_serve_aggression
        self._tactic = tactic
        self.state = PlayerState()

    @classmethod
    def from_file(cls, file_name, match_file):
        with open(file_name, "r") as file:
            stats = yaml.safe_load(file)
        with open(match_file, "r") as file:
            tactics = yaml.safe_load(file)
        return cls(stats["age"], stats["serve"], stats["shot_selection"], stats["serve"], stats["strength_basis"],
                   stats["strength_optimal_age"], stats["mobility_basis"], stats["mobility_optimal_age"],
                   stats["fitness_basis"], stats["fitness_optimal_age"], stats["stamina"], tactics["serve_aggression"],
                   tactics["second_serve_aggression"], tactics["aggression"], tactics["tactic"], stats["name"],
                   stats["id"])

    @property
    def serve_aggression(self):
        return self._serve_aggression

    @property
    def second_serve_aggression(self):
        return self._second_serve_aggression

    @property
    def aggression(self):
        return self._aggression

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

    @property
    def sets(self):
        return self._sets_won

    @property
    def points(self):
        return self._points_won

    @property
    def games(self):
        return self._games_won

    @property
    def points_won_in_match(self):
        return self._points_won_old_games

    @property
    def games_won_in_match(self):
        return self._games_won_old_sets

    def won_point(self):
        self._points_won += 1

    def won_game(self):
        self._points_won_old_games.append(self._points_won)
        self._games_won += 1
        self._games_won_old_sets[-1] = self._games_won
        self._points_won = 0

    def won_set(self):
        self._games_won_old_sets.append(0)
        self._sets_won += 1
        self._points_won = 0
        self._games_won = 0

    def lost_game(self):
        self._points_won_old_games.append(self._points_won)
        self._games_won_old_sets[-1] = self._games_won
        self._points_won = 0

    def lost_set(self):
        self._games_won_old_sets.append(0)
        self._games_won = 0
        self._points_won = 0
