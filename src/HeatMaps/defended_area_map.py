import numpy as np
from sc2.ids.ability_id import AbilityId

from sc2.units import Units


class DefendedAreaMap:
    def __init__(self, bot, map_size):
        self.bot = bot
        self.map_size = map_size

    def update(self):
        for unit in self.bot.unit_by_tag:
            if unit.is_mine:
                self.add_defended_zone(unit.position, self.get_radius(unit))

    def add_defended_zone(self, unit_position, radius):
        pass

    @staticmethod
    def get_radius(unit):
        return 0
