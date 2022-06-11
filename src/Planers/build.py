class Build:
    def __init__(self, bot):
        self.bot = bot
        self.build_list = []

    def add_item(self, item):
        self.build_list.append(item)

    def set_build(self, build):
        self.build_list = build

    def get_next_item(self):
        if len(self.build_list) > 0:
            return self.build_list.pop(0)
        else:
            return None


class BuildItem:
    def __init__(self, item_id, is_structure=False):
        self.item_ID = item_id
        self.is_structure = is_structure
        self.time_to_start = 0

    def get_item_ID(self):
        return self.item_ID

    def is_structure(self):
        return self.is_structure

    def get_time_to_start(self):
        return self.time_to_start
