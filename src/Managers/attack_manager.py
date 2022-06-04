from math import dist
from tkinter import N
from sc2 import units as Units
from sc2 import unit
from sc2.ids.unit_typeid import UnitTypeId as UnitID

from manager import Manager


class AttackManager(Manager):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.army_count: int = None
        self.enemy_units: Units = None
        self.clear_map = None

    async def micro_marine(self):
        marines = self.units(UnitID.MARINE)
        enemy_location = self.enemy_start_locations[0]

        for marine in marines:
            if (marine.weapon_cooldown == 0):
                marine.attack(enemy_location)
            elif marine.weapon_cooldown < 0:
                marine.move()

    def control_army_(self):
        army = self.units.filter(lambda unit: unit.type_id in {
                                 UnitID.MARINE, UnitID.SIEGETANK, UnitID.MEDIVAC, UnitID.REAPER, UnitID.SIEGETANKSIEGED})
        if not army:
            return

        # prasivaiksto publika bsk, jei nieko nemato
        ground_enemy_units = self.enemy_units.filter(
            lambda unit: not unit.is_flying and unit.type_id not in {UnitID.LARVA, UnitID.EGG})

        if not ground_enemy_units:
            self.army_no_vision_attack(army)
            return

        enemy_fighters = ground_enemy_units.filter(lambda u: u.can_attack) + self.enemy_structures(
            {UnitID.BUNKER, UnitID.SPINECRAWLER, UnitID.PHOTONCANNON}
        )

        self.army_set_attack(army, enemy_fighters, ground_enemy_units)

    def army_no_vision_attack(self, current_army):
        for unit in current_army:
            if self.enemy_structures:
                structures_in_range = self.enemy_structures.in_attack_range_of(
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
                    unit.move(self.enemy_structures.closest_to(unit))
            else:
                unit.move(self.enemy_start_locations[0])

    def army_set_attack(self, current_army, enemy_fighters, ground_enemy_units):
        for unit in current_army:
            if enemy_fighters:
                in_range_enemies = enemy_fighters.in_attack_range_of(unit)
                if in_range_enemies:
                    workers = in_range_enemies.filter(
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

                            unit.move(closest_enemy.position.towards(
                                unit, distance))

                    else:
                        lowest_hp = min(in_range_enemies, key=lambda s: (
                            s.health + s.shield, s.tag))
                        unit.attack(lowest_hp)

                else:
                    unit.attack(ground_enemy_units.closest_to(unit))

    # TODO: finish the function later

    async def execute_attack(self):
        marines = self.units(UnitID.MARINE)
        enemy_location = self.enemy_start_locations[0]

        if marines.amount >= 14:
            if self.enemy_units:
                for marine in marines:
                    if marine.weapon_ready:
                        marine.attack(
                            self.enemy_units.closest_to(marine.position))
                    else:
                        marine.move(self.units.closest_to(marine.position))
