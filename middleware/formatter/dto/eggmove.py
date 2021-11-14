class EggMove:
    name = None
    alias = None
    version_group = None

    def __init__(self):
        self.specifics_vgs = []

    different_version_group = False
    def add_vg_if_possible(self, vg: str):
        if vg not in self.specifics_vgs:
            self.specifics_vgs.append(vg)
