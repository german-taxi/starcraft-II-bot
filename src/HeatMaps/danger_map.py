# It's a class that represents a map of danger values
class DangerMap:
    def __init__(self, bot, map_size):
        self.bot = bot
        self.map_size = map_size

    def update(self):
        """
        For each enemy unit, add a danger zone to the map
        """
        for unit in self.bot.unit_by_tag:
            if unit.is_enemy:
                self.add_danger_zone(unit.position, self.get_radius(unit))

    def add_danger_zone(self):
        pass

    def get_radius(self):
        return 0
