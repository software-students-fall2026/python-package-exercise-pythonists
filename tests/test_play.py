import pytest
from termpet.constants import (
    GAMES,
    MAX_PLAY_MINUTES,
    STAT_MAX,
    STAT_MIN,
)
from termpet.pet import Pet
from termpet.play import play

class Tests:

    def setup_method(self):
        self.pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)

    def test_play_returns_the_pet(self):
        result = play(self.pet, "fetch", 10)
        assert result is self.pet, "Expected play() to return the same pet object"

    def test_play_increases_happiness(self):
        initial_happiness = self.pet.happiness
        play(self.pet, "fetch", 10)
        assert self.pet.happiness > initial_happiness, "Expected happiness to increase after playing"

    def test_play_reduces_energy(self):
        initial_energy = self.pet.energy
        play(self.pet, "fetch", 10)
        assert self.pet.energy < initial_energy, "Expected energy to decrease after playing"

    def test_play_reduces_hunger(self):
        initial_hunger = self.pet.hunger
        play(self.pet, "fetch", 10)
        assert self.pet.hunger < initial_hunger, "Expected hunger to decrease after playing"

    def test_play_with_different_games(self):
        for game, effect in GAMES.items():
            pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
            play(pet, game, 10)
            assert pet.hunger == 50 + effect["hunger"] * 10, f"Wrong hunger after playing {game}, got {pet.hunger}"
            assert pet.energy == 50 + effect["energy"] * 10, f"Wrong energy after playing {game}, got {pet.energy}"
            assert pet.happiness == 50 + effect["happiness"] * 10, f"Wrong happiness after playing {game}, got {pet.happiness}"

    def test_play_with_whitespace_uppercase_game_name(self):
        initial_happiness = self.pet.happiness
        play(self.pet, "  FETCH  ", 10)
        assert self.pet.happiness > initial_happiness, "Expected happiness to increase after playing with whitespace in game name"

    def test_play_with_default_minutes(self):
        initial_happiness = self.pet.happiness
        other = Pet("Mochi", "cat", hunger=50, energy=50, happiness=50)
        play(self.pet, "fetch")
        play(other, "fetch", 10)
        assert self.pet == other, "Expected default minutes to behave the same as 10 minutes"

    def test_play_accepts_partial_minutes(self):
        initial_happiness = self.pet.happiness
        play(self.pet, "fetch", 0.5)
        assert self.pet.happiness > initial_happiness, "Expected happiness to increase after playing for partial minutes"

    def test_play_does_not_go_above_max_happiness(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=50, happiness=STAT_MAX - 1)
        play(pet, "fetch", 10)
        assert pet.happiness == STAT_MAX, f"Expected happiness to stop at {STAT_MAX}, got {pet.happiness}"

    def test_play_does_not_go_below_min_energy(self):
        pet = Pet("Mochi", "cat", hunger=50, energy=STAT_MIN + 1, happiness=50)
        play(pet, "fetch", 10)
        assert pet.energy == STAT_MIN, f"Expected energy to stop at {STAT_MIN}, got {pet.energy}"

    def test_play_does_not_go_below_min_hunger(self):
        pet = Pet("Mochi", "cat", hunger=STAT_MIN + 1, energy=50, happiness=50)
        play(pet, "fetch", 10)
        assert pet.hunger == STAT_MIN, f"Expected hunger to stop at {STAT_MIN}, got {pet.hunger}"

    def test_play_zero_minutes_raises_value_error(self):
        with pytest.raises(ValueError):
            play(self.pet, "fetch", 0)
    
    def test_play_negative_minutes_raises_value_error(self):
        with pytest.raises(ValueError):
            play(self.pet, "fetch", -5)

    def test_play_too_many_minutes_raises_value_error(self):
        with pytest.raises(ValueError):
            play(self.pet, "fetch", MAX_PLAY_MINUTES + 1)

    def test_play_accepts_max_minutes(self):
        play(self.pet, "fetch", MAX_PLAY_MINUTES)
        assert self.pet.happiness == STAT_MAX, f"Expected happiness to cap at {STAT_MAX}, got {self.pet.happiness}"
        assert self.pet.energy == STAT_MIN, f"Expected energy to floor at {STAT_MIN}, got {self.pet.energy}"
        assert self.pet.hunger == STAT_MIN, f"Expected hunger to floor at {STAT_MIN}, got {self.pet.hunger}"

    def test_play_with_non_pet_raises_type_error(self):
        with pytest.raises(TypeError):
            play("not_a_pet", "fetch", 1)
        with pytest.raises(TypeError):
            play(123, "fetch", 1)
        with pytest.raises(TypeError):
            play(None, "fetch", 1)
        with pytest.raises(TypeError):
            play([], "fetch", 1)

    def test_play_invalid_game_raises_value_error(self):
        with pytest.raises(ValueError):
            play(self.pet, "invalid_game", 10)
        with pytest.raises(ValueError):
            play(self.pet, "   ", 10)
        with pytest.raises(ValueError):
            play(self.pet, "", 10)
        with pytest.raises(ValueError):
            play(self.pet, "fetching", 10)  

    def test_play_non_string_game_raises_type_error(self):
        with pytest.raises(TypeError):
            play(self.pet, 123, 10)
        with pytest.raises(TypeError):
            play(self.pet, None, 10)
        with pytest.raises(TypeError):
            play(self.pet, [], 10)
        with pytest.raises(TypeError):
            play(self.pet, {}, 10)

    def test_play_non_number_minutes_raises_type_error(self):
        with pytest.raises(TypeError):
            play(self.pet, "fetch", "10")
        with pytest.raises(TypeError):
            play(self.pet, "fetch", None)
        with pytest.raises(TypeError):
            play(self.pet, "fetch", [])
        with pytest.raises(TypeError):
            play(self.pet, "fetch", {})
        with pytest.raises(TypeError):
            play(self.pet, "fetch", True)

    def test_failed_play_leaves_pet_unchanged(self):
        initial_hunger = self.pet.hunger
        initial_energy = self.pet.energy
        initial_happiness = self.pet.happiness
        with pytest.raises(ValueError):
            play(self.pet, "fetch", -5)
        assert self.pet.hunger == initial_hunger, "Expected hunger to be unchanged after failed play"
        assert self.pet.energy == initial_energy, "Expected energy to be unchanged after failed play"
        assert self.pet.happiness == initial_happiness, "Expected happiness to be unchanged after failed play"
        with pytest.raises(ValueError):
            play(self.pet, "invalid_game", 10)
        assert self.pet.hunger == initial_hunger, "Expected hunger to be unchanged after failed play"
        assert self.pet.energy == initial_energy, "Expected energy to be unchanged after failed play"
        assert self.pet.happiness == initial_happiness, "Expected happiness to be unchanged after failed"

