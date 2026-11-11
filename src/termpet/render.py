from .constants import STAT_MAX
from .pet import Pet, mood

DEFAULT_RENDER_WIDTH = 10

FACES = {
    "ecstatic": "^.^",
    "content": "o.o",
    "grumpy": "-.-",
    "feral": ">.<",
}

def stat_bar(value, width):
    filled = int(value * width / STAT_MAX)
    empty = width - filled
    return "[" + "#" * filled + "-" * empty + "]"

def render(pet, width=DEFAULT_RENDER_WIDTH):
    if not isinstance(pet, Pet):
        raise TypeError("pet must be a Pet")
    if isinstance(width, bool) or not isinstance(width, int):
        raise TypeError("width must be a whole number")
    if width < 1:
        raise ValueError("width must be a positive value")

    feeling = mood(pet)
    face = FACES[feeling]

    return "\n".join([
        "  /\\_/\\",
        f" ( {face} )  {pet.name} the {pet.species} — {feeling}",
        "  > ^ <",
        f"Hunger {stat_bar(pet.hunger, width)}",
        f"Energy {stat_bar(pet.energy, width)}",
        f"Happiness {stat_bar(pet.happiness, width)}"
    ])
