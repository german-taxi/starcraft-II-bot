# It's a class that holds a list of builds
class Build:
    def __init__(self, bot):
        self.bot = bot
        self.build_list = []

    def add_item(self, item):
        """
        The function takes in an item and adds it to the build_list

        Args:
          item: The item to be added to the list.
        """
        self.build_list.append(item)

    def add_to_start(self, item):
        """
        The function takes in an item and adds it to the start of the build_list

        Args:
          item: The item to be added to the list.
        """
        self.build_list.insert(0, item)

    def set_build(self, build):
        """
        It sets the build list to the build list that is passed in.

        Args:
          build: A list of strings that are the names of the build files.
        """
        self.build_list = build

    def get_next_item(self):
        """
        If there are items in the build list, return the first item in the list. Otherwise, return None

        Returns:
          The first item in the list is being returned.
        """
        if len(self.build_list) > 0:
            return self.build_list.pop(0)
        return None

    def first_item(self):
        """
        If there are items in the build list, return the first item in the list. Otherwise, return None

        Returns:
          The first item in the list is being returned.
        """
        if len(self.build_list) > 0:
            return self.build_list[0]
        return None

# The BuildItem class is a class that represents an item that is being built. It has three attributes:
# item_ID, is_structure, and time_to_start
class BuildItem:
    def __init__(self, item_id, is_structure=False):
        self.item_ID = item_id
        self.is_structure = is_structure
        self.time_to_start = 0

    def get_item_ID(self):
        """
        It returns the item ID of the item.

        Returns:
          The item ID
        """
        return self.item_ID

    def is_structure(self):
        """
        It returns the value of the is_structure attribute.

        Returns:
           A boolean value.
        """
        return self.is_structure

    def get_time_to_start(self):
        """
        This function returns the time to start of the event

        Returns:
          The time to start.
        """
        return self.time_to_start
