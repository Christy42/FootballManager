class OffenseFormation:
    def __init__(self, no_tes=0, no_wrs=0, no_rbs=0, no_k=0, no_gnr=0, shotgun=False, kicking=False):
        self._no_tes = no_tes
        self._no_wrs = no_wrs
        self._no_rbs = no_rbs
        self._no_k = no_k
        self._no_gnr = no_gnr
        self._shotgun = shotgun
        self._kicking = kicking

    @property
    def no_tes(self):
        return self._no_tes

    @property
    def no_wrs(self):
        return self._no_wrs

    @property
    def no_gnr(self):
        return self._no_gnr

    @property
    def no_k(self):
        return self._no_k

    @property
    def kicking(self):
        return self._kicking

    @property
    def no_rbs(self):
        return self._no_rbs


# TODO: Kick formations
SINGLEBACK = OffenseFormation(no_tes=1, no_wrs=3, no_rbs=1, shotgun=False)
I_FORM = OffenseFormation(no_tes=1, no_wrs=2, no_rbs=2, shotgun=False)
SHOTGUN = OffenseFormation(no_tes=1, no_wrs=3, no_rbs=1, shotgun=True)
DOUBLE_TE_SET = OffenseFormation(no_tes=2, no_wrs=2, no_rbs=1, shotgun=False)
SPREAD = OffenseFormation(no_tes=0, no_wrs=4, no_rbs=1, shotgun=True)
KICK_OFF = OffenseFormation(no_rbs=2, no_tes=1, no_k=1, no_gnr=2, kicking=True)
