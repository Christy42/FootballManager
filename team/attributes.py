import utils

ATTRIBUTE_MIN = 0
ATTRIBUTE_MAX = 100


class Attribute:
    def __init__(self, name, base_value):
        self._value = base_value
        self._base_value = base_value
        self._name = name
        self._stam_factor = 1
        self._add_factor = 0
        self._mult_factor = 1

    @property
    def base_value(self):
        return self._base_value

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def _update_value(self):
        self._value = max(min(self._base_value * self._mult_factor * self._stam_factor + self._add_factor,
                              ATTRIBUTE_MAX), ATTRIBUTE_MIN)

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
        base_value = int((-age ** 2 + 2 * optimal_age * age + basis))
        super().__init__(name, base_value)

    def stamina_effect(self, stamina):
        stam_value = (stamina < 500) * 0.2 + (stamina < 300) * 0.1 + (stamina <= 0) * 0.1 + 0.2
        self._stam_factor = (100 * (1 - stam_value + stam_value * stamina / 1000))
        self._update_value()


class StaminaAttribute(PhysicalAttribute):
    def __init__(self, name, basis, age, optimal_age, fitness):
        super().__init__(name, basis, age, optimal_age)
        self._fitness = fitness

    def amend_stamina(self, value):
        self._value = self._value - value

    def reset_stat(self):
        self._value = self._fitness


class MatchAttributes:
    def __init__(self):
        self._fitness = 1
        self._stamina = 1
        self._passing = 1
        self._catching = 1
        self._route_running = 1
        self._carrying = 1
        self._blocking = 1
        self._vision = 1
        self._tackling = 1
        self._awareness = 1
        self._coverage = 1
        self._jumping = 1