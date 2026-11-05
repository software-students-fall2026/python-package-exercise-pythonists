"""Fresh example pets shared by the package's tests."""

import pytest

from termpet import Pet


@pytest.fixture
def pet():
    """A pet with the default stats."""
    return Pet("Mochi", "cat")


@pytest.fixture
def hungry_pet():
    """A pet with no fullness remaining."""
    return Pet("Mochi", "cat", hunger=0)


@pytest.fixture
def tired_pet():
    """A pet with no energy remaining."""
    return Pet("Mochi", "cat", energy=0)


@pytest.fixture
def unhappy_pet():
    """A pet with no happiness remaining."""
    return Pet("Mochi", "cat", happiness=0)
