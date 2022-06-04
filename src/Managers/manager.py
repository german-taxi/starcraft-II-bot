import sc2

from bot import WorkerRushBot

class Manager(WorkerRushBot):
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

    async def execute_build_order(self):
        if (self.minerals < 25):
            return
            
        # To be continued...
        
        
