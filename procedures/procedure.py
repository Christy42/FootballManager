from abc import ABC, abstractmethod


class Procedure(ABC):
    def __init__(self, match):
        # Procedure adds itself to the stack when it is created
        self.match = match
        self.match.state.push(self)

    @abstractmethod
    def step(self):
        pass
