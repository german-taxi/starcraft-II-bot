# It's a class that stores a map of defended areas
class DefendedAreaMap:
    def __init__(self, bot, map_size):
        self.bot = bot
        self.map_size = map_size

    def update(self):
        """
        For each unit that is mine, add a defended zone around it with a radius equal to the unit's
        radius
        """
        for unit in self.bot.unit_by_tag:
            if unit.is_mine:
                self.add_defended_zone(unit.position, self.get_radius(unit))

    def add_defended_zone(self):
        pass

    def get_radius(self):
        return 0
