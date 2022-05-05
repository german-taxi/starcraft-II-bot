class QueueItem():
    def __init__(self, unit_type, structure=None, location=None):
        self.unit_type = unit_type
        self.structure = structure
        self.location = location

    def set_item(self, unit_type, structure=None, location=None):
        self.unit_type = unit_type
        self.structure = structure
        self.location = location
