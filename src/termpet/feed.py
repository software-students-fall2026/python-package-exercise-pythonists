from .constants import FOODS, STAT_MAX, STAT_MIN
from .pet import Pet


def feed(pet, food):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")
    if not isinstance(food, str):
        raise TypeError("food must be a string")

    key = food.strip().lower()
    if key not in FOODS:
        options = ", ".join(sorted(FOODS))
        raise ValueError(f"unknown food '{food}'. Choose from: {options}")

    effects = FOODS[key]
    pet.hunger = max(STAT_MIN, min(STAT_MAX, pet.hunger + effects["hunger"]))
    pet.energy = max(STAT_MIN, min(STAT_MAX, pet.energy + effects["energy"]))
    pet.happiness = max(
        STAT_MIN, min(STAT_MAX, pet.happiness + effects["happiness"])
    )
    return pet