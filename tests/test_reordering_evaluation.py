import pandas
import pytest

from src.reordering_evaluation import ReorderingEvaluation


@pytest.fixture()
def dataframe():
    data = {'test_id': [1, 2, 3, 4, 5], 'outcome': [True, False, True, False, False], 'duration': [1, 2, 3, 4, 5]}
    pd = pandas.DataFrame(data)
    return pd


@pytest.fixture()
def linear_ordering():
    return [1, 2, 3, 4, 5]


@pytest.fixture()
def reverse_ordering():
    return [5, 4, 3, 2, 1]


@pytest.fixture()
def good_ordering():
    return [2, 4, 5, 1, 3]


def test_linear_ordering(linear_ordering, dataframe):
    r = ReorderingEvaluation(linear_ordering, dataframe)
    assert r.first_failing_duration() == 3
    assert r.last_test_failing_duration() == 15
    assert round(r.APFD(), 6) == round(0.36666666666, 6)


def test_reverse_ordering(reverse_ordering, dataframe):
    r = ReorderingEvaluation(reverse_ordering, dataframe)
    assert r.first_failing_duration() == 5
    assert r.last_test_failing_duration() == 14
    assert round(r.APFD(), 6) == round(0.6333333333, 6)


def test_good_ordering(good_ordering, dataframe):
    r = ReorderingEvaluation(good_ordering, dataframe)
    assert r.first_failing_duration() == 2
    assert r.last_test_failing_duration() == 11
    assert round(r.APFD(), 6) == round(0.7, 6)
