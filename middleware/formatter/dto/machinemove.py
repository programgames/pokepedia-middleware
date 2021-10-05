class MachineMove:
    name = None
    alias = None
    is_hm = False
    item = None
    version_group = None
    different_item = False
    different_name = False
    def __init__(self):
        self.specifics_vgs = []
    different_version_group = False
    def add_vg_if_possible(self, vg: str):
        if vg not in self.specifics_vgs:
            self.specifics_vgs.append(vg)
