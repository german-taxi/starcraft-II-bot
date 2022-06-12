from sc2.units import Units
from Managers.manager import Manager
# from src.Managers.manager import Manager


# > This class is a manager for the Army model
class ArmyManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.army_units = Units([], self.bot)

    def update(self):
        """
        If the unit has no actions in its action queue, then perform actions
        """
        for unit in self.bot.units:
            if not unit.action_queue:
                self.perform_actions(unit)

    def perform_actions(self, unit):
        pass
