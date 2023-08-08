from dataclasses import dataclass

from skills import FuryPunch, HardShot, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass = UnitClass(
    name='Воин',
    max_health=100,
    max_stamina=50,
    attack=20,
    stamina=50,
    armor=10,
    skill=FuryPunch(),
)

ThiefClass = UnitClass(
    name='Вор',
    max_health=80,
    max_stamina=100,
    attack=10,
    stamina=100,
    armor=5,
    skill=HardShot(),
)

unit_classes = {ThiefClass.name: ThiefClass, WarriorClass.name: WarriorClass}
