import pytest
from termpet.constants import (
    ENERGY_PER_SLEEP_HOUR,
    HUNGER_PER_SLEEP_HOUR,
    MAX_SLEEP_HOURS,
    STAT_MAX,
    STAT_MIN,
)
from termpet.pet import Pet
from termpet.sleep import sleep


class Tests:

    def setup_method(self):
        self.pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)

    def test_sleep_returns_the_pet(self):
        result = sleep(self.pet, 1)
        assert result is self.pet, "Expected sleep() to return the same pet object"

    def test_sleep_restores_energy(self):
        pet = Pet("Mochi", "cat", hunger=100, energy=0, happiness=50)
        sleep(pet, 2)
        expected = 2 * ENERGY_PER_SLEEP_HOUR
        assert pet.energy == expected, f"Expected energy {expected}, got {pet.energy}"
        assert pet.energy > 0, "Expected the pet to have more energy than before"

    def test_sleep_lowers_fullness(self):
        pet = Pet("Mochi", "cat", hunger=100, energy=0, happiness=50)
        sleep(pet, 2)
        expected = 100 - 2 * HUNGER_PER_SLEEP_HOUR
        assert pet.hunger == expected, f"Expected hunger {expected}, got {pet.hunger}"
        assert pet.hunger < 100, "Expected the pet to be less full than before"

    def test_longer_sleep_restores_more_energy(self):
        short = Pet("A", "cat", hunger=100, energy=0, happiness=50)
        long = Pet("B", "cat", hunger=100, energy=0, happiness=50)
        sleep(short, 1)
        sleep(long, 3)
        assert long.energy > short.energy, "Expected more sleep to give more energy"
        assert long.hunger < short.hunger, "Expected more sleep to make the pet hungrier"

    def test_sleep_accepts_partial_hours(self):
        pet = Pet("Mochi", "cat", hunger=100, energy=0, happiness=50)
        sleep(pet, 0.5)
        expected = 0.5 * ENERGY_PER_SLEEP_HOUR
        assert pet.energy == expected, f"Expected energy {expected}, got {pet.energy}"

    def test_sleep_does_not_change_happiness(self):
        sleep(self.pet, 3)
        assert self.pet.happiness == 50, "Expected happiness to stay the same"
        assert self.pet.name == "Mochi", "Expected the name to stay the same"
        assert self.pet.species == "cat", "Expected the species to stay the same"

    def test_sleep_does_not_go_above_max_energy(self):
        pet = Pet("Mochi", "cat", hunger=100, energy=STAT_MAX - 1, happiness=50)
        sleep(pet, 8)
        assert pet.energy == STAT_MAX, f"Expected energy to stop at {STAT_MAX}, got {pet.energy}"

    def test_sleep_does_not_go_below_min_fullness(self):
        pet = Pet("Mochi", "cat", hunger=1, energy=0, happiness=50)
        sleep(pet, 10)
        assert pet.hunger == STAT_MIN, f"Expected hunger to stop at {STAT_MIN}, got {pet.hunger}"

    def test_sleep_for_max_hours_is_allowed(self):
        sleep(self.pet, MAX_SLEEP_HOURS)
        assert STAT_MIN <= self.pet.energy <= STAT_MAX, "Expected energy to stay in range"
        assert STAT_MIN <= self.pet.hunger <= STAT_MAX, "Expected hunger to stay in range"

    def test_sleep_zero_hours_raises_value_error(self):
        with pytest.raises(ValueError):
            sleep(self.pet, 0)

    def test_sleep_negative_hours_raises_value_error(self):
        with pytest.raises(ValueError):
            sleep(self.pet, -2)

    def test_sleep_too_many_hours_raises_value_error(self):
        with pytest.raises(ValueError):
            sleep(self.pet, MAX_SLEEP_HOURS + 1)

    def test_sleep_non_number_hours_raises_type_error(self):
        with pytest.raises(TypeError):
            sleep(self.pet, "8")
        with pytest.raises(TypeError):
            sleep(self.pet, None)

    def test_sleep_non_pet_raises_type_error(self):
        with pytest.raises(TypeError):
            sleep("Mochi", 2)
        with pytest.raises(TypeError):
            sleep(None, 2)

    def test_failed_sleep_leaves_pet_unchanged(self):
        with pytest.raises(ValueError):
            sleep(self.pet, -2)
        assert self.pet.hunger == 50, "Expected hunger to be unchanged"
        assert self.pet.energy == 50, "Expected energy to be unchanged"
        assert self.pet.happiness == 50, "Expected happiness to be unchanged"