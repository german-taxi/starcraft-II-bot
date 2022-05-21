import numpy as np
import sc2
from sc2.ids.ability_id import AbilityId
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
import sys

from sc2.units import Units

from Manager import Manager
from ProductionQueue import ProductionQueue
from QueueItem import QueueItem
from Manager import Manager


#  TODO: Mine, worker micro and mules, Building creation, Base relocation, Repair ?
#  TODO: calculate available mineral fields and gas fields

class WorkerManager(Manager):
    def __init__(self, bot, base=None):
        super().__init__()
        self.bot = bot
        self.base = base
        self.WORKERS_PER_GAS = 3
        self.WORKERS_PER_MINERAL = 2
        self.max_mineral_workers = 0
        self.max_gas_workers = 0
        self.workers = np.empty((0, 2))
        self.workers_target = Units([], self.bot)
        self.mineral_worker_tags = set()  # maybe join with gas workers
        self.gas_workers = []
        self.mules = []
        self.mineral_fields = []
        self.mineral_occupation = np.zeros(8)
        self.gas_fields = []
        self.building_workers = []
        # time_to_walk = mineral_fields.distance_to(self.base.position) / self.mineral_worker.move_speed

    def add_workers(self, workers_to_add, where_to_add=None):
        tags = np.array([[x.tag, None] for x in workers_to_add])
        if where_to_add is None:
            where_to_add = self.workers
        self.workers = np.append(where_to_add, tags, axis=0)
        print(self.workers)
        print(len(self.workers), "workers added")
        self.update_collectable_fields()
        if self.base is not None:
            print("send to work")
            print(tags)
            print(tags[:, 0])
            self.send_to_work(tags[:, 0])
        # else handle, maybe wait or something

    def remove_worker(self, tag):
        pass

    def send_to_work(self, tags):
        if len(self.mineral_worker_tags) < self.max_mineral_workers:
            print(len(self.mineral_worker_tags), self.max_mineral_workers)
            self.find_minerals(tags)
        else:
            print(len(self.mineral_worker_tags), self.max_mineral_workers)
            print("too many mineral workers")
        # or self.find_gas(tags)

    def get_unit_by_tag(self, tag):
        unit = self.bot.unit_by_tag.get(tag)
        if unit is None:   # cant be none anymre since we remove the tag when the unit is destroyed
            print("unit not found")
            return None
        #     self.remove_tag(tag)
        return unit

    def get_units_by_tag(self, tags):
        units = Units([], self.bot)
        for tag in tags:
            unit = self.get_unit_by_tag(tag)
            if unit is not None:
                units.append(unit)
        return units

    def remove_tag(self, tag):
        print("REMOVING TAGGGGGGGGGGGGGG")
        self.workers = np.delete(self.workers, np.where(self.workers[:, 0] == tag), axis=0)
        # self.workers.remove(tag)

    def get_index(self, tag):
        return np.where(self.workers[:, 0] == tag)[0][0]

    def worker_gather(self, worker):
        target_index = self.get_index(worker.tag)
        target_tag = self.workers[target_index, 1]
        target = self.bot.unit_by_tag.get(target_tag)
        worker.gather(target, queue=False)
        # if worker.target_unit is not None:
        #     worker.gather(worker.target_unit, queue=False)
        # else:
        #     pass  # assign new target and send to gather

    def find_minerals(self, free_workers):
        # free_workers = self.workers[:, 0]  ## TODO: add check if worker is already mining
        self.split_workers_to_minerals_(free_workers)

    def update(self):
        #print("update workers")
        self.fix_workers()

    def fix_workers(self):
        workers = self.get_units_by_tag(self.mineral_worker_tags)
        for worker in workers:
            #print(worker.is_carrying_minerals, worker.is_gathering)
            if worker.is_gathering:
                index = self.get_index(worker.tag)
                if worker.orders[0].target != self.workers[index, 1]:
                    self.worker_gather(worker)
                    print("Send worker to gather, reason wrong target")

    def update_info(self, worker, info, i):
        index = self.get_index(worker.tag)
        self.workers[index][i] = info

    def set_base(self, base):
        self.base = base

    def set_base_rally(self, base_rally):
        self.base(AbilityId.RALLY_BUILDING, base_rally)

    # todo: add a check if worker should go to mineral or base first
    def assign_worker(self, worker, target):
        worker.gather(target)

    def build_structure(self, structure, target):
        worker = self.get_worker_for_structure(target)
        if worker:
            worker.build(structure, target)
            # self
            # self.building_workers.append(worker)
        else:
            print("No worker available for building")  # TODO: Handeling of this

    # Get closest Not MINING worker, If have cargo, return then build structure, can remake with closest_to
    def get_worker_for_structure(self, target):
        distance_to_target = [target.distance_to(x) for x in
                              self.mineral_worker_tags]  # only mineral workers for now, TODO: Gas workers
        closest_worker = self.mineral_worker_tags[distance_to_target.index(min(distance_to_target))]
        # self.mineral_workers.closest_to(target)
        return closest_worker

    def update_collectable_fields(self):
        if self.base.position:
            self.mineral_fields = self.bot.mineral_field.closer_than(10, self.base.position) \
                .sorted(lambda x: x.distance_to(self.base.position))

            # maybe dont sort gast fields
            self.gas_fields = self.bot.vespene_geyser.closer_than(10, self.base.position) \
                .sorted(lambda x: x.distance_to(self.base.position))

            self.max_mineral_workers = self.WORKERS_PER_MINERAL * len(self.mineral_fields)
            self.max_gas_workers = self.WORKERS_PER_GAS * len(self.gas_fields)

    def redistribute_workers(self):
        self.split_workers_to_minerals_(self.mineral_worker_tags)

    def get_next_mineral(self):
        if self.mineral_fields:
            for i, mineral in enumerate(self.mineral_fields):
                if self.mineral_occupation[i] < self.WORKERS_PER_MINERAL:
                    return i, mineral
        return None, None ## not sure waht to do here

    # Assigning workers to the closest mineral fields, max 2 workers per field
    def split_workers_to_minerals_(self, workers):
        worker_units = self.get_units_by_tag(workers)
        for _ in range(len(worker_units)):
            i, mineral = self.get_next_mineral()
            closest_worker = worker_units.closest_to(mineral)
            self.update_info(closest_worker, mineral.tag, 1)
            worker_units.remove(closest_worker)
            self.mineral_worker_tags.add(closest_worker.tag)
            self.mineral_occupation[i] += 1

    def split_workers_to_minerals(self, free_worker_tags):
        # make this work when sending workers one by one todo!!!!!!!!!
        free_worker_units = self.get_units_by_tag(free_worker_tags)
        for mineral_field in self.mineral_fields:
            # mineral_field = self.get_unit_by_tag(mineral_field.tag)
            for i in range(self.WORKERS_PER_MINERAL - mineral_field.assigned_harvesters):
                if len(free_worker_units) > 0:
                    print("Assigning worker to mineral field")
                    closest_worker = free_worker_units.closest_to(mineral_field)
                    self.update_info(closest_worker, mineral_field.tag, 1)
                    free_worker_units.remove(closest_worker)
                    self.mineral_worker_tags.add(closest_worker.tag)
                else:
                    return None
        return free_worker_units
