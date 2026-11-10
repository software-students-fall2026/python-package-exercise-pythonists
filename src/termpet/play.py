from .constants import (
    GAMES,
    MAX_PLAY_MINUTES,
    STAT_MAX,
    STAT_MIN,
)
from .pet import Pet

def play(pet, game, minutes=10):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")
    if not isinstance(game, str):
        raise TypeError("game must be a string")
    if isinstance(minutes, bool) or not isinstance(minutes, (int, float)):
        raise TypeError("minutes must be a number")
    if not 0 < minutes <= MAX_PLAY_MINUTES:
        raise ValueError(
            f"minutes must be greater than 0 and at most {MAX_PLAY_MINUTES}"
        )

    key = game.strip().lower()
    if key not in GAMES:
        options = ", ".join(sorted(GAMES))
        raise ValueError(f"Invalid game: {game}, must be one of: {options}")

    effect = GAMES[key]
    pet.hunger = max(
        STAT_MIN, min(STAT_MAX, pet.hunger + effect["hunger"] * minutes)
    )
    pet.energy = max(
        STAT_MIN, min(STAT_MAX, pet.energy + effect["energy"] * minutes)
    )
    pet.happiness = max(
        STAT_MIN, min(STAT_MAX, pet.happiness + effect["happiness"] * minutes)
    )

    return pet