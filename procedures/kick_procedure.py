import random

from procedures.procedure import Procedure


class KickOff(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        print(len(self.match.state.cur_off_players))
        kicker = self.match.state.cur_off_players[10][0]
        returner = self.match.state.cur_def_players[10][0]
        self.match.state.kicking = False
        distance = round(kicker.kicking / 30) + 60 + random.randint(0, 30)
        print("distance " + str(distance))
        # TODO: A proper return
        # TODO: How and when to call this, probably in coin flip and after TDs, Kicks
        self.match.state.blue_flag()
        if distance > 85 or (distance > 75 and returner.speed < 500):
            print("stable")
            self.match.state.set_ball_loc(75)
        else:
            final = distance - round(returner.speed / 500) - random.randint(5, 20)
            print("return " + str(final))
            self.match.state.set_ball_loc(final)


class Kick(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        kicker = self.match.state.cur_off_players[0]
        # TODO: Add potential kick block
        # TODO: Deal with successful kicks
        if kicker.kicking > random.random():
            return 1
        else:
            return 0


class Punt(Procedure):
    def __init__(self, match):
        super().__init__(match)

    def step(self):
        pass
