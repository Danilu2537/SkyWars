from random import randint


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self):
        self.game_is_running = True

    def _check_players_hp(self):
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Ничья'
        elif self.player.hp <= 0:
            self.battle_result = f'{self.enemy.name} победил в битве'
        elif self.enemy.hp <= 0:
            self.battle_result = f'{self.player.name} победил в битве'

    def _stamina_regeneration(self):
        if self.player.stamina < self.player.unit_class.max_stamina:
            if (
                self.player.stamina + self.STAMINA_PER_ROUND
                > self.player.unit_class.max_stamina
            ):
                self.player.stamina = self.player.unit_class.max_stamina
            else:
                self.player.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        self._check_players_hp()
        if self.battle_result:
            self.game_is_running = False
            return self.battle_result
        self._stamina_regeneration()
        if not self.enemy._is_skill_used and not randint(0, 3):
            return self.enemy.use_skill(self.player)
        return self.enemy.hit(self.player)

    def end_game(self):
        self._instances = {}
        self.game_is_running = False
        self.battle_result = None

    def player_hit(self):
        result_hit = self.player.hit(self.enemy)
        enemy_turn = self.next_turn()
        return f'{result_hit}<br>{enemy_turn}'

    def player_use_skill(self):
        result_skill = self.player.use_skill(self.enemy)
        enemy_turn = self.next_turn()
        return f'{result_skill}<br>{enemy_turn}'
