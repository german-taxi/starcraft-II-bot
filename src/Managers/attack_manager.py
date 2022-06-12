from sc2 import units as Units
from sc2.ids.unit_typeid import UnitTypeId as UnitID

from src.Managers.manager import Manager


# > This class is used to manage the attack of the bot
class AttackManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.__bot = bot
        self.army_count: int = 0
        self.clear_map = None
        self.__army_tags = set()
        self.__army_units: Units = None
        self.attack = False

    def add_army_tags(self, units):
        """
        It adds the army tag to a list of units

        Args:
          units: A list of units to add the tag to.
        """
        for unit in units:
            self.add_army_tag(unit.tag)

    def add_army_tag(self, tag):
        """
        The function adds the unit's tag to the army_tags set, and then increments the army_count by 1

        Args:
          tag: The unit that we want to add to the army.
        """
        self.__army_tags.add(tag)
        # later :self.bot.calculate_supply_cost(unit.type_id)
        self.army_count += 1
        print("Added army tag: ", tag)

    def remove_army_tag(self, tag):
        """
        It removes the tag from the set of army tags, and decrements the army count

        Args:
          tag: The tag of the army you want to remove.

        Returns:
          A boolean value.
        """
        if tag in self.__army_tags:
            self.__army_tags.discard(tag)
            self.army_count -= 1
            return True
        return False

    def update(self):
        """
        The update function is called every frame, and it updates the army_units list with the current units
        in the army, and if the army is large enough, it sets the attack variable to True
        """
        self.__army_units = self.__bot.get_units_by_tag(self.__army_tags)
        if self.army_count > 20:
            self.attack = True
        if self.attack:
            self.__control_army()

    def __control_army(self):
        """
        If there are no enemy units in sight, the army will move to the closest enemy structure. If there
        are enemy units in sight, the army will attack the closest enemy unit

        Returns:
          a list of units that are in the army.
        """
        # army = self.army_units.filter(lambda unit: unit.type_id in {
        #                          UnitID.MARINE, UnitID.SIEGETANK, UnitID.MEDIVAC, UnitID.REAPER, UnitID.SIEGETANKSIEGED, UnitID.HELLION})
        army = self.__army_units
        if not army:
            return

        # prasivaiksto publika bsk, jei nieko nemato
        ground_enemy_units = self.__bot.enemy_units.filter(
            lambda unit: not unit.is_flying and unit.type_id not in {UnitID.LARVA, UnitID.EGG})  # and not unit.is_structure

        if not ground_enemy_units:
            self.__army_attack_no_vision(army)
            return

        # o cia jau lupa
        enemy_fighters = ground_enemy_units.filter(lambda u: u.can_attack) + self.__bot.enemy_structures(
            {UnitID.BUNKER, UnitID.SPINECRAWLER, UnitID.PHOTONCANNON}
        )
        # print("enemy fighters: ", len(enemy_fighters))
        self.__army_attack(army, enemy_fighters, ground_enemy_units)

    def __army_attack_no_vision(self, current_army):
        """
        If there are enemy structures, attack the one with the lowest health, otherwise move towards the
        enemy base

        Args:
          current_army: The army that is currently being controlled.
        """
        for unit in current_army:
            if self.__bot.enemy_structures:
                structures_in_range = self.__bot.enemy_structures.in_attack_range_of(
                    unit)
                if structures_in_range:
                    lowest_hp = min(structures_in_range, key=lambda s: (
                        s.health + s.shield, s.tag))
                    if unit.weapon_ready:
                        unit.attack(lowest_hp)
                    else:
                        if unit.ground_range > 1:
                            unit.move(lowest_hp.position.towards(
                                unit, 1 + lowest_hp.radius))
                        else:
                            unit.move(lowest_hp.position)

                else:
                    unit.move(self.__bot.enemy_structures.closest_to(unit))
            else:
                unit.move(self.__bot.enemy_start_locations[0])

    def __army_attack(self, current_army, enemy_fighters, ground_enemy_units):
        """
        If there are enemy fighters in range, attack the one with the lowest health. If there are no
        enemy fighters in range, attack the closest enemy unit

        Args:
          current_army: The army that is currently attacking
          enemy_fighters: Units that can attack back
          ground_enemy_units: This is the enemy ground units that are in range of our army.
        """
        for unit in current_army:
            if enemy_fighters:
                in_range_enemies = enemy_fighters.in_attack_range_of(unit)
                if in_range_enemies:
                    workers = in_range_enemies.filter(  # bot derps out, and ignores all dangerous units
                        lambda u: u.type_id in {UnitID.SCV, UnitID.DRONE, UnitID.PROBE})
                    if workers:
                        in_range_enemies = workers

                    if unit.ground_range > 1:
                        if unit.weapon_ready:
                            lowest_hp = min(in_range_enemies, key=lambda s: (
                                s.health + s.shield, s.tag))
                            unit.attack(lowest_hp)

                        else:
                            friends_in_range = current_army.in_attack_range_of(
                                unit)
                            closest_enemy = in_range_enemies.closest_to(unit)
                            distance = unit.ground_range + unit.radius + closest_enemy.radius
                            if (len(friends_in_range) <= len(in_range_enemies) and closest_enemy.ground_range <= unit.ground_range):
                                distance += 1
                            else:
                                if (len(current_army.closer_than(7, unit.position)) >= 6):
                                    distance -= 1
                            unit.move(unit.position.towards(
                                closest_enemy, -2))

                    else:
                        lowest_hp = min(in_range_enemies, key=lambda s: (
                            s.health + s.shield, s.tag))
                        unit.attack(lowest_hp)

                else:
                    unit.attack(ground_enemy_units.closest_to(unit))

    # TODO: finish the function later

    def __simple_micro(self):
        """
        If there are enemy units, then for each marine, if the marine's weapon is ready, then attack the
        closest enemy unit, otherwise move to the closest enemy structure
        """
        marines = self.__units(UnitID.MARINE)

        if self.enemy_units:
            for marine in marines:
                if marine.weapon_ready:
                    marine.attack(
                        self.enemy_units.closest_to(marine.position))
                else:
                    marine.move(self.__bot.enemy_structures.closest_to(marine))

    def __army_set_attack_enemy_base(self):
        """
        If we have at least 14 marines, attack the enemy base
        """
        enemy_base_location = self.__bot.enemy_start_locations[0]
        marines = self.__units(UnitID.MARINE)

        if marines >= 14:
            for marine in marines:
                if marine.weapon_ready:
                    marine.attack(enemy_base_location)
                else:
                    marine.move(self.__bot.enemy_structures.closest_to(marine))

    def __army_set_attack_enemy_fighters(self):
        """
        If there are enemy units that can attack, attack them. If not, attack the enemy structures
        """
        marines = self.__units(UnitID.MARINE)
        enemy_fighters = self.enemy_units.filter(lambda u: u.can_attack) + self.enemy_units.filter(
            lambda u: u.type_id in {UnitID.STALKER, UnitID.ZEALOT, UnitID.VOIDRAY, UnitID.DARKTEMPLAR, UnitID.COLOSSUS, UnitID.HIGHTEMPLAR})

        if enemy_fighters:
            for marine in marines:
                if marine.weapon_ready:
                    marine.attack(enemy_fighters.closest_to(marine))
                else:
                    marine.move(self.__bot.enemy_structures.closest_to(marine))
                self.handle_low_health_units(enemy_fighters)

    def __handle_low_health_units(self, enemy_units):
        """
        If a marine is low on health, move it away from the enemy

        Args:
          enemy_units: The enemy units that are in range of the marines.
        """
        low_marines = self.__army_units(UnitID.MARINE).filter(
            lambda unit: unit.health_percentage < 0.4)
        furthest_unit_from_enemy = self.__units(UnitID.MARINE).furthest_to(
            enemy_units.closest_to(self.__bot.start_location))
        furthest_unit_from_enemy_base = self.__units.furthest_to(
            self.__bot.enemy_start_locations[0])

        for marine in low_marines:
            if marine.distance_to(furthest_unit_from_enemy) < 1:
                marine.move(furthest_unit_from_enemy_base.position.towards(
                    marine, 1 + furthest_unit_from_enemy_base.radius))
            else:

                marine.move(furthest_unit_from_enemy.position.towards(
                    marine, 1 + furthest_unit_from_enemy.radius))
