from sc2.units import Units


class unit_tag:
    def __init__(self, bot):
        self.bot = bot
        self.units = Units([], self.bot)
        self.unit_tags = []
        self.target_tags = []
        self.accesed = 0