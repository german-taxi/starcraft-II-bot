# It's a class that stores a map of defended areas
class DefendedAreaMap:
    def __init__(self, bot, map_size):
        self.__bot = bot
        self.map_size = map_size

    def update(self):
        """
        For each unit that is mine, add a defended zone around it with a radius equal to the unit's
        radius
        """
        for unit in self.__bot.unit_by_tag:
            if unit.is_mine:
                self.__add_defended_zone(unit.position, self.__get_radius(unit))

    def __add_defended_zone(self):
        pass

    def __get_radius(self):
        return 0
