import pytest
from termpet import Pet, status

@pytest.fixture
def pet():
    return Pet(name="Mochi", species="cat", hunger=30, energy=70, happiness=100)

class TestStatusValid:
    def test_short_form_exact(self, pet):
        assert status(pet) == "Mochi the cat | Hunger 30 | Energy 70 | Happiness 100"

    def test_short_form_is_single_line(self, pet):
        assert "\n" not in status(pet)

    def test_short_form_uses_name_and_species(self):
        p = Pet(name="Biscuit", species="dog")
        assert status(p).startswith("Biscuit the dog | ")

    def test_verbose_has_header_and_three_stats(self, pet):
        lines = status(pet, verbose=True).split("\n")
        assert len(lines) == 4
        assert lines[0] == "Mochi the cat"

    def test_verbose_bars(self, pet):
        lines = status(pet, verbose=True).split("\n")
        assert lines[1] == "Hunger    ███░░░░░░░  30"
        assert lines[2] == "Energy    ███████░░░  70"
        assert lines[3] == "Happiness ██████████ 100"

    @pytest.mark.parametrize("value, filled", [(0, 0), (50, 5), (100, 10)])
    def test_bar_extremes(self, value, filled):
        p = Pet(name="Mochi", species="cat", hunger=value)
        hunger_line = status(p, verbose=True).split("\n")[1]
        assert hunger_line.count("█") == filled
        assert hunger_line.count("░") == 10 - filled

    def test_verbose_false_matches_default(self, pet):
        assert status(pet, verbose=False) == status(pet)

    def test_does_not_change_pet(self, pet):
        before = Pet(name="Mochi", species="cat", hunger=30, energy=70, happiness=100)
        status(pet, verbose=True)
        assert pet == before

class TestStatusInvalid:
    @pytest.mark.parametrize("bad_pet", [None, "Mochi", 42])
    def test_non_pet_raises(self, bad_pet):
        with pytest.raises(TypeError):
            status(bad_pet)

    @pytest.mark.parametrize("bad_verbose", ["yes", 1, None])
    def test_non_bool_verbose_raises(self, pet, bad_verbose):
        with pytest.raises(TypeError):
            status(pet, verbose=bad_verbose)