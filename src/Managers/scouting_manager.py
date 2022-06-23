import random
from sc2 import position
from sc2.ids.unit_typeid import UnitTypeId

# from Managers.manager import Manager
from src.Managers.manager import Manager


class ScoutingManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.__bot = bot
        self._scout_tags = set()
        self.scouts_and_spots = {}
        self.occupation = 0

    def add_scout_tag(self, scout_tag):
        """
        The function adds the unit's tag to the scout_tags set, and then increments the occupation by 1

        Args:
          tag: The unit that we want to add to the scouting.
        """
        self._scout_tags.add(scout_tag)
        self.occupation += 1

    def remove_scout_tag(self, scout_tag):
        """
        It removes the tag from the set of scout tags, and decrements the occupation

        Args:
          tag: The tag of the scouts you want to remove.

        Returns:
          A boolean value.
        """

        if scout_tag in self._scout_tags:
            self._scout_tags.discard(scout_tag)
            self.occupation -= 1
            return True
        return False

    def get_random_scout_tag(self):
        """
        If there are scout tags available, return one and decrement the occupation count

        Returns:
          A random scout tag is being returned.
        """

        if self._scout_tags:
            self.occupation -= 1
            return self._scout_tags.pop()
        return None

    def update(self):
        """

        The function updates the scouting manager

        """

        scouts = self.__bot.get_units_by_tag(self._scout_tags)

        for scout in scouts:
            # if scout.is_idle:
                self.scouting(scout)                        

    def scouting(self, scout):
        #  if len(self._scout_tags) > 0:
        #     scout = self._scout_tags[0]
            # if scout.is_idle:
                enemy_location = self.__bot.enemy_start_locations[0]
                move_to = self.__random_location_variance(enemy_location)
                scout.move(move_to)
                
    def __random_location_variance(self, location):
        """
        It takes the enemy start location, adds a random number between -5 and 5 to the x and y
        coordinates, then divides that number by 100 and multiplies it by the enemy start location

        Args:
          enemy_start_location: This is the location of the enemy base.

        Returns:
          The go_to variable is being returned.
        """
        x = location[0]
        y = location[1]

   
        x += random.randrange(-5,5)
        y += random.randrange(-5,5)

        if x < 0:
            print("x below")
            x = 0
        if y < 0:
            print("y below")
            y = 0
        if x > self.__bot.game_info.map_size[0]:
            print("x above")
            x = self.__bot.game_info.map_size[0]
        if y > self.__bot.game_info.map_size[1]:
            print("y above")
            y = self.__bot.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x,y)))
        # print("Unit goes to enemy location: ")
        # print(x)
        # print(y)
        return go_to
