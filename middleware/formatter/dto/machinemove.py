class MachineMove:
    def __init__(self, name=None, alias=None, is_hm=False, item=None, version_group=None):
        self.name = name
        self.alias = alias
        self.is_hm = is_hm
        self.item = item
        self.version_group = version_group
        self.different_item = False
        self.different_name = False
        self.different_version_group = False
        self.specifics_vgs = []

    def add_vg_if_possible(self, vg: str):
        if vg not in self.specifics_vgs:
            self.specifics_vgs.append(vg)
