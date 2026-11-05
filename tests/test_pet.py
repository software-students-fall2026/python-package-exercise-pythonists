"""Tests for the basic shared Pet interface."""

import pytest

from termpet import Pet


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
