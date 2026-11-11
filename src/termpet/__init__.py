"""A playful terminal-pet package."""

from .pet import Pet, mood
from .feed import feed
from .sleep import sleep
from .storage import save, load
from .status import status
from .play import play
from .tick import tick

__all__ = ["Pet", "mood"]
