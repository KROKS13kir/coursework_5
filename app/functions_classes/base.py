from typing import Dict

from app.functions_classes.unit import BaseUnit

class BaseSingleton(type):
    _instances: Dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_RECOVERY_PER_TURN: float = 1
    game_on: bool = False
    battle_result: str = ""
    player: BaseUnit
    enemy: BaseUnit

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        """Начало игры, инициализация героя и противника"""
        self.player = player
        self.enemy = enemy
        self.game_on = True

    def player_attack(self) -> str:
        """Атака и следующий ход"""
        player_result = self.player.attack(target=self.enemy)
        return player_result + " " + self.next_turn()

    def player_use_skill(self) -> str:
        """Использование скилла и следующий ход"""
        player_result = self.player.use_skill(target=self.enemy)
        return player_result + " " + self.next_turn()

    def next_turn(self) -> str:
        """Проверка здоровья, обновление стамины и вызов ответного действия от противника"""
        if self._check_health():
            self._regenerate_stamina()
            enemy_result = self.enemy.attack(target=self.player)
            self._regenerate_stamina()
            return enemy_result
        return self.battle_result

    def _regenerate_stamina(self) -> None:
        """Обновление стамины"""
        player_stamina_recovery = self.STAMINA_RECOVERY_PER_TURN * self.player.unit_class.stamina
        enemy_stamina_recovery = self.STAMINA_RECOVERY_PER_TURN * self.enemy.unit_class.stamina
        self.player.stamina_points_ += round(player_stamina_recovery, 1)
        self.enemy.stamina_points_ += round(enemy_stamina_recovery, 1)

        # Исчерпалась ли стамина?
        if self.player.stamina_points_ > self.player.unit_class.max_stamina:
            self.player.stamina_points_ = self.player.unit_class.max_stamina
        if self.enemy.stamina_points_ > self.enemy.unit_class.max_stamina:
            self.enemy.stamina_points_ = self.enemy.unit_class.max_stamina

    def _check_health(self) -> bool:
        """Проверка здоровья"""

        if self.player.health_points_ > 0 and self.enemy.health_points_ > 0:
            return True

        if self.player.health_points_ <= 0 <= self.enemy.health_points_:
            self.battle_result = f'{self.player.name} проиграл {self.enemy.name}'

        if self.player.health_points_ >= 0 >= self.enemy.health_points_:
            self.battle_result = f'{self.player.name} победил {self.enemy.name}'

        if self.player.health_points_ <= 0 and self.enemy.health_points_ <= 0:
            self.battle_result = f'Ничья между {self.player.name} и {self.enemy.name}!'

        self._finish_game()

        return False

    def _finish_game(self) -> None:
        """Конец игры"""
        self._instances: Dict = {}
        self.game_on = False
