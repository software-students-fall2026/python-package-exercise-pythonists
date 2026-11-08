from .constants import (
    ENERGY_PER_SLEEP_HOUR,
    HUNGER_PER_SLEEP_HOUR,
    MAX_SLEEP_HOURS,
    STAT_MAX,
    STAT_MIN,
)
from .pet import Pet


def sleep(pet, hours):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")
    if isinstance(hours, bool) or not isinstance(hours, (int, float)):
        raise TypeError("hours must be a number")
    if not 0 < hours <= MAX_SLEEP_HOURS:
        raise ValueError(
            f"hours must be greater than 0 and at most {MAX_SLEEP_HOURS}"
        )

    pet.energy = max(
        STAT_MIN, min(STAT_MAX, pet.energy + hours * ENERGY_PER_SLEEP_HOUR)
    )
    pet.hunger = max(
        STAT_MIN, min(STAT_MAX, pet.hunger - hours * HUNGER_PER_SLEEP_HOUR)
    )
    return pet