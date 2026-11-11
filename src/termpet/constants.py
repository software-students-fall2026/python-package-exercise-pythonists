"""Starting values and bounds for the basic pet stats."""

STAT_MIN = 0
STAT_MAX = 100
DEFAULT_STAT = 50

MOODS = ("ecstatic", "content", "grumpy", "feral")

MOOD_THRESHOLDS = {
    "ecstatic": 75,
    "content": 50,
    "grumpy": 25,
}

FOODS = {
    "apple":   {"hunger": 10, "energy": 5,   "happiness": 2},
    "kibble":  {"hunger": 20, "energy": 0,   "happiness": 1},
    "steak":   {"hunger": 35, "energy": 5,   "happiness": 10},
    "treat":   {"hunger": 5,  "energy": 15,  "happiness": 15},
    "veggies": {"hunger": 15, "energy": 0,   "happiness": 0},
}

GAMES = {
    "fetch": {"hunger": -1, "energy": -1, "happiness": 2},
    "hide & seek": {"hunger": -0.5, "energy": -0.5, "happiness": 1.5},
    "tug of war": {"hunger": -1.5, "energy": -1.5, "happiness": 2.5},
    "chase": {"hunger": -2, "energy": -2, "happiness": 3},
}

ENERGY_PER_SLEEP_HOUR = 10   
HUNGER_PER_SLEEP_HOUR = 2    
MAX_SLEEP_HOURS = 24

MAX_PLAY_MINUTES = 60
ENERGY_PER_SLEEP_HOUR = 10
ENERGY_LOST_PER_TICK_HOUR = 2

HUNGER_PER_SLEEP_HOUR = 2
HUNGER_LOST_PER_TICK_HOUR = 4

HAPPINESS_LOST_PER_TICK_HOUR = 3

MAX_SLEEP_HOURS = 24
MAX_TICK_HOURS = 24