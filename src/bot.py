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
# from src.WorkerManager import WorkerManager


from manager import Manager
from worker_manager import WorkerManager

print(sys.version)

SCV_BUILD_TIME = 12

#  TODO: Calculate the time it takes to walk somewhere


class WorkerRushBot(BotAI):
    def __init__(self):
        super().__init__()
        self.unit_by_tag = {}
        self.next_item = None
        self.w_managers = []
        self.unit_by_tag = {}

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
        #self.next_item = QueueItem(None)
        # why doesnt work with all_my_units?
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        self.w_managers.append(WorkerManager(self, self.townhalls[0]))
        # self.w_managers[0].add_workers(self.workers)

    async def on_step(self, iteration: int):
        self.unit_by_tag = {unit.tag: unit for unit in self.all_units}
        # if (iteration == 0):
        # self.w_managers[0].redistribute_workers()
        #     self.on_game_start()
        if (iteration % 1 == 0):
            for w_manager in self.w_managers:
                w_manager.update()

            # self.worker_manager.update()
       # print(self.workers.amount, "workers amount")
       # print(self.workers[0].is_carrying_minerals, "is carying minerals")

    # self.worker_manager.update()
        # base_location = self.expansion_locations_list[len(self.townhalls) - 1]
        # if self.minerals >= self.calculate_cost(UnitTypeId.COMMANDCENTER).minerals or (SCV_BUILD_TIME*self.state.score.collection_rate_minerals)/60 >= len(self.townhalls) * self.calculate_cost(UnitTypeId.SCV).minerals:
        #         self.next_item.set_item(UnitTypeId.COMMANDCENTER, location=await self.get_next_expansion())
        # else:
        #     self.next_item.set_item(UnitTypeId.SCV)
        # self.spend_resources()
        # print(self.vespene_geyser.closer_than(10, base_location))
        # print(self.mineral_field.closer_than(10, base_location))

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

            elif self.next_item.unit_type == UnitTypeId.SCV:          # SCV only
                for cc in self.townhalls:
                    if cc.is_idle:      # no queue
                        cc.train(self.next_item.unit_type)
                        break


run_game(maps.get("AcropolisLE"), [
    Bot(Race.Terran, WorkerRushBot()),
    Computer(Race.Protoss, Difficulty.Medium)
], realtime=True)
