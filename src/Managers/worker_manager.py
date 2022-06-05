from sc2.ids.unit_typeid import UnitTypeId


class MineralField:
    def __init__(self, bot, tag):
        self.bot = bot
        self.tag = tag
        self.mineral_worker_tags = set()
        self.mineral_occupation = 0

    def update(self):
        workers = self.bot.get_units_by_tag(self.mineral_worker_tags)

        for worker in workers:
            if worker.is_gathering or worker.is_idle:
                if not worker.orders or worker.orders[0].target != self.tag:
                    mineral = self.bot.unit_by_tag.get(self.tag)
                    worker.gather(mineral, queue=False)
                    # print("Send worker to gather, reason wrong target/idle")  # Debug

    def add_worker(self, worker_tag):
        self.mineral_worker_tags.add(worker_tag)
        self.mineral_occupation += 1

    def remove_worker(self, worker_tag):
        if worker_tag in self.mineral_worker_tags:
            self.mineral_worker_tags.discard(worker_tag)
            self.mineral_occupation -= 1
            return True
        return False


#  TODO: micro mules,  Base relocation, Repair ?
class WorkerManager:
    def __init__(self, bot, base=None):
        self.bot = bot
        self.mineral_fields = []
        self.gas_fields = []
        self.base = base
        self.free_worker_tags = []
        self.building_worker_tags = []
        self.WORKERS_PER_MINERAL = 2
        self.create_collectable_fields()

    def update(self):
        self.fix_idle_buildings_worker()
        self.fix_free_workers()

        for mineral_field in self.mineral_fields:
            mineral_field.update()

    def create_collectable_fields(self, position=None):
        if position is None:
            position = self.base.position

        if position:
            mineral_fields = self.bot.mineral_field.closer_than(10, position) \
                .sorted(lambda x: x.distance_to(position))

            # maybe don't sort gast fields
            gas_fields = self.bot.vespene_geyser.closer_than(10, position) \
                .sorted(lambda x: x.distance_to(position))

            for mineral_field in mineral_fields:
                self.mineral_fields.append(MineralField(self.bot, mineral_field.tag))

    def set_base(self, base):
        self.base = base

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

    def fix_free_workers(self):
        tags_to_remove = []
        for free_worker_tag in self.free_worker_tags:
            for mineral_field in self.mineral_fields:
                if mineral_field.mineral_occupation < self.WORKERS_PER_MINERAL:
                    mineral_field.add_worker(free_worker_tag)
                    tags_to_remove.append(free_worker_tag)
                    break
            else:
                break
        for tag in tags_to_remove:
            self.free_worker_tags.remove(tag)
        if len(self.free_worker_tags) != 0:
            print("Not all workers were assigned! Left: ", len(self.free_worker_tags))
            # TODO: pass to other worker manager

    def get_worker_for_structure(self, target):
        all_workers = self.bot.all_units(UnitTypeId.SCV)
        closest_worker = all_workers.closest_to(target)   # self.mineral_worker_tags >- self.bot.workers

        return closest_worker

    async def build_structure(self, structure):
        map_center = self.bot.game_info.map_center
        position_towards_map_center = self.bot.start_location.towards(map_center, distance=5)
        placement_position = await self.bot.find_placement(structure.item_ID, near=position_towards_map_center,
                                                           placement_step=1)

        worker = self.get_worker_for_structure(placement_position)

        if worker and placement_position:
            removed = self.remove_worker_tag(worker.tag)
            if removed:
                worker.build(structure.item_ID, placement_position)
                self.building_worker_tags.append(worker.tag)
            return True
        else:
            # TODO: Handeling of this
            print("No worker available for building, or there is no placement position")
            return False
