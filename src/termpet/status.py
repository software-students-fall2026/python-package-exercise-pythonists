from .constants import STAT_MAX
from .pet import Pet

BAR_WIDTH = 10

def _bar(value):
    """Render a stat as a 10-character bar, e.g. 70 -> '███████░░░'."""
    filled = round(value / STAT_MAX * BAR_WIDTH)
    return "█" * filled + "░" * (BAR_WIDTH - filled)

def status(pet, verbose=False):
    if not isinstance(pet, Pet):
        raise TypeError(f"pet must be a Pet, got {type(pet).__name__}")
    if not isinstance(verbose, bool):
        raise TypeError(f"verbose must be a bool, got {type(verbose).__name__}")

    header = f"{pet.name} the {pet.species}"
    stats = [("Hunger", pet.hunger), ("Energy", pet.energy), ("Happiness", pet.happiness)]

    if not verbose:
        return " | ".join([header] + [f"{label} {value}" for label, value in stats])

    lines = [header] + [f"{label:<10}{_bar(value)} {value:>3}" for label, value in stats]
    return "\n".join(lines)