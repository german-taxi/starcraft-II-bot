from sc2.ids.unit_typeid import UnitTypeId


class MineralField:
    def __init__(self, bot, tag):
        self.bot = bot
        self.tag = tag
        self.worker_tags = set()
        self.occupation = 0

    def update(self):
        workers = self.bot.get_units_by_tag(self.worker_tags)

        for worker in workers:
            if worker.is_gathering or worker.is_idle:
                if not worker.orders or worker.orders[0].target != self.tag:
                    mineral = self.bot.unit_by_tag.get(self.tag)
                    worker.gather(mineral, queue=False)
                    # print("Send worker to gather, reason wrong target/idle")  # Debug

    def add_worker(self, worker_tag):
        self.worker_tags.add(worker_tag)
        self.occupation += 1

    def remove_worker(self, worker_tag):
        if worker_tag in self.worker_tags:
            self.worker_tags.discard(worker_tag)
            self.occupation -= 1
            return True
        return False

    def get_random_worker_tag(self):
        if self.worker_tags:
            self.occupation -= 1
            return self.worker_tags.pop()
        return None


class GasField(MineralField):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.building_tag = None

    def set_gas_building(self, building_tag):
        self.building_tag = building_tag

    def update(self):
        workers = self.bot.get_units_by_tag(self.worker_tags)

        for worker in workers:
            if worker.is_gathering or worker.is_idle:
                if not worker.orders or worker.orders[0].target != self.building_tag:
                    gas_building = self.bot.unit_by_tag.get(self.building_tag)
                    worker.gather(gas_building, queue=False)
                    # print("Send worker to gather, reason wrong target/idle")  # Debug


#  TODO: micro mules,  Base relocation, Repair ?
class WorkerManager:
    def __init__(self, bot, base_tag=None):
        self.WORKERS_PER_GAS = 3
        self.WORKERS_PER_MINERAL = 2

        self.bot = bot
        self.base_tag = base_tag
        self.mineral_fields = []
        self.gas_fields = []
        self.free_worker_tags = []
        self.building_worker_tags = []
        self.create_collectable_fields()

    def update(self):
        self.fix_idle_buildings_worker()
        self.fix_free_workers()

        for mineral_field in self.mineral_fields:
            mineral_field.update()

        for gas_field in self.gas_fields:
            gas_field.update()

    def create_collectable_fields(self, position=None):
        if position is None:
            position = self.bot.get_unit_by_tag(self.base_tag).position

        if position:
            self.gas_fields.clear()
            self.mineral_fields.clear()
            mineral_fields = self.bot.mineral_field.closer_than(10, position) \
                .sorted(lambda x: x.distance_to(position))

            gas_fields = self.bot.vespene_geyser.closer_than(10, position) \
                .sorted(lambda x: x.distance_to(position))

            for gas_field in gas_fields:
                self.gas_fields.append(GasField(self.bot, gas_field.tag))

            for mineral_field in mineral_fields:
                self.mineral_fields.append(MineralField(self.bot, mineral_field.tag))

    def set_base_tag(self, base_tag):
        self.base_tag = base_tag

    def add_worker_tag(self, worker_tag):
        self.free_worker_tags.append(worker_tag)

    def remove_worker_tag(self, worker_tag):
        removed = False
        for mineral_field in self.mineral_fields:
            removed = mineral_field.remove_worker(worker_tag)
            if removed:
                break
        return removed

    def fix_idle_buildings_worker(self):
        tags_to_remove = []

        building_workers = self.bot.get_units_by_tag(self.building_worker_tags)
        for building_worker in building_workers:
            if building_worker.is_idle:
                tags_to_remove.append(building_worker.tag)

        for tag in tags_to_remove:
            self.building_worker_tags.remove(tag)
            self.free_worker_tags.append(tag)

    def free_workers_to_mineral(self):
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

    def free_workers_to_gas(self):
        tags_to_remove = []
        for free_worker_tag in self.free_worker_tags:
            for gas_field in self.gas_fields:
                if gas_field.building_tag and gas_field.occupation < self.WORKERS_PER_GAS:
                    gas_field.add_worker(free_worker_tag)
                    tags_to_remove.append(free_worker_tag)
                    # print("Gas field occupation: ", gas_field.occupation) # Debug
                    break
            else:
                break

        for tag in tags_to_remove:
            self.free_worker_tags.remove(tag)

    def transfer_workers(self):
        for w_manager in self.bot.w_managers:
            if self != w_manager:
                empty_space = w_manager.get_empty_space()
                for i in range(empty_space):
                    if len(self.free_worker_tags) != 0:
                        w_manager.add_worker_tag(self.free_worker_tags.pop())
                    else:
                        break
        # if len(self.free_worker_tags) != 0:   # Debug
        #     print("Not all workers were redistributed! Left: ", len(self.free_worker_tags))   # Debug

    def fix_free_workers(self):
        if self.get_empty_space() == 0:
            self.transfer_workers()
            return
        self.free_workers_to_gas()
        self.free_workers_to_mineral()

    def get_empty_space(self):
        space = 0
        for mineral_field in self.mineral_fields:
            space += self.WORKERS_PER_MINERAL - mineral_field.occupation
        for gas_field in self.gas_fields:
            if gas_field.building_tag:
                space += self.WORKERS_PER_GAS - gas_field.occupation
        return space

    def get_worker_for_structure(self, target):
        for mineral in reversed(self.mineral_fields):
            random_worker_tag = mineral.get_random_worker_tag()
            if random_worker_tag is not None:
                return self.bot.get_unit_by_tag(random_worker_tag)
        for gas in reversed(self.gas_fields):
            random_worker_tag = gas.get_random_worker_tag()
            if random_worker_tag is not None:
                return self.bot.get_unit_by_tag(random_worker_tag)
        return None

    async def build_gas_building(self, structure):
        for gas_field in self.gas_fields:
            if gas_field.building_tag is None:
                placement_unit = self.bot.get_unit_by_tag(gas_field.tag)
                if placement_unit:
                    worker = self.get_worker_for_structure(placement_unit.position)
                    if worker:
                        worker.build(structure.item_ID, placement_unit)
                        worker.stop(queue=True)
                        self.building_worker_tags.append(worker.tag)
                        self.bot.waiting_for_structures.append([gas_field, self.bot.get_unit_by_tag(gas_field.tag).position])
                        return True
        return False

    async def build_structure(self, structure):
        if structure.item_ID == UnitTypeId.REFINERY:
            return await self.build_gas_building(structure)
        elif structure.item_ID == UnitTypeId.COMMANDCENTER:
            placement_position = await self.bot.get_next_expansion()
        else:
            map_center = self.bot.game_info.map_center
            position_towards_map_center = self.bot.start_location.towards(map_center, distance=5)
            placement_position = await self.bot.find_placement(structure.item_ID, near=position_towards_map_center,
                                                               placement_step=1)

        if placement_position:
            worker = self.get_worker_for_structure(placement_position)
            if worker:
                worker.build(structure.item_ID, placement_position)
                self.building_worker_tags.append(worker.tag)
                return True
            return False
        else:
            # TODO: Handeling of this
            print("There is no placement position")
            return False
