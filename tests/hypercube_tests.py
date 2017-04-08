from nose.tools import *
from hypercube import Hypercube
import mock
from mock import Mock
from example import Example

correct_coords=[1,1]
not_only_numerical_coords=['a',1,1,1]
no_numbers_coords=['ab','dd']


def test_hypercube_constructor_correct_coordinates():
    assert Hypercube(correct_coords)

@raises(ValueError)
def test_hypercube_constructor_not_only_numerical_coordinates():
    assert Hypercube(not_only_numerical_coords)

@raises(ValueError)
def test_hypercube_constructor_nonumbers_coordinates():
    assert Hypercube(no_numbers_coords)

@raises(ValueError)
def test_hypercube_constructor_empty_coordinates():
    assert Hypercube([])

# def test_set_hypercube_class():
#
#     mock = Mock(examples=[0,1], class_dict=None)
#     mock.set_hypercube_class()
#     print(mock.class_dict)
