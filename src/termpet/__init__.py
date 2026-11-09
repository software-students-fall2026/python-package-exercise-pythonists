"""A playful terminal-pet package."""

from .pet import Pet
from .feed import feed
from .sleep import sleep
from .storage import save, load
from .status import status
from .tick import tick

__all__ = ["Pet"]
