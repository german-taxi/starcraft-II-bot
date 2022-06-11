class DefendedAreaMap:
    def __init__(self, bot, map_size):
        self.bot = bot
        self.map_size = map_size

    def update(self):
        for unit in self.bot.unit_by_tag:
            if unit.is_mine:
                self.add_defended_zone(unit.position, self.get_radius(unit))

    def add_defended_zone(self):
        pass

<<<<<<< HEAD
    def get_radius(self):
=======
    @staticmethod
    def get_radius(unit):
>>>>>>> 0895e930b7488498855a235a65f73985fa1c066e
        return 0
