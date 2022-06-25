from sc2.ids.unit_typeid import UnitTypeId
#from Managers.manager import Manager
from src.Other.gas_field import GasField
from src.Other.mineral_field import MineralField
from src.Managers.manager import Manager


#  TODO: 1. micro_mules,  2. base_relocation, repair?
# It manages workers
class WorkerManager(Manager):
    def __init__(self, bot, base_tag=None):
        super().__init__()
        self.WORKERS_PER_GAS = 3
        self.WORKERS_PER_MINERAL = 2

        self.bot = bot
        self.base_tag = base_tag
        self.mineral_fields = []
        self.gas_fields = []
        self.free_worker_tags = []
        self.building_worker_tags = []
        self.update_collectable_fields()

    def update(self):
        """
        The function updates the mineral fields and gas fields
        """
        self.__fix_idle_buildings_worker()
        self.__fix_free_workers()

        for mineral_field in self.mineral_fields:
            mineral_field.update()

        for gas_field in self.gas_fields:
            gas_geyser = self.bot.unit_by_tag.get(gas_field.tag)
            if gas_geyser and gas_geyser.has_vespene:
                gas_field.update()
            else:
                gas_field.set_gas_building(None)
                for _ in range(gas_field.occupation):
                    self.free_worker_tags.append(gas_field.get_random_worker_tag())

    def get_empty_space(self):
        """
        It returns the number of workers that can be assigned to a mineral or gas field

        Returns:
          The number of workers that can be assigned to a mineral or gas field.
        """
        space = 0
        for mineral_field in self.mineral_fields:
            space += self.WORKERS_PER_MINERAL - mineral_field.occupation
        for gas_field in self.gas_fields:
            if gas_field.building_tag not in [None, 1]:
                space += self.WORKERS_PER_GAS - gas_field.occupation
        return space

    def remove_mineral_field(self, mineral_field_tag):
        """
        It removes a mineral field from the list of mineral fields.
        """
        for mineral_field in self.mineral_fields:
            if mineral_field.tag == mineral_field_tag:
                for _ in range(mineral_field.occupation):
                    self.free_worker_tags.append(mineral_field.get_random_worker_tag())
                self.mineral_fields.remove(mineral_field)
                return True
        return False

    def update_collectable_fields(self, position=None):
        """
        It creates a list of mineral fields and gas fields that are close to the base

        Args:
          position: The position of the base.
        """
        if position is None:
            position = self.bot.get_unit_by_tag(self.base_tag).position

        if position:
            for mineral_field in self.mineral_fields:
                for _ in range(mineral_field.occupation):
                    self.free_worker_tags.append(mineral_field.get_random_worker_tag())
            for gas_field in self.gas_fields:
                for _ in range(gas_field.occupation):
                    self.free_worker_tags.append(gas_field.get_random_worker_tag())

            self.gas_fields.clear()
            self.mineral_fields.clear()
            mineral_fields = self.bot.mineral_field.closer_than(15, position) \
                .sorted(lambda x: x.distance_to(position))

            gas_fields = self.bot.vespene_geyser.closer_than(15, position) \
                .sorted(lambda x: x.distance_to(position))

            print("Found {} mineral fields and {} gas fields".format(len(mineral_fields), len(gas_fields)))     # Debug
            for gas_field in gas_fields:
                self.gas_fields.append(GasField(self.bot, gas_field.tag))

            for mineral_field in mineral_fields:
                self.mineral_fields.append(
                    MineralField(self.bot, mineral_field.tag))

    def set_base_tag(self, base_tag):
        """
        This function sets the base tag of the object to the base tag passed in as an argument

        Args:
          base_tag: The base tag for the image.
        """
        self.base_tag = base_tag
        self.update_collectable_fields()

    def add_worker_tag(self, worker_tag):
        """
        It adds a worker tag to the list of free worker tags.

        Args:
          worker_tag: A string that identifies the worker.
        """
        self.free_worker_tags.append(worker_tag)

    def remove_worker_tag(self, worker_tag):
        """
        If a worker is assigned to a mineral field, remove the worker from the mineral field

        Args:
          worker_tag: The tag of the worker to remove.

        Returns:
          A boolean value.
        """
        removed = False
        for mineral_field in self.mineral_fields:
            removed = mineral_field.remove_worker(worker_tag)
            if removed:
                break
        return removed

    def remove_random_worker(self):
        """
        It removes a random worker from the list of free workers. Or mineral_field/gas_field if there is no free workers.

        Returns:
          The tag of the worker that was removed.
        """
        if len(self.free_worker_tags) > 0:
            return self.free_worker_tags.pop()
        for mineral_field in self.mineral_fields:
            if mineral_field.occupation != 0:
                return mineral_field.get_random_worker_tag()
        for gas_field in self.gas_fields:
            if gas_field.occupation != 0:
                return gas_field.get_random_worker_tag()
        return None

    def __fix_idle_buildings_worker(self):
        """
        If a worker is idle, remove it from the list of building workers and add it to the list of free
        workers
        """
        tags_to_remove = []

        building_workers = self.bot.get_units_by_tag(self.building_worker_tags)
        for building_worker in building_workers:
            if building_worker.is_idle:
                tags_to_remove.append(building_worker.tag)

        for tag in tags_to_remove:
            self.building_worker_tags.remove(tag)
            self.free_worker_tags.append(tag)

    def __free_workers_to_mineral(self):
        """
        For each free worker, find the first mineral field that has less than 3 workers and assign the
        worker to it
        """
        tags_to_remove = []
        for free_worker_tag in self.free_worker_tags:
            for mineral_field in self.mineral_fields:
                if mineral_field.occupation < self.WORKERS_PER_MINERAL:
                    mineral_field.add_worker(free_worker_tag)
                    tags_to_remove.append(free_worker_tag)
                    break
            else:
                break
        for tag in tags_to_remove:
            self.free_worker_tags.remove(tag)

    def __free_workers_to_gas(self):
        """
        If there are free workers and gas fields that need workers, assign the free workers to the gas
        fields
        """
        tags_to_remove = []
        for free_worker_tag in self.free_worker_tags:
            for gas_field in self.gas_fields:
                if gas_field.building_tag not in [None, 1] and gas_field.occupation < self.WORKERS_PER_GAS:
                    refinery = self.bot.get_unit_by_tag(gas_field.building_tag)
                    if refinery.build_progress == 1:
                        gas_field.add_worker(free_worker_tag)
                        tags_to_remove.append(free_worker_tag)
                        # print("Gas field occupation: ", gas_field.occupation) # Debug
                    break
            else:
                break

        for tag in tags_to_remove:
            self.free_worker_tags.remove(tag)

    def __transfer_workers(self):
        """
        If there are free workers in the current worker manager, then transfer them to the other worker
        managers until there are no more free workers
        """
        for w_manager in self.bot.worker_managers:
            if self != w_manager:
                empty_space = w_manager.get_empty_space()
                for i in range(empty_space):
                    if len(self.free_worker_tags) != 0:
                        w_manager.add_worker_tag(self.free_worker_tags.pop())
                    else:
                        break
        #if len(self.free_worker_tags) != 0:
            #print("Not all workers were redistributed! Left: ", len(self.free_worker_tags))   # Debug
            # print("Sending jobless to war!")   # Debug

            # for worker_tag in self.free_worker_tags:
            #     self.bot.attack_managers[0].add_army_tag(worker_tag)
            #     self.free_worker_tags.remove(worker_tag)

    def __fix_free_workers(self):
        """
        If there is no empty space, transfer workers. Otherwise, send workers to gas or minerals

        Returns:
          The number of workers that are not assigned to a mineral patch or a gas refinery.
        """
        if self.get_empty_space() == 0:
            self.__transfer_workers()
            return
        if len(self.free_worker_tags) == 0:
            return
        self.__free_workers_to_gas()
        self.__free_workers_to_mineral()

    def __get_worker_for_structure(self, target):
        """
        It returns a random worker from the mineral fields, and if there are no workers in the mineral
        fields, it returns a random worker from the gas fields

        Args:
          target: The target structure that we want to get a worker for.

        Returns:
          A worker unit.
        """
        if len(self.free_worker_tags) != 0:
            return self.bot.get_unit_by_tag(self.free_worker_tags.pop())
        for mineral in reversed(self.mineral_fields):
            random_worker_tag = mineral.get_random_worker_tag()
            if random_worker_tag is not None:
                return self.bot.get_unit_by_tag(random_worker_tag)
        for gas in reversed(self.gas_fields):
            random_worker_tag = gas.get_random_worker_tag()
            if random_worker_tag is not None:
                return self.bot.get_unit_by_tag(random_worker_tag)
        return None

    async def __build_gas_building(self, structure):
        """
        If there is a gas field that is not being built on, find a worker to build on it

        Args:
          structure: The structure you want to build.

        Returns:
          True or False
        """
        for gas_field in self.gas_fields:
            if gas_field.building_tag is None:
                placement_unit = self.bot.get_unit_by_tag(gas_field.tag)
                if placement_unit:
                    # if placement_unit.is_snapshot:print("Gas field is snapshot!")   # Debug
                    # if placement_unit.is_memory:print("Gas field is memory!")   # Debug
                    worker = self.__get_worker_for_structure(
                        placement_unit.position)
                    if worker:
                        worker.build(structure.item_ID, placement_unit)
                        worker.stop(queue=True)
                        self.building_worker_tags.append(worker.tag)
                        self.bot.waiting_for_structures.append(
                            [gas_field, self.bot.get_unit_by_tag(gas_field.tag).position])
                        gas_field.building_tag = 1      # Set tag to 1 to indicate that it is reserved for a structure
                        # TODO: Remove this if unit dies before building starts
                        return True
                    # else: print("No worker found for gas field!")  # Debug
                else:
                    self.__fix_gas_tags()
                    # print("trying to update gas tag")  # Debug
        return False

    def __fix_gas_tags(self):
        """
        Update the gas tags to match the current state of the gas fields. Sometimes gas geyser can have memory tag
        :return: void
        """
        position = self.bot.get_unit_by_tag(self.base_tag).position
        gas_fields = self.bot.vespene_geyser.closer_than(15, position) \
            .sorted(lambda x: x.distance_to(position))
        for i, gas_field in enumerate(gas_fields):
            self.gas_fields[i].update_gas_tag(gas_field.tag)

    async def build_structure(self, structure):
        """
        If the structure is a refinery, build it at the gas geyser. If it's a command center, build it
        at the next expansion. Otherwise, build it 11 units away from the map center

        Args:
          structure: The structure to build

        Returns:
          A boolean value
        """
        if structure.item_ID == UnitTypeId.REFINERY:
            return await self.__build_gas_building(structure)
        if structure.item_ID == UnitTypeId.COMMANDCENTER:
            placement_position = await self.bot.get_next_expansion()
        else:
            map_center = self.bot.game_info.map_center
            base = self.bot.get_unit_by_tag(self.base_tag)
            position_towards_map_center = base.position.towards(
                map_center, distance=11)
            placement_position = await self.bot.find_placement(structure.item_ID, near=position_towards_map_center,
                                                               placement_step=4)

        # TODO: Handle the case of placement_position being defined, but there being no position available
        if placement_position:
            worker = self.__get_worker_for_structure(placement_position)
            if worker:
                worker.build(structure.item_ID, placement_position)
                self.building_worker_tags.append(worker.tag)
                return True
            return False

        print("There is no placement position")
        return False
