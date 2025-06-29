from enum import Enum

class Mood(Enum):
    PLAYFUL = "игривый"
    LAZY = "ленивый"
    MOODY = "капризный"
    HUNGRY = "голодный"
    ARISTOCRAT = "аристократичный"

CATS = {
    "Барсик": {"rarity": "common", "fav_drink": 1},
    "Мурзик": {"rarity": "common", "fav_drink": 2},
    # ... остальные коты
}