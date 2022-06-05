import random
from sc2 import position
from sc2.ids.unit_typeid import UnitTypeId


class ScoutingManager:
    def __init__(self, bot):
        #super().__init__()
        self.bot = bot

    async def scout(self):
        if len(self.bot.units(UnitTypeId.SCV)) > 0:
            scout = self.bot.units(UnitTypeId.SCV)[0]
            if scout.is_idle:
                enemy_location = self.bot.enemy_start_locations[0]
                move_to = self.random_location_variance(enemy_location)
                self.bot.do(scout.move(move_to))

    def random_location_variance(self, enemy_start_location):
        x = enemy_start_location[0]
        y = enemy_start_location[1]

        x += ((random.randrange(-20,20))/100) * enemy_start_location[0]
        y += ((random.randrange(-20,20))/100) * enemy_start_location[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.bot.game_info.map_size[0]:
            x = self.bot.game_info.map_size[0]
        if y > self.bot.game_info.map_size[1]:
            y = self.bot.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x, y)))
        return go_to
