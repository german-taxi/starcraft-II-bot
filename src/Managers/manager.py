# Base class for all managers
class Manager:
    def __init__(self):
        self.__units = []

    def add_unit(self, unit):
        """
        Add a unit to the list of units.

        Args:
          unit: The unit to add to the list.
        """
        self.__units.append(unit)

    def remove_unit(self, unit):
        """
        It removes a unit from the units list.

        Args:
          unit: The unit to remove from the list.
        """
        self.__units.remove(unit)

    def transfer_units(self, unit_list, target_manager):
        """
        It removes units from the current manager and adds them to the target manager

        Args:
          unit_list: A list of units to transfer.
          target_manager: The manager that you want to transfer the units to.
        """
        for unit in unit_list:
            self.remove_unit(unit)
            target_manager.add_unit(unit)

    def split_manager(self, units_to_split):
        """
        The function takes in a list of units and creates a new manager object. It then transfers the
        units from the original manager to the new manager

        Args:
          units_to_split: a list of units that will be transferred to the new manager

        Returns:
          A new manager object.
        """
        new_manager = Manager()
        self.transfer_units(units_to_split, new_manager)
        return new_manager
