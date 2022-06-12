import random
from sc2 import position
from sc2.ids.unit_typeid import UnitTypeId

from src.Managers.manager import Manager


# It's a class that manages the scouting system
class ScoutingManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.__bot = bot

    async def scout(self):
        """
        If there are any SCVs, send the first one to a random location near the enemy base
        """
        if len(self.__bot.units(UnitTypeId.SCV)) > 0:
            scout = self.__bot.units(UnitTypeId.SCV)[0]
            if scout.is_idle:
                enemy_location = self.__bot.enemy_start_locations[0]
                move_to = self.__random_location_variance(enemy_location)
                scout.move(move_to)
                print("Scout commanded to move to: " + str(move_to))

    def __random_location_variance(self, enemy_start_location):
        """
        It takes the enemy start location, adds a random number between -20 and 20 to the x and y
        coordinates, then divides that number by 100 and multiplies it by the enemy start location

        Args:
          enemy_start_location: This is the location of the enemy base.

        Returns:
          The go_to variable is being returned.
        """
        x = enemy_start_location[0]
        y = enemy_start_location[1]

        x += ((random.randrange(-20, 20))/100) * enemy_start_location[0]
        y += ((random.randrange(-20, 20))/100) * enemy_start_location[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.__bot.game_info.map_size[0]:
            x = self.__bot.game_info.map_size[0]
        if y > self.__bot.game_info.map_size[1]:
            y = self.__bot.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x, y)))
        return go_to
