from enums import GenOff
from plays.field_loc import *
from plays.route import RouteRead


class Coverage:
    def __init__(self, area=None, target=None, blitz=False):
        self._area = area
        self._target = target
        self._blitz = blitz

    def amend_area(self, routes: RouteRead):  # Run this for each if area is None at start of a play?
        if self._area is None:
            if type(routes.assignments[self._target]) == FieldLocation:
                self._area = routes.assignments[self._target]
            else:  # If receiver is blocking then blitz
                self._area = BACK_CENTER
                self._target = GenOff.QB
                self._blitz = True

    @property
    def area(self):
        return self._area

    @property
    def target(self):
        return self._target

    @property
    def blitz(self):
        return self._blitz


CENTER_RUSH = Coverage(area=BACK_CENTER, target=GenOff.QB, blitz=True)
LEFT_RUSH = Coverage(area=BACK_CENT_L, target=GenOff.QB, blitz=True)
RIGHT_RUSH = Coverage(area=BACK_CENT_R, target=GenOff.QB, blitz=True)
MAN_1 = Coverage(area=None, target=GenOff.REC1, blitz=False)
MAN_2 = Coverage(area=None, target=GenOff.REC2, blitz=False)
MAN_3 = Coverage(area=None, target=GenOff.REC3, blitz=False)
MAN_4 = Coverage(area=None, target=GenOff.REC4, blitz=False)
MAN_5 = Coverage(area=None, target=GenOff.REC5, blitz=False)
MAN_6 = Coverage(area=None, target=GenOff.QB, blitz=False)  # Spy on the QB
BACK_RIGHT_C = Coverage(area=BACK_RIGHT, target=None, blitz=False)
BACK_CENT_R_C = Coverage(area=BACK_CENT_R, target=None, blitz=False)
BACK_CENTER_C = Coverage(area=BACK_CENTER, target=None, blitz=False)
BACK_CENT_L_C = Coverage(area=BACK_CENT_L, target=None, blitz=False)
BACK_LEFT_C = Coverage(area=BACK_LEFT, target=None, blitz=False)
SHORT_RIGHT_C = Coverage(area=SHORT_RIGHT, target=None, blitz=False)
SHORT_CENT_R_C = Coverage(area=SHORT_CENT_R, target=None, blitz=False)
SHORT_CENTER_C = Coverage(area=SHORT_CENTER, target=None, blitz=False)
SHORT_CENT_L_C = Coverage(area=SHORT_CENT_L, target=None, blitz=False)
SHORT_LEFT_C = Coverage(area=SHORT_LEFT, target=None, blitz=False)
MID_RIGHT_C = Coverage(area=MID_RIGHT, target=None, blitz=False)
MID_CENT_R_C = Coverage(area=MID_CENT_R, target=None, blitz=False)
MID_CENTER_C = Coverage(area=MID_CENTER, target=None, blitz=False)
MID_CENT_L_C = Coverage(area=MID_CENT_L, target=None, blitz=False)
MID_LEFT_C = Coverage(area=MID_LEFT, target=None, blitz=False)
LONG_RIGHT_C = Coverage(area=LONG_RIGHT, target=None, blitz=False)
LONG_CENT_R_C = Coverage(area=LONG_CENT_R, target=None, blitz=False)
LONG_CENTER_C = Coverage(area=LONG_CENTER, target=None, blitz=False)
LONG_CENT_L_C = Coverage(area=LONG_CENT_L, target=None, blitz=False)
LONG_LEFT_C = Coverage(area=LONG_LEFT, target=None, blitz=False)
FAR_RIGHT_C = Coverage(area=FAR_RIGHT, target=None, blitz=False)
FAR_CENT_R_C = Coverage(area=FAR_CENT_R, target=None, blitz=False)
FAR_CENTER_C = Coverage(area=FAR_CENTER, target=None, blitz=False)
FAR_CENT_L_C = Coverage(area=FAR_CENT_L, target=None, blitz=False)
FAR_LEFT_C = Coverage(area=FAR_LEFT, target=None, blitz=False)
DEEP_RIGHT_C = Coverage(area=DEEP_RIGHT, target=None, blitz=False)
DEEP_CENT_R_C = Coverage(area=DEEP_CENT_R, target=None, blitz=False)
DEEP_CENTER_C = Coverage(area=DEEP_CENTER, target=None, blitz=False)
DEEP_CENT_L_C = Coverage(area=DEEP_CENT_L, target=None, blitz=False)
DEEP_LEFT_C = Coverage(area=DEEP_LEFT, target=None, blitz=False)
