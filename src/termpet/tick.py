from termpet.pet import Pet
from .constants import (
    ENERGY_LOST_PER_TICK_HOUR,
    HUNGER_LOST_PER_TICK_HOUR,
    HAPPINESS_LOST_PER_TICK_HOUR,
    MAX_TICK_HOURS,
    STAT_MAX,
    STAT_MIN,
)

def tick(pet, hours):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")
    if isinstance(hours, bool) or not isinstance(hours, (int, float)):
        raise TypeError("hours must be a number")
    if not 0 < hours <= MAX_TICK_HOURS:
            raise ValueError(
                f"hours must be greater than 0 and at most {MAX_TICK_HOURS}"
    )

    pet.energy = max(STAT_MIN, min(STAT_MAX, pet.energy - hours * ENERGY_LOST_PER_TICK_HOUR))
    pet.hunger = max(STAT_MIN, min(STAT_MAX, pet.hunger - hours * HUNGER_LOST_PER_TICK_HOUR))
    pet.happiness = max(STAT_MIN, min(STAT_MAX, pet.happiness - hours * HAPPINESS_LOST_PER_TICK_HOUR))

    return pet