from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import sys

from sc2.unit import Unit

# from src.Manager import Manager
# from src.ProductionQueue import ProductionQueue
# from src.QueueItem import QueueItem
from src.Build import Build
from src.HeatMaps.danger_map import DangerMap
from src.HeatMaps.defender_area_map import DefendedAreaMap
from src.Managers.army_manager import ArmyManager
from src.Managers.worker_manager import WorkerManager
from src.Helpers.time_to_travel_map import TimeToTravel

print(sys.version)

map_name = "AcropolisLE"


#  TODO: Calculate the time it takes to walk somewhere
class WorkerRushBot(BotAI):
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

    def spend_resources(self):
        if self.can_afford(self.next_item.unit_type):
            if self.next_item.unit_type == UnitTypeId.COMMANDCENTER:  # TODO for all buildings
                worker_candidates = self.workers.filter(lambda worker: (worker.is_collecting or worker.is_idle)
                                                        and worker.tag not in self.unit_tags_received_action)
                if worker_candidates:
                    building_worker = worker_candidates.closest_to(
                        self.next_item.location)
                    building_worker.build(
                        self.next_item.unit_type, self.next_item.location)

            elif self.next_item.unit_type == UnitTypeId.SCV:  # SCV only
                for cc in self.townhalls:
                    if cc.is_idle:  # no queue
                        cc.train(self.next_item.unit_type)
                        break

    # async Methods
    async def on_unit_created(self, unit: Unit):
        self.unit_by_tag[unit.tag] = unit
        if unit.type_id == UnitTypeId.SCV:
            for w_manager in self.w_managers:
                if w_manager.base.distance_to(unit) < 10:
                    w_manager.add_workers([unit])
                    break

    async def on_unit_destroyed(self, unit_tag: int):
        found = False
        for w_manager in self.w_managers:
            found = w_manager.remove_worker(unit_tag)
            if found:
                break
        if not found:
            print("Unit not found")
            # search in other managers

    async def on_start(self):
        # why doesn't work with all_my_units?
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        self.w_managers.append(WorkerManager(self, self.townhalls[0]))
        self.a_managers.append(ArmyManager(self))

        self.danger_map = DangerMap(self, [640, 640])
        self.defended_area_map = DefendedAreaMap(self, [640, 640])
        self.build = Build(self)
        # self.time_to_travel = TimeToTravel(self)

    async def on_step(self, iteration: int):
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}

        if iteration % self.fast_iteration_speed == 0:
            for w_manager in self.w_managers:
                w_manager.update()

            next_item = self.build.get_next_item()
            if next_item and self.can_afford(next_item.unit_type):
                self.produce(next_item)


        if iteration % self.medium_iteration_speed == 0:
            pass

        if iteration % self.slow_iteration_speed == 0:
            pass

    def produce(self, unit):
        # find who can produce it
        producer = None

        if unit.is_building():
            self.w_managers[0].build_structure(unit)
        #         if p.can
        #     producer = self.townhalls.closest_to(unit.location)
        # for cc in self.townhalls:
        #     if cc.is_idle:  # no queue
        #         cc.train(unit_type)
        #         break


if __name__ == "__main__":
    run_game(maps.get(map_name), [
        Bot(Race.Terran, WorkerRushBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=True)
