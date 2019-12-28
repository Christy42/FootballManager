from enums import OffenseFormation


# Ordering (changes slightly depending on formation, RB, TEs go in for later WRs
# OT, OG, C, OG, OT, WR1, WR2, WR3, WR4, QB
class OffensePlay:
    def __init__(self, formation, style, assignments, direction, runner, primary, name, com_name, block_style):
        self._assignments = assignments
        self._direction = direction
        self._runner = 0
        self._primary = primary
        self._formation = formation
        self._name = name
        self._commentary_name = com_name
        self._runner = runner
        self._style = style
        self._block_style = block_style

    @property
    def assignments(self):
        return self._assignments

    @property
    def block_style(self):
        return self._block_style
