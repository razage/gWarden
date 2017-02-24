from gWarden import db
from gWarden.models import Class, Race, Specialization
from gWarden.characters.models import Character

db.create_all()
db.session.commit()

# Basic WoW data
classes = {
    "Warrior": {
        "id": 1,
        "specs": (("Protection", "Tank"), ("Arms", "DPS"), ("Fury", "DPS"))
    },
    "Paladin": {
        "id": 2,
        "specs": (("Protection", "Tank"), ("Retribution", "DPS"), ("Holy", "Healer"))
    },
    "Hunter": {
        "id": 3,
        "specs": (("Survival", "DPS"), ("Marksmanship", "RDPS"), ("Beast Mastery", "RDPS"))
    },
    "Rogue": {
        "id": 4,
        "specs": (("Assassination", "DPS"), ("Outlaw", "DPS"), ("Subtlety", "DPS"))
    },
    "Priest": {
        "id": 5,
        "specs": (("Holy", "Healer"), ("Discipline", "Healer"), ("Shadow", "RDPS"))
    },
    "Death Knight": {
        "id": 6,
        "specs": (("Unholy", "DPS"), ("Frost", "DPS"), ("Blood", "Tank"))
    },
    "Shaman": {
        "id": 7,
        "specs": (("Restoration", "Healer"), ("Elemental", "RDPS"), ("Enhancement", "DPS"))
    },
    "Mage": {
        "id": 8,
        "specs": (("Frost", "RDPS"), ("Fire", "RDPS"), ("Arcane", "RDPS"))
    },
    "Warlock": {
        "id": 9,
        "specs": (("Demonology", "RDPS"), ("Affliction", "RDPS"), ("Destruction", "RDPS"))
    },
    "Monk": {
        "id": 10,
        "specs": (("Brewmaster", "Tank"), ("Mistweaver", "Healer"), ("Windwalker", "DPS"))
    },
    "Druid": {
        "id": 11,
        "specs": (("Restoration", "Healer"), ("Feral", "DPS"), ("Balance", "RDPS"), ("Guardian", "Tank"))
    },
    "Demon Hunter": {
        "id": 12,
        "specs": (("Havoc", "DPS"), ("Vengeance", "Tank"))
    }
}

races = (
    ("Human", 1),
    ("Orc", 2),
    ("Dwarf", 3),
    ("Night Elf", 4),
    ("Undead", 5),
    ("Tauren", 6),
    ("Gnome", 7),
    ("Troll", 8),
    ("Goblin", 9),
    ("Blood Elf", 10),
    ("Draenei", 11),
    ("Worgen", 22),
    ("Pandaren (N)", 24),
    ("Pandaren (A)", 25),
    ("Pandaren (H)", 26)
)

for r in races:
    db.session.add(Race(r[0], r[1]))

db.session.commit()

for k, v in classes.items():
    _class = Class(k, v['id'])

    # noinspection PyTypeChecker
    for s in v['specs']:
        _class.specs.append(Specialization(s[0], s[1]))

    db.session.add(_class)

db.session.commit()
