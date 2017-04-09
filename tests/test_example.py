import pytest
from example import Example

good_observation = [1, 1, 'B']
good_observation_2 = [1, 1, 3]
not_only_numbers_observation = ['x', 'sd', 1]
no_numbers_observation = ['a', 'b']
too_small_observation = [1]


def test_example_constructor_too_small_observation():
    with pytest.raises(ValueError):
        assert Example(too_small_observation)


def test_example_constructor_empty_observation():
    with pytest.raises(ValueError):
        assert Example([])


def test_example_constructor_not_only_numerical_coordinates():
    with pytest.raises(ValueError):
        assert Example(not_only_numbers_observation)


def test_example_constructor_no_numerical_coordinates():
    with pytest.raises(ValueError):
        assert Example(no_numbers_observation)


def test_good_observation():
    assert Example(good_observation)


def test_good_observation_numerical_class():
    assert Example(good_observation_2)
