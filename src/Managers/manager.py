class Manager:
    def __init__(self):
        self.units = []

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)

    def transfer_units(self, unit_list, target_manager):
        for unit in unit_list:
            self.remove_unit(unit)
            target_manager.add_unit(unit)

    def split_manager(self, units_to_split):
        new_manager = Manager()
        self.transfer_units(units_to_split, new_manager)
        return new_manager
