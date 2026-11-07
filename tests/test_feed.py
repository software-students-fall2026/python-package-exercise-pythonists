import pytest
from termpet.constants import FOODS, STAT_MAX, STAT_MIN
from termpet.feed import feed
from termpet.pet import Pet


class Tests:

    def setup_method(self):
        self.pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)

    def test_feed_returns_the_pet(self):
        result = feed(self.pet, "kibble")
        assert result is self.pet, "Expected feed() to return the same pet object"

    def test_feed_increases_fullness(self):
        feed(self.pet, "kibble")
        expected = 50 + FOODS["kibble"]["hunger"]
        assert self.pet.hunger == expected, f"Expected hunger {expected}, got {self.pet.hunger}"
        assert self.pet.hunger > 50, "Expected the pet to be more full than before"

    def test_feed_can_change_energy_and_happiness(self):
        feed(self.pet, "steak")
        expected_energy = 50 + FOODS["steak"]["energy"]
        expected_happiness = 50 + FOODS["steak"]["happiness"]
        assert self.pet.energy == expected_energy, f"Expected energy {expected_energy}, got {self.pet.energy}"
        assert self.pet.happiness == expected_happiness, f"Expected happiness {expected_happiness}, got {self.pet.happiness}"

    def test_feed_ignores_capital_letters(self):
        feed(self.pet, "KIBBLE")
        expected = 50 + FOODS["kibble"]["hunger"]
        assert self.pet.hunger == expected, f"Expected hunger {expected}, got {self.pet.hunger}"

    def test_feed_ignores_extra_spaces(self):
        feed(self.pet, "  kibble  ")
        expected = 50 + FOODS["kibble"]["hunger"]
        assert self.pet.hunger == expected, f"Expected hunger {expected}, got {self.pet.hunger}"

    def test_feed_does_not_change_name_or_species(self):
        feed(self.pet, "kibble")
        assert self.pet.name == "Mochi", "Expected the name to stay the same"
        assert self.pet.species == "cat", "Expected the species to stay the same"

    def test_every_food_keeps_stats_in_range(self):
        for food in FOODS:
            pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
            feed(pet, food)
            assert STAT_MIN <= pet.hunger <= STAT_MAX, f"{food} pushed hunger out of range"
            assert STAT_MIN <= pet.energy <= STAT_MAX, f"{food} pushed energy out of range"
            assert STAT_MIN <= pet.happiness <= STAT_MAX, f"{food} pushed happiness out of range"

    def test_feed_does_not_go_above_max(self):
        pet = Pet("Mochi", "cat", hunger=STAT_MAX - 1)
        feed(pet, "steak")
        assert pet.hunger == STAT_MAX, f"Expected hunger to stop at {STAT_MAX}, got {pet.hunger}"

    def test_feed_does_not_go_below_min(self):
        pet = Pet("Mochi", "cat", hunger=0, energy=0, happiness=0)
        feed(pet, "veggies")
        assert pet.happiness == STAT_MIN, f"Expected happiness to stop at {STAT_MIN}, got {pet.happiness}"

    def test_feed_unknown_food_raises_value_error(self):
        with pytest.raises(ValueError):
            feed(self.pet, "pizza")

    def test_feed_blank_food_raises_value_error(self):
        with pytest.raises(ValueError):
            feed(self.pet, "")

    def test_feed_non_string_food_raises_type_error(self):
        with pytest.raises(TypeError):
            feed(self.pet, 5)
        with pytest.raises(TypeError):
            feed(self.pet, None)

    def test_feed_non_pet_raises_type_error(self):
        with pytest.raises(TypeError):
            feed("Mochi", "kibble")
        with pytest.raises(TypeError):
            feed(None, "kibble")

    def test_failed_feed_leaves_pet_unchanged(self):
        with pytest.raises(ValueError):
            feed(self.pet, "pizza")
        assert self.pet.hunger == 50, "Expected hunger to be unchanged"
        assert self.pet.energy == 50, "Expected energy to be unchanged"
        assert self.pet.happiness == 50, "Expected happiness to be unchanged"