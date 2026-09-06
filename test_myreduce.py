import pytest
from myreduce import myreduce
from random import randint
from functools import reduce

def sum(a, b):
    return a + b


def test_empty_list_with_no_initial():
    with pytest.raises(ValueError, match="empty list with no initial value"):
        myreduce(lambda x, y: x + y, [])


def test_empty_list_with_initial():
    # input = [random.randint(1, 100) for _ in range(5)]
    initial = randint(1, 100)

    result = myreduce(sum, [], initial)

    assert result == initial


def test_list_with_one_element():
    rand = randint(1, 100)
    input = [rand]

    result = myreduce(sum, input)

    assert result == rand


def test_nontrivial_list():
    input = [randint(1, 100) for _ in range(5)]
    expected = reduce(sum, input)

    result = myreduce(sum, input)

    assert result == expected


def test_nontrivial_with_initial():
    input = [randint(1, 100) for _ in range(5)]
    initial = randint(1, 1000)
    expected = reduce(sum, input, initial)

    result = myreduce(sum, input, initial)

    assert result == expected