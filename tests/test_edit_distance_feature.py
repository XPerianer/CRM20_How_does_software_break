import pandas

import pytest

from src.edit_distance_feature import edit_distance_feature


@pytest.fixture()
def dataframe():
    data = {'method_name': ['method_one', 'method_two', 'three'], 'test_name': ['method_one', 'method', 'four']}
    pd = pandas.DataFrame(data)
    return pd


def test_edit_distance_feature(dataframe):
    edit_distances = edit_distance_feature(dataframe['method_name'], dataframe['test_name'])
    assert edit_distances == [0, 4, 5]
