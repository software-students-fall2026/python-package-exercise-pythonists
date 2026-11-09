import pytest
from termpet.render import render

def test_render_shows_the_pet_and_its_stats(pet):
    pet.hunger = 0
    pet.energy = 100
    pet.happiness = 25

    picture = render(pet, width=4)

    assert "Mochi the cat" in picture
    assert "Hunger [----]" in picture
    assert "Energy [####]" in picture
    assert "Happiness [#---]" in picture

def test_render_default_width(pet):
    assert "Hunger [#####-----]" in render(pet)

def test_render_invalid_width(pet):
    with pytest.raises(ValueError):
        render(pet, width=0)
    with pytest.raises(TypeError):
        render(pet, width=True)

def test_render_invalid_pet():
    with pytest.raises(TypeError):
        render("Mochi")
