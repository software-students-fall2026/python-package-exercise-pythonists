"""Tests for the basic shared Pet interface."""

import pytest

from termpet import Pet, mood


def test_pet_starts_with_the_supplied_identity_and_default_stats(pet):
    assert pet.name == "Mochi"
    assert pet.species == "cat"
    assert pet.hunger == 50
    assert pet.energy == 50
    assert pet.happiness == 50


def test_pet_accepts_restored_stats_including_boundaries_and_fractions():
    restored = Pet("Biscuit", "dog", hunger=0, energy=100, happiness=25.5)

    assert restored.name == "Biscuit"
    assert restored.species == "dog"
    assert restored.hunger == 0
    assert restored.energy == 100
    assert restored.happiness == 25.5


def test_pets_have_independent_editable_stats(pet):
    other_pet = Pet("Biscuit", "dog")

    pet.hunger = 20
    pet.energy = 30
    pet.happiness = 40

    assert (pet.hunger, pet.energy, pet.happiness) == (20, 30, 40)
    assert (other_pet.hunger, other_pet.energy, other_pet.happiness) == (50, 50, 50)
    assert pet is not other_pet


@pytest.mark.parametrize("field", ["name", "species"])
@pytest.mark.parametrize("value", ["", "   "])
def test_pet_rejects_blank_identity_fields(field, value):
    arguments = {"name": "Mochi", "species": "cat", field: value}

    with pytest.raises(ValueError, match=field):
        Pet(**arguments)


@pytest.mark.parametrize("field", ["name", "species"])
@pytest.mark.parametrize("value", [None, 123])
def test_pet_requires_text_identity_fields(field, value):
    arguments = {"name": "Mochi", "species": "cat", field: value}

    with pytest.raises(TypeError, match=field):
        Pet(**arguments)


@pytest.mark.parametrize("field", ["hunger", "energy", "happiness"])
@pytest.mark.parametrize("value", [-1, 101, float("nan"), float("inf")])
def test_pet_rejects_stats_outside_the_valid_range(field, value):
    with pytest.raises(ValueError, match=field):
        Pet("Mochi", "cat", **{field: value})


@pytest.mark.parametrize("field", ["hunger", "energy", "happiness"])
@pytest.mark.parametrize("value", [None, "50", True])
def test_pet_requires_numeric_stats(field, value):
    with pytest.raises(TypeError, match=field):
        Pet("Mochi", "cat", **{field: value})


def test_mood_at_stat_boundaries():
    assert mood(Pet("Mochi", "cat", 0, 0, 0)) == "feral"
    assert mood(Pet("Mochi", "cat", 24.9, 24.9, 24.9)) == "feral"
    assert mood(Pet("Mochi", "cat", 25, 25, 25)) == "grumpy"
    assert mood(Pet("Mochi", "cat", 49.9, 49.9, 49.9)) == "grumpy"
    assert mood(Pet("Mochi", "cat", 50, 50, 50)) == "content"
    assert mood(Pet("Mochi", "cat", 74.9, 74.9, 74.9)) == "content"
    assert mood(Pet("Mochi", "cat", 75, 75, 75)) == "ecstatic"
    assert mood(Pet("Mochi", "cat", 100, 100, 100)) == "ecstatic"


def test_mood_uses_the_average_of_all_three_stats():
    assert mood(Pet("Mochi", "cat", 100, 25, 25)) == "content"
    assert mood(Pet("Mochi", "cat", 25, 100, 25)) == "content"
    assert mood(Pet("Mochi", "cat", 25, 25, 100)) == "content"


def test_mood_leaves_the_pet_unchanged():
    pet = Pet("Mochi", "cat", 25, 50, 75)
    assert mood(pet) == "content"
    assert (pet.name, pet.species) == ("Mochi", "cat")
    assert (pet.hunger, pet.energy, pet.happiness) == (25, 50, 75)


def test_mood_rejects_inputs_that_are_not_pets():
    for value in [None, {}, "cat", 50]:
        with pytest.raises(TypeError, match="pet must be a Pet"):
            mood(value)
