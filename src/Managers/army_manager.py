from genericpath import exists
import numpy as np
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId as UnitID
from sc2.units import Units

from manager import Manager
from worker_manager import WorkerManager


class ArmyManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.army_units = Units([], self.bot)
        self.army = None
        self.army_count: int = None
        self.army_build_order = [
            # TODO: add army build order
        ]
        self.army_build_order_step: int = None
        self.army_unit_ids = [
            UnitID.MARINE,
            UnitID.MARAUDER,
            UnitID.SIEGETANK,
            UnitID.SIEGETANKSIEGED,
            UnitID.REAPER,
            UnitID.MEDIVAC,
        ]

    def update(self):
        for unit in self.bot.units:
            if not unit.action_queue:
                self.perform_actions(unit)

    def perform_actions(self, unit):
        pass

    async def train_reaper(self):

        if (self.structures(UnitID.BARRACKS).ready):
            self

    def is_army_unit(self, unitID):
        if (unitID in self.army_unit_ids):
            return True

        return False

    async def build_army(self):
        if (self.minerals < 50):
            return

        if (self.structures(UnitID.BARRACKS).ready):
            marine = self.units(UnitID.MARINE)
            await self.train(marine, 1)

