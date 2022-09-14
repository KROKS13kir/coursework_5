from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit

class Skill(ABC):
    """
    Базовый класс умения
    """
    name: str = ""
    damage: float = 0
    stamina_required: float = 0
    user: BaseUnit
    target: BaseUnit

    @abstractmethod
    def _skill_effect(self):
        pass

    def use(self, user: BaseUnit, target: BaseUnit):
        """Использование скилла, если хватает стамины"""
        self.user = user
        self.target = target

        if self.user.stamina_points_ < self.stamina_required:
            return (f"{self.user.name} попытался использовать {self.user.unit_class.skill.name}, "
                    f"но у него не хватило выносливости.")
        return self._skill_effect()


class FuryPunch(Skill):
    name: str = 'Свирепый пинок'
    damage: float = 12.0
    stamina_required: float = 6.0

    def _skill_effect(self):
        """Уменьшение стамины и здоровья"""
        self.target.health_points_ -= self.damage
        self.user.stamina_points_ -= self.stamina_required
        return f'{self.user.name} использует {self.user.unit_class.skill.name} и наносит {self.damage} урона сопернику.'

class HardShot(Skill):
    name: str = 'Мощный укол'
    damage: float = 15.0
    stamina_required: float = 5.0

    def _skill_effect(self) -> str:
        """Уменьшение стамины и здоровья"""
        self.target.health_points_ -= self.damage
        self.user.stamina_points_ -= self.stamina_required
        return f'{self.user.name} использует {self.user.unit_class.skill.name} и наносит {self.damage} урона сопернику.'
