# It's a bot that builds economy, army and fights the opponent.
import sys

import numpy as np
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty, AIBuild
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.ids.unit_typeid import UnitTypeId as UnitID
from sc2.units import Units
from sc2.dicts.unit_trained_from import UNIT_TRAINED_FROM
from Planners.build import Build, BuildItem
from Managers.attack_manager import AttackManager
from Managers.worker_manager import WorkerManager
from Managers.scouting_manager import ScoutingManager
# from src.Planners.build import Build, BuildItem
# from src.Managers.army_manager import ArmyManager
# from src.Managers.worker_manager import WorkerManager
# from src.Managers.scouting_manager import ScoutingManager


map_name = "AcropolisLE"
print(sys.version)

# This class is the main class that contains all the functions that are used to control the bot, that can
# play the game of Starcraft 2.


class MacroBot(BotAI):
    def __init__(self):
        super().__init__()
        self.unit_by_tag = {}
        self.next_item = None
        self.worker_managers = []
        self.unit_by_tag = {}
        self.danger_map = None
        self.defended_area_map = None
        self.time_to_travel = None
        self.build = None
        self.fast_iteration_speed = 1
        self.medium_iteration_speed = 3
        self.slow_iteration_speed = 15
        self.very_slow_iteration_speed = 250
        self.scouting_managers = []
        self.waiting_for_structures = []
        self.attack_managers = []
        self.build_workers = True
        self.build_depot = True

    def get_unit_by_tag(self, tag):
        """
        It returns the unit object associated with the tag

        Args:
          tag: The tag of the unit you want to get.

        Returns:
          The unit is being returned.
        """
        unit = self.unit_by_tag.get(tag)
        if unit is None:
            # print("unit not found")  # Debug
            return None
        return unit

    def get_units_by_tag(self, tags):
        """
        Get a list of units by their tags

        Args:
          tags: A list of tags to search for.

        Returns:
          A list of units that match the tags.
        """
        units = Units([], self)
        for tag in tags:
            unit = self.get_unit_by_tag(tag)
            if unit is not None:
                units.append(unit)
        return units

    def relocate_army_unit(self, unit: Unit):
        """
        Adds unit to correct manager(to get away from combat or go fight).

        Args:
          unit (Unit): Unit
        """
        # adding unit to non attacking manager
        if unit.health < unit.health_max * 0.5:
            for attack_manager in self.attack_managers:
                if not attack_manager.is_fighting():
                    attack_manager.add_army_tag(unit.tag)
                    print("Added to army manager")
                    break
            else:
                print("No attack_manager found, adding new one")
                self.attack_managers.append(AttackManager(self))
                self.attack_managers[-1].add_army_tag(unit.tag)
        # adding unit to attacking manager
        else:
            for attack_manager in self.attack_managers:
                if attack_manager.is_fighting():
                    attack_manager.add_army_tag(unit.tag)
                    print("Added to army manager")
                    break
            else:
                print("No attack_manager found, adding new one")
                self.attack_managers.append(AttackManager(self))
                self.attack_managers[-1].add_army_tag(unit.tag)

    def should_build_workers(self):
        """
        It checks if the bot should build workers.
        """
        free_worker_space = 0
        for worker_manager in self.worker_managers:
            free_worker_space += worker_manager.get_empty_space()
        if free_worker_space > 0:
            return True
        return False

    def should_build_depot(self):
        """
        It checks if the bot should build a depot.
        """
        supply_already_building = 0

        for unit in self.structures.filter(lambda unit: unit.type_id in {
            UnitID.SUPPLYDEPOT, UnitID.COMMANDCENTER}):
            if not unit.is_ready:   # under construction
                if unit.type_id == UnitID.SUPPLYDEPOT:
                    supply_already_building += 8
                elif unit.build_progress > 0.65:
                    supply_already_building += 10

        for unit in self.placeholders.filter(lambda unit: unit.type_id in {
            UnitID.SUPPLYDEPOT, UnitID.COMMANDCENTER}):
            if not unit.is_ready:   # worker on the way to build it
                if unit.type_id == UnitID.SUPPLYDEPOT:
                    supply_already_building += 8

        # TODO: compare with value based on speed supply is used and projected supply losses
        if self.supply_left + supply_already_building < max(self.supply_cap * 0.13, 4):
            if self.supply_cap + supply_already_building >= 200:
                return False
            return True
        return False

    def recalculate_state(self):
        """
        It recalculates the state of the bot,
        and updates global variables.
        """
        self.build_workers = self.should_build_workers()
        self.build_depot = self.should_build_depot()

    async def on_unit_created(self, unit: Unit):
        """
        If the unit is an SCV, then it will find the closest worker manager and add the SCV to that worker
        manager

        Args:
          unit (Unit): The unit that was created.
        """
        self.unit_by_tag[unit.tag] = unit

        if unit.type_id == UnitTypeId.SCV:
            for w_manager in self.worker_managers:
                if self.get_unit_by_tag(w_manager.base_tag).position.is_closer_than(10, unit):
                    w_manager.add_worker_tag(unit.tag)
                    break
            else:
                print("Didn't find close worker manager")

        if unit.type_id in [UnitID.MARINE, UnitID.SIEGETANK, UnitID.MEDIVAC, UnitID.REAPER, UnitID.SIEGETANKSIEGED, UnitID.HELLION]:
            self.attack_managers[0].add_army_tag(unit.tag)

    async def on_building_construction_complete(self, unit: Unit):
        """
        When a refinery is built, it checks if there is a worker waiting for it, and if so, it tags the
        refinery to the worker.

        Args:
          unit (Unit): Unit
        """
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
        """
        If a command center is built, it will check if there is a worker manager that has no base tag. If
        there is, it will set the base tag to the command center's tag. If there isn't, it will create a new
        worker manager and set the base tag to the command center's tag.

        Args:
          unit (Unit): Unit
        """
        self.unit_by_tag[unit.tag] = unit

        if unit.type_id == UnitTypeId.COMMANDCENTER:
            for w_manager in self.worker_managers:
                if w_manager.base_tag is None:
                    w_manager.set_base_tag(unit.tag)
                    print("Base tagged, on empty manager")
                    break
            else:
                print("No w_manager found, adding new one")
                self.worker_managers.append(WorkerManager(self, unit.tag))

    async def on_unit_destroyed(self, unit_tag: int):
        """
        "If a worker is destroyed, remove it from the worker manager."

        The function is called when a worker is destroyed. It loops through all the worker managers and
        calls the remove_worker function. If the worker is found, it is removed from the worker manager.
        If the worker is not found, it prints "Unit not found"

        Args:
          unit_tag (int): The tag of the unit that was destroyed.
        """
        removed = False
        for w_manager in self.worker_managers:
            removed = w_manager.remove_mineral_field(unit_tag)
            if removed:
                break
        if not removed:
            for w_manager in self.worker_managers:
                removed = w_manager.remove_worker_tag(unit_tag)
                if removed:
                    break
        if not removed:
            for w_manager in self.worker_managers:
                if w_manager.base_tag == unit_tag:
                    w_manager.base_tag = None
                    removed = True
                    print("Base removed")
                    break
        if not removed:
            for attack_manager in self.attack_managers:
                removed = attack_manager.remove_army_tag(unit_tag)
                if removed:
                    break
        if not removed:
            pass

    async def on_start(self):
        """
        The function is called when the game starts. It creates a dictionary of all the units in the game
        and assigns them a tag. It also creates a worker manager, an army manager, and a scouting manager
        """
        # why doesn't work with all_my_units?
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        self.worker_managers.append(WorkerManager(self, self.townhalls[0].tag))
        self.attack_managers.append(AttackManager(self))
        self.attack_managers.append(AttackManager(self, True))
        self.scouting_managers.append(ScoutingManager(self))

        # TODO: Future features:
        # 1. self.danger_map = DangerMap(self, [640, 640])
        # 2. self.defended_area_map = DefendedAreaMap(self, [640, 640])
        # 3. self.time_to_travel = TimeToTravel(self)

        # Creating a build order for the bot to follow.
        self.build = Build(self)

        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.COMMANDCENTER, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.COMMANDCENTER, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.REFINERY, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))
        self.build.add_item(BuildItem(UnitTypeId.BARRACKS, True))

    async def update_build(self):
        """
        The function is called every frame. it manages all things related to the build order.
        """
        item_to_build = self.build.first_item()
        if self.build_workers and self.can_afford(UnitID.SCV):
            succeeded = await self.produce(BuildItem(UnitTypeId.SCV, False))
        if self.build_depot and item_to_build and item_to_build.item_ID != UnitTypeId.SUPPLYDEPOT:
            self.build.add_to_start(BuildItem(UnitTypeId.SUPPLYDEPOT, True))
            print("Added supply depot to start")
            self.build_depot = False

        succeeded = await self.produce(BuildItem(UnitTypeId.REAPER, False))

        if item_to_build:
            if self.can_afford(item_to_build.item_ID):
                succeeded = await self.produce(item_to_build)
                if succeeded:
                    print("Producing: " + str(item_to_build.item_ID))
                    self.build.get_next_item()
        else:
            self.build.add_item(BuildItem(UnitTypeId.SCV, False))
            self.build.add_item(BuildItem(UnitTypeId.MARINE, False))

    def update_worker_managers(self):
        """
        The function is called every frame. It updates all the worker managers.
        """
        for worker_manager in self.worker_managers:
            worker_manager.update()

    def update_attack_managers(self):
        for attack_manager in self.attack_managers:
            if attack_manager.army_count > 10:
                attack_manager.update(True)
            attack_manager.update()

    def update_scouting_managers(self):
        for s_manager in self.scouting_managers:
            s_manager.update()

    async def on_step(self, iteration: int):
        """
        The on_step function is called every iteration of the game. The iteration variable is the number of
        iterations that have passed since the game started. The iteration variable is used to determine how
        often certain functions are called

        Args:
          iteration (int): int
        """
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        # for item in self.build.build_list:
        #     print(item.item_ID)
        # if iteration == 0:
            
            
        #     await self._client.debug_create_unit([[UnitTypeId.REAPER, 5, self._game_info.map_center, 1]])
        #     self.attack_managers[0].update(True)

        if iteration % self.fast_iteration_speed == 0:
            self.recalculate_state()
            self.update_worker_managers()
            await self.update_build()
            self.update_scouting_managers()
            self.update_attack_managers()

        if iteration % self.medium_iteration_speed == 0:
            pass

        if iteration % self.slow_iteration_speed == 0:
            pass

        '''

        very_slow_iteration_speed helps to add one unit to scouting manager once in a minute
        
        '''
        if iteration % self.very_slow_iteration_speed == 0:
            self.scouting_managers[0].add_scout_tag(self.workers[0].tag)
            # print(self.scouting_managers[0]._scout_tags)
            self.worker_managers[0].remove_worker_tag(self.workers[0].tag)
            print("Unit is going to scout to enemy base.")

    async def produce(self, unit):
        """
        If the unit is a structure, then check if the tech requirement is met, and if so, build the
        structure. If the unit is not a structure, then check if there is an idle structure that can
        train the unit, and if so, train the unit

        Args:
          unit: The unit to be produced.

        Returns:
          The return value is a boolean value.
        """
        succeeded = False

        # print("train_structure_type: " + str(train_structure_types))  # Debug

        if unit.is_structure:
            tech_requirement = self.tech_requirement_progress(unit.item_ID)
            if tech_requirement == 1:
                succeeded = await self.worker_managers[0].build_structure(unit)
            return succeeded

        train_structure_types = UNIT_TRAINED_FROM[unit.item_ID]
        for train_structure_type in train_structure_types:
            for structure in self.structures(train_structure_type):
                if structure.is_idle and structure.is_ready:
                    structure.train(unit.item_ID)
                    succeeded = True
                    break

        return succeeded


# Running the game with the map and the bot.
if __name__ == "__main__":
    run_game(maps.get(map_name), [
        Bot(Race.Terran, MacroBot()),
        Computer(Race.Protoss, Difficulty.Easy, ai_build=AIBuild.Macro)
    ], realtime=False)
