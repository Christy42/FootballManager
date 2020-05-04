import random

from utils import exp_limited
from procedures.procedure import Procedure
from enums import GenOff


class KickOff(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        kicker = self.match.state.cur_off_players[GenOff.QB][0]
        returner = self.match.state.cur_def_players[10][0]
        self.match.state.kicking = False
        distance = round(kicker.kicking / 30) + 60 + random.randint(0, 30)
        print("distance " + str(distance))
        # TODO: A proper return
        # TODO: How and when to call this, probably in coin flip and after TDs, Kicks
        self.match.state.blue_flag()
        if distance > 85 or (distance > 75 and returner.speed < 500):
            self.match.state.set_ball_loc(75)
        else:
            return_dist = max(0, round(returner.speed / 100) + random.randint(5, 20) - 5
                              if random.random() * 4000 > 3000 + returner.catching else 0)
            final = distance - return_dist
            print("return " + str(final))
            self.match.state.set_ball_loc(final)


class Kick(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        kicker = self.match.state.cur_off_players[0]
        distance = 100 - self.match.state.ball_position + 10 + 5 \
            if kicker.strength + kicker.kicking <= random.random() * 2000 else 0 + 5 \
            if kicker.strength + kicker.kicking <= random.random() * 2000 else 0
        miss_odds = distance * distance + 101 - kicker.kicking
        return 1 if 10000 - miss_odds > random.random() * 10000 else 0


class Punt(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        print("Punt used")
        punter = self.match.state.cur_off_players[GenOff.QB][0]
        returner = self.match.state.cur_def_players[10][0]
        self.match.state.kicking = False
        distance = self.match.state.ball_position + round(punter.strength / 40) + 20 + random.randint(0, 15)
        print("distance " + str(distance))
        # TODO: A proper return
        # TODO: How and when to call this, probably in coin flip and after TDs, Kicks
        self.match.state.blue_flag()
        if distance > 100:
            if random.random() * 2000 > 1000 + punter.punt:
                self.match.state.set_ball_loc(80)
            else:
                self.match.state.set_ball_loc(80 + punter.punt / 100 + random.randint(0, 9))
        elif distance > 90 and random.random() * 2000 > 1000 + punter.punt and \
                random.random() * 2000 > 1000 + punter.punt + (1000 - punter.punt) / 2:
            self.match.state.set_ball_loc(distance - 10 + punter.punt / 200 + random.randint(0, 5))
        else:
            # TODO: Eventually stick in full blocking/ tackling stuff here, if statement is a fumble, could be expanded
            # TODO: Turning over a turn over could be an issue
            return_dist = max(0, round(returner.speed / 500) + exp_limited(0, 20, 2 - returner.speed / 2000) - 5
                              if random.random() * 4000 > 3000 + returner.catching else 0)

            final = distance - return_dist
            print("return " + str(final))
            self.match.state.set_ball_loc(final)
