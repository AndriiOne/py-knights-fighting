from typing import Iterator


KNIGHTS = {
    "lancelot": {
        "name": "Lancelot",
        "power": 35,
        "hp": 100,
        "armour": [],
        "weapon": {
            "name": "Metal Sword",
            "power": 50,
        },
        "potion": None,
    },
    "arthur": {
        "name": "Arthur",
        "power": 45,
        "hp": 75,
        "armour": [
            {
                "part": "helmet",
                "protection": 15,
            },
            {
                "part": "breastplate",
                "protection": 20,
            },
            {
                "part": "boots",
                "protection": 10,
            }
        ],
        "weapon": {
            "name": "Two-handed Sword",
            "power": 55,
        },
        "potion": None,
    },
    "mordred": {
        "name": "Mordred",
        "power": 30,
        "hp": 90,
        "armour": [
            {
                "part": "breastplate",
                "protection": 15,
            },
            {
                "part": "boots",
                "protection": 10,
            }
        ],
        "weapon": {
            "name": "Poisoned Sword",
            "power": 60,
        },
        "potion": {
            "name": "Berserk",
            "effect": {
                "power": +15,
                "hp": -5,
                "protection": +10,
            }
        }
    },
    "red_knight": {
        "name": "Red Knight",
        "power": 40,
        "hp": 70,
        "armour": [
            {
                "part": "breastplate",
                "protection": 25,
            }
        ],
        "weapon": {
            "name": "Sword",
            "power": 45
        },
        "potion": {
            "name": "Blessing",
            "effect": {
                "hp": +10,
                "power": +5,
            }
        }
    }
}


class Knight:
    def __init__(self, name: str, hp: int, power: int) -> None:
        self.name = name
        self.hp = hp
        self.power = power
        self.protection = 0

    def apply_armour(self, armour: dict) -> None:
        self.armour = armour
        for item in self.armour:
            self.protection += item.get("protection")

    def apply_weapon(self, weapon: dict) -> None:
        self.power += weapon.get("power")

    def apply_potion(self, potion: dict) -> None:
        if potion:
            effects = potion.get("effect")
            self.protection += effects.get("protection", 0)
            self.power += effects.get("power", 0)
            self.hp += effects.get("hp", 0)

    def take_damage(self, attacker_power: int) -> None:
        damage = attacker_power - self.protection
        if damage < 0:
            damage = 0
        self.hp = max(0, self.hp - damage)


def create_knight(knights_stats: dict) -> Iterator[Knight]:
    for one_knight, stats in knights_stats.items():
        knight_obj = Knight(
            name=stats["name"],
            hp=stats["hp"],
            power=stats["power"]
        )
        knight_obj.apply_armour(stats["armour"])
        knight_obj.apply_weapon(stats["weapon"])
        knight_obj.apply_potion(stats["potion"])
        yield knight_obj


def battle(knights_stats: dict) -> dict:
    ready_knights = {
        knight.name: knight for knight in create_knight(knights_stats)
    }

    ready_knights["Lancelot"].take_damage(ready_knights["Mordred"].power)
    ready_knights["Mordred"].take_damage(ready_knights["Lancelot"].power)

    ready_knights["Arthur"].take_damage(ready_knights["Red Knight"].power)
    ready_knights["Red Knight"].take_damage(ready_knights["Arthur"].power)

    return {
        "Lancelot": ready_knights["Lancelot"].hp,
        "Arthur": ready_knights["Arthur"].hp,
        "Mordred": ready_knights["Mordred"].hp,
        "Red Knight": ready_knights["Red Knight"].hp
    }


print(battle(KNIGHTS))
