from hypercube import Hypercube
import pytest

correct_coords=[1,1]
not_only_numerical_coords=['a',1,1,1]
no_numbers_coords=['ab','dd']


def test_hypercube_constructor_correct_coordinates():
    assert Hypercube(correct_coords)

def test_hypercube_constructor_not_only_numerical_coordinates():
    with pytest.raises(ValueError):
        assert Hypercube(not_only_numerical_coords)


def test_hypercube_constructor_nonumbers_coordinates():
    with pytest.raises(ValueError):
        assert Hypercube(no_numbers_coords)


def test_hypercube_constructor_empty_coordinates():
    with pytest.raises(ValueError):
        assert Hypercube([])
