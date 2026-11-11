"""The shared pet information used by the package's functions."""

from dataclasses import dataclass

from .constants import DEFAULT_STAT, MOOD_THRESHOLDS, STAT_MAX, STAT_MIN


@dataclass
class Pet:
    """Create a pet with a name, species, and three editable stats.

    All stats range from 0 to 100. Hunger measures fullness: 0 means
    starving and 100 means full. Species is a nonempty text label.
    Starting stats can be supplied when restoring a saved pet.
    """

    name: str
    species: str
    hunger: float = DEFAULT_STAT
    energy: float = DEFAULT_STAT
    happiness: float = DEFAULT_STAT

    def __post_init__(self):
        for field in ("name", "species"):
            value = getattr(self, field)
            if not isinstance(value, str):
                raise TypeError(f"{field} must be a string")
            if not value.strip():
                raise ValueError(f"{field} must not be blank")

        for field in ("hunger", "energy", "happiness"):
            value = getattr(self, field)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(f"{field} must be a number")
            if not STAT_MIN <= value <= STAT_MAX:
                raise ValueError(
                    f"{field} must be between {STAT_MIN} and {STAT_MAX}"
                )


def mood(pet):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")

    average = (pet.hunger + pet.energy + pet.happiness) / 3

    if average >= MOOD_THRESHOLDS["ecstatic"]:
        return "ecstatic"
    if average >= MOOD_THRESHOLDS["content"]:
        return "content"
    if average >= MOOD_THRESHOLDS["grumpy"]:
        return "grumpy"
    return "feral"
