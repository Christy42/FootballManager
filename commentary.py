from enums import Event


class Commentary:
    def __init__(self, event: Event, players: list, extra_numb=None):
        self._players = players
        self._event = event
        self._extra_numb = extra_numb

    def to_text(self):
        # Use a lot of if statements as best course here?
        # Use specific classes
        pass


class SingleLine:
    def __init__(self):
        pass

    def create_line(self):
        pass
