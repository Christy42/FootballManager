import utils

ATTRIBUTE_MIN = 0
ATTRIBUTE_MAX = 100


class Attribute:
    def __init__(self, name, basis_value, age, optimal_age):
        self._basis = basis_value
        self._cur_basis = basis_value
        self._age = age
        self._optimal_age = optimal_age
        self._value = self._calc_value()

        self._name = name
        self._stam_factor = 1
        self._add_factor = 0
        self._mult_factor = 1

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def _calc_value(self):
        return max(min(int((-self._age ** 2 / 2 + 2 * self._optimal_age * self._age / 2 + self._cur_basis)),
                       ATTRIBUTE_MAX), ATTRIBUTE_MIN)

    def _update_value(self):
        self._cur_basis = self._basis * self._mult_factor * self._stam_factor + self._add_factor
        self._calc_value()

    def modify_add(self, modifier):
        self._add_factor += modifier
        self._update_value()

    def set_mult_value(self, modifier):
        self._mult_factor *= modifier / 100
        self._update_value()

    def reset_stat(self):
        self._add_factor = 0
        self._mult_factor = 1
        self._stam_factor = 1
        self._update_value()

    def stamina_effect(self, stamina):
        stam_value = (stamina < 500) * 0.2 + (stamina < 300) * 0.1 + (stamina <= 0) * 0.1
        self._stam_factor = (100 * (1 - stam_value + stam_value * min(500, stamina) / 500))
        self._update_value()

    @classmethod
    def initiate(cls, name):
        base = utils.repeated_randint(15, 25, 4)
        return cls(name, base)


class PhysicalAttribute(Attribute):
    def __init__(self, name, basis, age, optimal_age):
        super().__init__(name, basis, age, optimal_age)

    def _calc_value(self):
        return max(min(int((-self._age ** 2 + 2 * self._optimal_age * self._age + self._cur_basis)),
                       ATTRIBUTE_MAX), ATTRIBUTE_MIN)

    def stamina_effect(self, stamina):
        stam_value = (stamina < 500) * 0.2 + (stamina < 300) * 0.1 + (stamina <= 0) * 0.1 + 0.2
        self._stam_factor = (100 * (1 - stam_value + stam_value * stamina / 1000))
        self._update_value()


class StaminaAttribute(PhysicalAttribute):
    def __init__(self, name, basis, age, optimal_age):
        super().__init__(name, basis, age, optimal_age)
        self._stamina_value = 1000

    def amend_stamina(self, value):
        self._stamina_value = max(min(self._value - value * self._value / 1000, 1000), 0)

    def stamina_effect(self, stamina):
        pass

    def reset_stat(self):
        self._stamina_value = 1000


class MatchAttributes:
    def __init__(self, passing, tackling, elusiveness, strength, speed, catching, punt, vision, fitness, weight, burst,
                 height, age, optimal_age, coverage, blocking, carrying, route_running, awareness, rushing, kicking):
        self._stamina = StaminaAttribute("stamina", fitness, age, optimal_age)
        self._passing = Attribute("passing", passing, age, optimal_age)
        self._catching = Attribute("catching", catching, age, optimal_age)
        self._route_running = PhysicalAttribute("route running", route_running, age, optimal_age)
        self._carrying = Attribute("carrying", carrying, age, optimal_age)
        self._blocking = Attribute("blocking", blocking, age, optimal_age)
        self._vision = Attribute("vision", vision, age, optimal_age)
        self._tackling = Attribute("tackling", tackling, age, optimal_age)
        self._awareness = Attribute("awareness", awareness, age, optimal_age)
        self._coverage = Attribute("coverage", coverage, age, optimal_age)
        self._punt = Attribute("punt", punt, age, optimal_age)
        self._strength = PhysicalAttribute("strength", strength, age, optimal_age)
        self._speed = PhysicalAttribute("speed", speed, age, optimal_age)
        self._elusiveness = PhysicalAttribute("elusiveness", elusiveness, age, optimal_age)
        self._rushing = Attribute("rushing", rushing, age, optimal_age)
        self._kicking = Attribute("kicking", kicking, age, optimal_age)
        self._burst = PhysicalAttribute("burst", burst, age, optimal_age)

    @property
    def stamina(self):
        return self._stamina.value

    @property
    def rushing(self):
        return self._rushing.value

    @property
    def passing(self):
        return self._passing.value

    @property
    def kicking(self):
        return self._kicking.value

    @property
    def catching(self):
        return self._catching.value

    @property
    def route_running(self):
        return self._route_running.value

    @property
    def carrying(self):
        return self._carrying.value

    @property
    def blocking(self):
        return self._blocking.value

    @property
    def vision(self):
        return self._vision.value

    @property
    def tackling(self):
        return self._tackling.value

    @property
    def awareness(self):
        return self._awareness.value

    @property
    def coverage(self):
        return self._coverage.value

    @property
    def punt(self):
        return self._punt.value

    @property
    def strength(self):
        return self._strength.value

    @property
    def speed(self):
        return self._speed.value

    @property
    def elusiveness(self):
        return self._elusiveness.value
