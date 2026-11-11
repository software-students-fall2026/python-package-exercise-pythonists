# termpet

[![CI](https://github.com/software-students-fall2026/python-package-exercise-pythonists/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-fall2026/python-package-exercise-pythonists/actions/workflows/ci.yml)

A small virtual pet that lives in your terminal. Adopt a pet, feed it, play with it, let time pass, put it to sleep, and save it to a file so it's still there next time. Its mood changes with how well you look after it, and you can draw it as ASCII art.

**PyPI:** [termpet-pythonists](https://pypi.org/project/termpet-pythonists/)

## Installation

```bash
pip install termpet-pythonists
```

The package installs as `termpet-pythonists` but you import it as `termpet`:

```python
import termpet
```

Requires Python 3.12 or newer.

## Quick start

```python
from termpet import Pet, feed, play, tick, sleep, mood, render, status, save, load

pet = Pet(name="Mochi", species="cat")
feed(pet, "steak")
tick(pet, 4)
sleep(pet, 2)
print(render(pet))
save(pet, "mochi.json")
```

Each action function updates the pet you pass in and returns the same pet, so you can call them on their own or chain the result.

## Pet stats

Every pet has three stats, each from 0 to 100. All start at 50.

| Stat | 0 means | 100 means |
|---|---|---|
| `hunger` | starving | full |
| `energy` | exhausted | fully rested |
| `happiness` | miserable | ecstatic |

Stats are kept between 0 and 100 automatically; actions never push them outside that range.

## Functions

### `Pet(name, species, hunger=50, energy=50, happiness=50)`

Creates a pet. `name` and `species` are required and can be any non-blank text. The three stats are optional, which is useful for restoring a pet with known values.

```python
pet = Pet(name="Mochi", species="cat")
tired = Pet(name="Biscuit", species="dog", energy=10)
```

Raises:
- `TypeError` if `name` or `species` isn't a string, or a stat isn't a number.
- `ValueError` if `name` or `species` is blank, or a stat is outside 0–100.

### `mood(pet)`

Returns the pet's mood as a string, based on the average of its three stats.

| Average stat | Mood |
|---|---|
| 75 or higher | `"ecstatic"` |
| 50 to 74 | `"content"` |
| 25 to 49 | `"grumpy"` |
| below 25 | `"feral"` |

```python
>>> mood(Pet(name="Mochi", species="cat"))
'content'
```

Raises `TypeError` if `pet` isn't a `Pet`.

### `feed(pet, food)`

Feeds the pet and returns it. Food names ignore case and surrounding spaces.

| Food | Hunger | Energy | Happiness |
|---|---|---|---|
| `apple` | +10 | +5 | +2 |
| `kibble` | +20 | 0 | +1 |
| `steak` | +35 | +5 | +10 |
| `treat` | +5 | +15 | +15 |
| `veggies` | +15 | 0 | 0 |

```python
feed(pet, "treat")
feed(pet, "  Steak ")   # same as "steak"
```

Raises:
- `TypeError` if `pet` isn't a `Pet` or `food` isn't a string.
- `ValueError` if `food` isn't one of the foods above.

### `play(pet, game, minutes=10)`

Plays a game with the pet for `minutes` minutes and returns it. Each game changes the pet's stats by a set amount per minute, so longer play has a bigger effect. Game names ignore case and surrounding spaces.

| Game | Hunger / min | Energy / min | Happiness / min |
|---|---|---|---|
| `fetch` | −1 | −1 | +2 |
| `hide & seek` | −0.5 | −0.5 | +1.5 |
| `tug of war` | −1.5 | −1.5 | +2.5 |
| `chase` | −2 | −2 | +3 |

`minutes` can be a whole or decimal number, greater than 0 and at most MAX_PLAY_MINUTES (60), defaulting at 10 minutes.

```python
pet = Pet(name="Mochi", species="cat")   # all stats start at 50
play(pet, "fetch")  # 10 minutes default
print(pet.hunger, pet.energy, pet.happiness) # 40 40 70

play(pet, "  Hide & Seek ", 5)           # same as "hide & seek"
```

Raises:
- `TypeError` if `pet` isn't a `Pet`, `game` isn't a string, or `minutes` isn't a number.
- `ValueError` if `game` isn't one of the games above, or `minutes` is 0 or less, or more than MAX_PLAY_MINUTES.

### `tick(pet, hours)`

Lets time pass and returns the pet. Each hour lowers its stats:

| Stat | Change per hour |
|---|---|
| `hunger` | −4 |
| `energy` | −2 |
| `happiness` | −3 |

`hours` can be a whole or decimal number, greater than 0 and at most 24.

```python
tick(pet, 6)     # six hours pass
tick(pet, 0.5)   # half an hour passes
```

Raises:
- `TypeError` if `pet` isn't a `Pet` or `hours` isn't a number.
- `ValueError` if `hours` is 0 or less, or more than 24.

### `sleep(pet, hours)`

Puts the pet to sleep and returns it. Each hour adds 10 energy and lowers hunger by 2. `hours` must be greater than 0 and at most 24.

```python
sleep(pet, 8)
```

Raises:
- `TypeError` if `pet` isn't a `Pet` or `hours` isn't a number.
- `ValueError` if `hours` is 0 or less, or more than 24.

### `render(pet, width=10)`

Returns the pet as ASCII art, with a face that matches its mood and a bar for each stat. `width` sets how many characters long each bar is.

```python
>>> print(render(Pet(name="Mochi", species="cat", hunger=80, energy=70, happiness=90)))
  /\_/\
 ( ^.^ )  Mochi the cat — ecstatic
  > ^ <
Hunger [########--]
Energy [#######---]
Happiness [#########-]
```

Faces by mood: `^.^` ecstatic, `o.o` content, `-.-` grumpy, `>.<` feral.

Raises:
- `TypeError` if `pet` isn't a `Pet` or `width` isn't a whole number.
- `ValueError` if `width` is less than 1.

### `status(pet, verbose=False)`

Returns a text summary of the pet's stats.

```python
>>> pet = Pet(name="Mochi", species="cat", hunger=30, energy=70, happiness=100)
>>> print(status(pet))
Mochi the cat | Hunger 30 | Energy 70 | Happiness 100

>>> print(status(pet, verbose=True))
Mochi the cat
Hunger    ███░░░░░░░  30
Energy    ███████░░░  70
Happiness ██████████ 100
```

Raises `TypeError` if `pet` isn't a `Pet` or `verbose` isn't `True`/`False`.

### `save(pet, path)` and `load(path)`

Save a pet to a JSON file and load it back.

```python
save(pet, "mochi.json")
pet = load("mochi.json")
```

`save` overwrites an existing file. `path` can be a string or a `pathlib.Path`.

Raises:
- `TypeError` if `pet` isn't a `Pet` or `path` isn't a string or `Path`.
- `ValueError` from `save` if `path` is empty.
- `FileNotFoundError` from `load` if the file doesn't exist.
- `ValueError` from `load` if the file isn't valid JSON or doesn't describe a valid pet.

## Example program

[`examples/play_demo.py`](examples/play_demo.py) is an interactive demo and uses every function in the package.

With a fresh clone, after running `pipenv install --dev`:
```bash
pipenv run python examples/play_demo.py
```


If you installed the package from PyPI download the file and run:

```bash
python examples/play_demo.py
```

## Contributing

### Setup

You need Python 3.12+ and [pipenv](https://pipenv.pypa.io/).

```bash
git clone https://github.com/software-students-fall2026/python-package-exercise-pythonists.git
cd python-package-exercise-pythonists
pipenv install --dev
```

If `pipenv` isn't installed, run `python -m pip install --user pipenv` (or `brew install pipenv` on macOS). On macOS and Linux, use `python3` wherever these instructions say `python` if `python` isn't found.

### Run the tests

```bash
pipenv run python -m pytest
```

### Build the package

```bash
pipenv run python -m build
```

This creates a source distribution and a wheel in `dist/`.

### Workflow

1. Create a feature branch from `main`.
2. Make your changes and run the tests.
3. Push the branch and open a pull request into `main` on this repository, not the upstream course repository.
4. A teammate reviews the code and runs the tests before merging.

GitHub Actions runs the tests and builds the package on Python 3.12 and 3.13 for every pull request and push to `main`.

## Configuration

termpet needs no environment variables, secret files, or database.

## Team

- [Hoang Ngo](https://github.com/ogngnaoh)
- [Jolie Leong](https://github.com/jl15113)
- [Layan Alyas](https://github.com/layan-al)
- [Ray Yang](https://github.com/rayyang262)
- [Ryan Lin](https://github.com/ryanwlin)