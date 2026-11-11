import pytest
from termpet.constants import (
    ENERGY_LOST_PER_TICK_HOUR,
    HUNGER_LOST_PER_TICK_HOUR,
    HAPPINESS_LOST_PER_TICK_HOUR,
    MAX_TICK_HOURS,
    STAT_MAX,
    STAT_MIN,
)
from termpet.pet import Pet
from termpet.tick import tick

class Tests:
    def setup_method(self):
        self.pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
    
    def test_tick_returns_the_pet(self):
        result = tick(self.pet, 1)
        assert result is self.pet, "Expected tick() to return the same pet object"
    
    def test_tick_reduces_energy(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        tick(pet, 2)
        expected = 50 - 2 * ENERGY_LOST_PER_TICK_HOUR
        assert pet.energy == expected, f"Expected energy {expected}, got {pet.energy}"
        assert pet.energy < 50, "Expected the pet to have less energy than before"
    
    def test_tick_reduces_hunger(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        tick(pet, 2)
        expected = 50 - 2 * HUNGER_LOST_PER_TICK_HOUR
        assert pet.hunger == expected, f"Expected hunger {expected}, got {pet.hunger}"
        assert pet.hunger < 50, "Expected the pet to be less full than before"
    
    def test_tick_reduces_happiness(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        tick(pet, 2)
        expected = 50 - 2 * HAPPINESS_LOST_PER_TICK_HOUR
        assert pet.happiness == expected, f"Expected happiness {expected}, got {pet.happiness}"
        assert pet.happiness < 50, "Expected the pet to be less happy than before"

    def test_tick_accepts_partial_hours(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        tick(pet, 0.5)
        expected_energy = 50 - 0.5 * ENERGY_LOST_PER_TICK_HOUR
        expected_hunger = 50 - 0.5 * HUNGER_LOST_PER_TICK_HOUR
        expected_happiness = 50 - 0.5 * HAPPINESS_LOST_PER_TICK_HOUR
        assert pet.energy == expected_energy, f"Expected energy {expected_energy}, got {pet.energy}"
        assert pet.hunger == expected_hunger, f"Expected hunger {expected_hunger}, got {pet.hunger}"
        assert pet.happiness == expected_happiness, f"Expected happiness {expected_happiness}, got {pet.happiness}"

    def test_tick_does_not_go_below_min_hunger(self):
        pet = Pet("Mochi", "cat", hunger=5, energy=50, happiness=50)
        tick(pet, MAX_TICK_HOURS)
        assert pet.hunger == STAT_MIN, f"Expected hunger to be at least {STAT_MIN}, got {pet.hunger}"

    def test_tick_does_not_go_below_min_energy(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=5, happiness=50)
        tick(pet, MAX_TICK_HOURS)
        assert pet.energy == STAT_MIN, f"Expected energy to be at least {STAT_MIN}, got {pet.energy}"

    def test_tick_does_not_go_below_min_happiness(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=5)
        tick(pet, MAX_TICK_HOURS)
        assert pet.happiness == STAT_MIN, f"Expected happiness to be at least {STAT_MIN}, got {pet.happiness}"

    def test_tick_does_not_exceed_one_day_limit(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        with pytest.raises(ValueError):
            tick(pet, MAX_TICK_HOURS + 1)

    def test_tick_accepts_maximum_hours(self):
        pet = Pet("Mochi", "cat", hunger=100, energy=100, happiness=100)
        tick(pet, MAX_TICK_HOURS)
        assert pet.energy == 100 - MAX_TICK_HOURS * ENERGY_LOST_PER_TICK_HOUR
        assert pet.hunger == 100 - MAX_TICK_HOURS * HUNGER_LOST_PER_TICK_HOUR
        assert pet.happiness == 100 - MAX_TICK_HOURS * HAPPINESS_LOST_PER_TICK_HOUR

    def test_tick_hour_just_over_max(self):
        with pytest.raises(ValueError):
            tick(self.pet, MAX_TICK_HOURS + 0.01)

    def test_tick_zero_hours_raises_value_error(self):
        with pytest.raises(ValueError):
            tick(self.pet, 0)

    def test_tick_negative_hours_raises_value_error(self):
        with pytest.raises(ValueError):
            tick(self.pet, -1)

    def test_tick_non_numeric_hours_raises_type_error(self):
        with pytest.raises(TypeError):
            tick(self.pet, "two")
        with pytest.raises(TypeError):
            tick(self.pet, "2")
        with pytest.raises(TypeError):
            tick(self.pet, None)
        with pytest.raises(TypeError):
            tick(self.pet, True)

    def test_tick_with_non_pet_raises_type_error(self):
        with pytest.raises(TypeError):
            tick("not_a_pet", 1)
        with pytest.raises(TypeError):
            tick(123, 1)
        with pytest.raises(TypeError):
            tick(None, 1)
        with pytest.raises(TypeError):
            tick([], 1)

    def test_failed_tick_leaves_pet_unchanged(self):
        with pytest.raises(ValueError):
            tick(self.pet, MAX_TICK_HOURS + 1)  # Invalid tick should not change the pet
        assert self.pet.energy == 50, f"Expected energy to remain 50, got {self.pet.energy}"
        assert self.pet.hunger == 50, f"Expected hunger to remain 50, got {self.pet.hunger}"
        assert self.pet.happiness == 50, f"Expected happiness to remain 50, got {self.pet.happiness}"

    def test_tick_reaches_min_exactly(self):
        pet = Pet(
            "Mochi", "cat",
            hunger=HUNGER_LOST_PER_TICK_HOUR,
            energy=ENERGY_LOST_PER_TICK_HOUR,
            happiness=HAPPINESS_LOST_PER_TICK_HOUR,
        )
        tick(pet, 1)
        assert pet.hunger == STAT_MIN
        assert pet.energy == STAT_MIN
        assert pet.happiness == STAT_MIN

    def test_tick_pet_at_min_stays_at_min(self):
        pet = Pet("Mochi", "cat", hunger=0, energy=0, happiness=0)
        tick(pet, 3)
        assert (pet.hunger, pet.energy, pet.happiness) == (STAT_MIN, STAT_MIN, STAT_MIN)

    def test_tick_stats_stay_within_bounds(self):
        tick(self.pet, 12)
        for stat in (self.pet.hunger, self.pet.energy, self.pet.happiness):
            assert STAT_MIN <= stat <= STAT_MAX

    def test_repeated_ticks_accumulate(self):
        tick(self.pet, 1)
        tick(self.pet, 1)
        assert self.pet.energy == 50 - 2 * ENERGY_LOST_PER_TICK_HOUR
        assert self.pet.hunger == 50 - 2 * HUNGER_LOST_PER_TICK_HOUR
        assert self.pet.happiness == 50 - 2 * HAPPINESS_LOST_PER_TICK_HOUR

    def test_tick_error_messages(self):
        with pytest.raises(TypeError, match="pet must be a Pet"):
            tick("not_a_pet", 1)
        with pytest.raises(TypeError, match="hours must be a number"):
            tick(self.pet, "1")
        with pytest.raises(ValueError, match="greater than 0 and at most 24"):
            tick(self.pet, 0)
