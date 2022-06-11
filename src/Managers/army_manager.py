from sc2.units import Units
from src.Managers.manager import Manager


class ArmyManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.army_units = Units([], self.bot)

    def update(self):
        for unit in self.bot.units:
            if not unit.action_queue:
                self.perform_actions(unit)

    def perform_actions(self, unit):
        pass
