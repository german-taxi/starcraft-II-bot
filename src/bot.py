import sys
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from Planners.build import Build, BuildItem
from Managers.army_manager import ArmyManager
from Managers.worker_manager import WorkerManager
from Managers.scouting_manager import ScoutingManager
# from src.Planners.build import Build, BuildItem
# from src.Managers.army_manager import ArmyManager
# from src.Managers.worker_manager import WorkerManager
# from src.Managers.scouting_manager import ScoutingManager

print(sys.version)

map_name = "AcropolisLE"


class MacroBot(BotAI):
    def __init__(self):
        super().__init__()
        self.unit_by_tag = {}
        self.next_item = None
        self.w_managers = []
        self.a_managers = []
        self.unit_by_tag = {}
        self.danger_map = None
        self.defended_area_map = None
        self.time_to_travel = None
        self.build = None
        self.fast_iteration_speed = 1
        self.medium_iteration_speed = 3
        self.slow_iteration_speed = 15
        self.s_managers = []
        self.waiting_for_structures = []

    def get_unit_by_tag(self, tag):
        unit = self.unit_by_tag.get(tag)
        if unit is None:
            # print("unit not found")  # Debug
            return None
        return unit

    def get_units_by_tag(self, tags):
        units = Units([], self)
        for tag in tags:
            unit = self.get_unit_by_tag(tag)
            if unit is not None:
                units.append(unit)
        return units

    async def on_unit_created(self, unit: Unit):
        self.unit_by_tag[unit.tag] = unit

        if unit.type_id == UnitTypeId.SCV:
            for w_manager in self.w_managers:
                if self.get_unit_by_tag(w_manager.base_tag).position.is_closer_than(10, unit):
                    w_manager.add_worker_tag(unit.tag)
                    break
            else:
                print("Didn't find close worker manager")

    async def on_building_construction_complete(self, unit: Unit):
        print("Building complete: " + str(unit.type_id))
        if unit.type_id == UnitTypeId.REFINERY:
            for waiting_for_structure in self.waiting_for_structures:
                if unit.distance_to(waiting_for_structure[1]) < 3:
                    waiting_for_structure[0].building_tag = unit.tag
                    self.waiting_for_structures.pop(0)
                    print("Refinery tagged")
                    break
            else:
                print("Refinery not found")

    async def on_building_construction_started(self, unit: Unit):
        self.unit_by_tag[unit.tag] = unit

        if unit.type_id == UnitTypeId.COMMANDCENTER:
            for w_manager in self.w_managers:
                if w_manager.base_tag is None:
                    w_manager.set_base_tag(unit.tag)
                    print("Base tagged, on empty manager")
                    break
            else:
                print("No w_manager found, adding new one")
                self.w_managers.append(WorkerManager(self, unit.tag))

    async def on_unit_destroyed(self, unit_tag: int):
        pass

        # found = False
        # for w_manager in self.w_managers:
        #     found = w_manager.remove_worker(unit_tag)
        #     if found:
        #         break
        # if not found:
        #     print("Unit not found")
        # search in other managers

    async def on_start(self):
        # why doesn't work with all_my_units?
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        self.w_managers.append(WorkerManager(self, self.townhalls[0].tag))
        self.a_managers.append(ArmyManager(self))
        self.s_managers.append(ScoutingManager(self))

        # TODO: Future features:
        # 1. self.danger_map = DangerMap(self, [640, 640])
        # 2. self.defended_area_map = DefendedAreaMap(self, [640, 640])
        # 3. self.time_to_travel = TimeToTravel(self)

        self.build = Build(self)

        # Crazy build bro
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SUPPLYDEPOT, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))

        # Orbital command
        self.build.add_item(BuildItem(UnitTypeId.REAPER, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.COMMANDCENTER, True))
        self.build.add_item(BuildItem(UnitTypeId.SUPPLYDEPOT, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.MARINE, False))
        self.build.add_item(BuildItem(UnitTypeId.FACTORY, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))

        # Reactor on Barracks
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.STARPORT, True))

        # Orbital command
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.HELLION, False))
        self.build.add_item(BuildItem(UnitTypeId.HELLION, False))

        # Tech lab on Barracks
        self.build.add_item(BuildItem(UnitTypeId.SUPPLYDEPOT, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.HELLION, False))
        self.build.add_item(BuildItem(UnitTypeId.HELLION, False))

        # Stim pack on Barracks
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.COMMANDCENTER, True))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))

        # self.build.add_item(BuildItem(UnitTypeId.SCV, False))
        # self.build.add_item(BuildItem(UnitTypeId.FACTORY, True))
        # self.build.add_item(BuildItem(UnitTypeId.COMMANDCENTER, True))
        # self.build.add_item(BuildItem(UnitTypeId.STARPORT, True))
        # self.build.add_item(BuildItem(UnitTypeId.HELLION, False))
        # self.build.add_item(BuildItem(UnitTypeId.MEDIVAC, False))

        self.next_item = self.build.get_next_item()

    # TODO: add more items to build
    async def on_step(self, iteration: int):
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}

        if iteration % self.fast_iteration_speed == 0:
            for w_manager in self.w_managers:
                w_manager.update()

            if self.next_item:
                if self.can_afford(self.next_item.item_ID):
                    succeeded = await self.produce(self.next_item)
                    if succeeded:
                        print("Producing: " + str(self.next_item.item_ID))
                        self.next_item = self.build.get_next_item()
            else:
                self.build.add_item(BuildItem(UnitTypeId.SCV, False))
                self.build.add_item(BuildItem(UnitTypeId.MARINE, False))
                self.next_item = self.build.get_next_item()

            for s_manager in self.s_managers:
                await s_manager.scout()

        if iteration % self.medium_iteration_speed == 0:
            pass

        if iteration % self.slow_iteration_speed == 0:
            pass

    async def produce(self, unit):
        succeeded = False
        train_structure_types = UNIT_TRAINED_FROM[unit.item_ID]
        # print("train_structure_type: " + str(train_structure_types))  # Debug

        if unit.is_structure:
            tech_requirement = self.tech_requirement_progress(unit.item_ID)
            if tech_requirement == 1:
                succeeded = await self.w_managers[0].build_structure(unit)
            return succeeded

        for train_structure_type in train_structure_types:
            for structure in self.structures(train_structure_type):
                if structure.is_idle:
                    structure.train(unit.item_ID)
                    succeeded = True
                    break

        return succeeded


if __name__ == "__main__":
    run_game(maps.get(map_name), [
        Bot(Race.Terran, MacroBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)
