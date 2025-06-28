from enum import Enum

class Mood(Enum):
    PLAYFUL = "игривый"
    LAZY = "ленивый"

CATS = {
    "Барсик": {"rarity": "common", "mood": Mood.PLAYFUL},
    "Гарфилд": {"rarity": "legendary", "mood": Mood.LAZY},
    # ... остальные коты
}