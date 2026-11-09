import json
from dataclasses import asdict, fields
from pathlib import Path
from .pet import Pet

def save(pet, path):
    if not isinstance(pet, Pet):
        raise TypeError(f"pet must be a Pet, got {type(pet).__name__}")
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be a str or Path, got {type(path).__name__}")
    if str(path).strip() == "":
        raise ValueError("path must not be empty")
    Path(path).write_text(json.dumps(asdict(pet), indent=2), encoding="utf-8")

def load(path):
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be a str or Path, got {type(path).__name__}")
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError as err:
        raise ValueError(f"{path} is not valid JSON") from err
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a pet object")
    known = {f.name for f in fields(Pet)}
    try:
        return Pet(**{k: v for k, v in data.items() if k in known})
    except TypeError as err:
        raise ValueError(f"{path} does not contain a valid pet: {err}") from err