# It's a class that represents a map of danger values
class DangerMap:
    def __init__(self, bot, map_size):
        self.__bot = bot
        self.__map_size = map_size

    def update(self):
        """
        For each enemy unit, add a danger zone to the map
        """
        for unit in self.__bot.unit_by_tag:
            if unit.is_enemy:
                self.__add_danger_zone(unit.position, self.__get_radius(unit))

    def __add_danger_zone(self):
        pass

    def __get_radius(self):
        return 0
