from src.Helpers.mineral_field import MineralField


# Class representing a gas field
class GasField(MineralField):
    def __init__(self, bot, tag):
        super().__init__(bot, tag)
        self.building_tag = None

    def set_gas_building(self, building_tag):
        """
        `set_gas_building` sets the building tag for the gas building

        Args:
          building_tag: The building tag of the building you want to set the gas for.
        """
        self.building_tag = building_tag

    def update(self):
        """
        If the worker is idle or gathering, and it's not already gathering from the correct building, send
        it to gather from the correct building
        """
        workers = self._bot.get_units_by_tag(self._worker_tags)

        for worker in workers:
            if worker.is_gathering or worker.is_idle:
                if not worker.orders or worker.orders[0].target != self.building_tag:
                    gas_building = self._bot.unit_by_tag.get(self.building_tag)
                    worker.gather(gas_building, queue=False)
                    # print("Send worker to gather, reason wrong target/idle")  # Debug

    def update_gas_tag(self, tag):
        """
        `update_gas_tag` updates the gas tag for the gas field
        :param tag:
        :return:
        """
        self.tag = tag
