import json
import pytest
from termpet import Pet, load, save

@pytest.fixture
def pet():
    return Pet(name="Mochi", species="cat", hunger=30, energy=70, happiness=90)

@pytest.fixture
def save_path(tmp_path):
    return tmp_path / "mochi.json"

class TestSaveLoadValid:
    def test_round_trip_equals_original(self, pet, save_path):
        save(pet, save_path)
        assert load(save_path) == pet

    def test_save_writes_readable_json(self, pet, save_path):
        save(pet, save_path)
        data = json.loads(save_path.read_text())
        assert data["name"] == "Mochi"
        assert data["species"] == "cat"
        assert data["hunger"] == 30

    def test_str_path_works(self, pet, save_path):
        save(pet, str(save_path))
        assert load(str(save_path)) == pet

    def test_save_overwrites(self, pet, save_path):
        save(pet, save_path)
        other = Pet(name="Biscuit", species="dog")
        save(other, save_path)
        assert load(save_path) == other

    def test_missing_optional_fields_use_defaults(self, save_path):
        save_path.write_text(json.dumps({"name": "Mochi", "species": "cat"}))
        assert load(save_path) == Pet(name="Mochi", species="cat")

    def test_unknown_keys_ignored(self, pet, save_path):
        save(pet, save_path)
        data = json.loads(save_path.read_text())
        data["favorite_color"] = "blue"
        save_path.write_text(json.dumps(data))
        assert load(save_path) == pet


class TestSaveInvalid:
    @pytest.mark.parametrize("bad_pet", [None, "Mochi", {"name": "Mochi"}])
    def test_non_pet_raises(self, bad_pet, save_path):
        with pytest.raises(TypeError):
            save(bad_pet, save_path)

    @pytest.mark.parametrize("bad_path", [None, 123, ["a.json"]])
    def test_bad_path_type_raises(self, pet, bad_path):
        with pytest.raises(TypeError):
            save(pet, bad_path)

    def test_empty_path_raises(self, pet):
        with pytest.raises(ValueError):
            save(pet, "  ")

class TestLoadInvalid:
    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            load(tmp_path / "nope.json")

    def test_corrupt_json_raises(self, save_path):
        save_path.write_text("{not json")
        with pytest.raises(ValueError, match="not valid JSON"):
            load(save_path)

    def test_non_object_json_raises(self, save_path):
        save_path.write_text("[1, 2, 3]")
        with pytest.raises(ValueError):
            load(save_path)

    @pytest.mark.parametrize("data", [{"species": "cat"}, {"name": "Mochi"}])
    def test_missing_required_field_raises(self, save_path, data):
        save_path.write_text(json.dumps(data))
        with pytest.raises(ValueError, match="valid pet"):
            load(save_path)

    @pytest.mark.parametrize("bad_path", [None, 123])
    def test_bad_path_type_raises(self, bad_path):
        with pytest.raises(TypeError):
            load(bad_path)