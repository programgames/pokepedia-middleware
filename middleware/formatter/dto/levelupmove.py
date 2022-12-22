class LevelUpMove:
    def __init__(self, name=None, alias=None):
        self.name = name
        self.alias = alias

        # Attributes for the first column
        self.level1 = None
        self.level1Extra = None
        self.on_evolution1 = None
        self.on_start1 = None

        # Attributes for the second column
        self.level2 = None
        self.level2Extra = None
        self.on_evolution2 = None
        self.on_start2 = None

        # Attributes for the third column
        self.level3 = None
        self.level3Extra = None
        self.on_evolution3 = None
        self.on_start3 = None