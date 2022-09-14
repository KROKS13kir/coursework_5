from __future__ import annotations
from abc import ABC, abstractmethod
from app.functions_classes.equipment import Equipment, Weapon, Armor
from app.functions_classes.classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """Base class for units"""

    def __init__(self, name: str, unit_class: UnitClass, weapon: Weapon, armor: Armor):
        self.name = name
        self.unit_class = unit_class
        self.health_points_: float = unit_class.max_health
        self.stamina_points_: float = unit_class.max_stamina
        self.weapon = weapon
        self.armor = armor
        self.skill_used: bool = False

    @property
    def health_points(self):
        if self.health_points_ < 0:
            return 0
        return round(self.health_points_, 1)

    @property
    def stamina_points(self):
        return round(self.stamina_points_, 1)

    def attack(self, target: BaseUnit) -> str:
        """Логика атаки"""
        if self.stamina_points_ >= self.weapon.stamina_per_hit:

            # Подсчёт урона
            damage_inflicted = self._calculate_damage(target)
            target._get_damage(damage_inflicted)

            # Обновление значения стамины
            self.stamina_points_ -= self.weapon.stamina_per_hit
            target.stamina_points_ -= target.armor.stamina_per_turn

            # Проверка значения стамины
            if target.stamina_points_ < 0:
                target.stamina_points_ = 0

            if damage_inflicted > 0:
                return (f"{self.name}, используя {self.weapon.name}, "
                        f"пробивает {target.armor.name} соперника и наносит {damage_inflicted} урона.")
            return (f"{self.name}, используя {self.weapon.name}, "
                    f"наносит удар, но {target.armor.name} соперника его останавливает.")

        return (f"{self.name} попытался использовать {self.weapon.name}, "
                f"но у него не хватило выносливости.")

    def use_skill(self, target: BaseUnit):
        """Использование скилла"""
        if self.skill_used:
            return (f"{self.name} попытался использовать {self.unit_class.skill.name}, "
                    f"но навык уже был использован.")
        self.skill_used = True
        return self.unit_class.skill.use(user=self, target=target)

    def _calculate_damage(self, target: BaseUnit) -> float:
        """Расчёт урона"""
        damage = self.weapon.calculate_damage() * self.unit_class.attack
        defence = target.armor.defence if target.stamina_points_ >= target.armor.stamina_per_turn else 0

        if damage <= defence:
            damage_inflicted = 0
        else:
            damage_inflicted = damage - defence

        return round(damage_inflicted, 1)

    def _get_damage(self, damage_inflicted: float) -> None:
        """Изменение очков здоровья с учётом урона"""
        self.health_points_ -= damage_inflicted


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция для удара игрока
        """
        if not self.skill_used:
            use_skill = randint(0, 9)
            if use_skill == 0:
                return self.use_skill(target)
        return super().attack(target)


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция для удара противника
        """
        if not self.skill_used:
            use_skill = randint(0, 9)
            if use_skill == 0:
                return self.use_skill(target)

        return super().attack(target)


