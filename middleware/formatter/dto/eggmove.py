class EggMove:
    def __init__(self, name=None, alias=None, version_groups=None, move=None):
        self.name = name
        self.alias = alias
        self.version_groups = version_groups or []
        self.move = move
        self.parents = []
        self.specifics_vgs = []
        self.different_version_group = False

    def add_vg_if_possible(self, vg: str):
        if vg not in self.specifics_vgs:
            self.specifics_vgs.append(vg)
