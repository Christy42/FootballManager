class Attribute:
    def __init__(self, name, base_value):
        self._value = base_value
        self._base_value = base_value
        self._name = name
        self._mult_factor = 1

    @property
    def base_value(self):
        return self._base_value

    @property
    def modified_value(self):
        return self._modified_value

    @property
    def name(self):
        return self._name

    def modify_add(self, modifier):
        self._value = max(self._value + modifier, 0)

    def set_mult_value(self, modifier):
        self._mult_factor *= modifier / 100
        self._value *= self._mult_factor

    def reset_stat(self):
        self._value = self._base_value

    def stamina_effect(self, stamina):
        value = (stamina < 500) * 0.2 + (stamina < 300) * 0.1 + (stamina <= 0) * 0.1
        self._value = self._base_value * (1 - value + value * stamina / 500)
        self.set_mult_value(100)

    @classmethod
    def initiate(cls, name):
        base = utils.repeated_randint(15, 25, 4)
        return cls(name, base)

class PhysicalAttribute(Attribute):
