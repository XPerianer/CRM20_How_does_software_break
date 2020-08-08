from typing import List
from pandas import DataFrame

import pandas as pd
import numpy as np


class ReorderingEvaluation:
    def __init__(self, ordering: List[int], dataframe: DataFrame):
        self.ordering = ordering
        self.number_of_tests = len(self.ordering)
        self.dataframe = dataframe
        self.number_of_failed_tests = self.dataframe.loc[self.dataframe['outcome'] == False].shape[0]
        # TODO: assert that ordering and dataframe are kind of legit

    def first_failing_duration(self):
        summed_duration = 0
        for test_id in self.ordering:
            rows = self.dataframe.loc[self.dataframe['test_id'] == test_id]
            assert rows.shape[0] == 1, "The provided dataframe contains more than one entry for the given test_id"

            summed_duration += rows['duration'].iloc[0]
            if rows['outcome'].iloc[0] == False:
                return summed_duration
        return summed_duration


    def last_test_failing_duration(self):
        summed_duration = 0
        temporary_duration = 0
        for test_id in self.ordering:
            rows = self.dataframe.loc[self.dataframe['test_id'] == test_id]
            assert rows.shape[0] == 1, "The provided dataframe contains more than one entry for the given test_id"

            if rows['outcome'].iloc[0] == True:
                temporary_duration += rows['duration'].iloc[0]
            if rows['outcome'].iloc[0] == False:
                summed_duration += temporary_duration + rows['duration'].iloc[0]
                temporary_duration = 0

        return summed_duration

    ### Calculates the widespread used Average Percentage of Faults detected metric
    ### We have the simplification here, that we say that each test failure is a defect,
    ### anc vice versa, so the number of failed tests is the number of faults
    ### While this is not realisitic, as probably some integration tests test the same as others,
    ### it is easier to calculate
    # TODO: How to format these nice docstrings?
    def APFD(self):
        number_encoded_test_outcomes = [0] # We always start at the beginning with 0 known failures and 0 executed tests
        for test_id in self.ordering:
            number_encoded_test_outcomes.append(not self.dataframe.loc[self.dataframe['test_id'] == test_id, 'outcome'].values[0])

        summed_number_encoded_test_outcome = np.cumsum(number_encoded_test_outcomes) * 1 / self.number_of_failed_tests

        return np.trapz(summed_number_encoded_test_outcome, np.linspace(0, 1, num=(self.number_of_tests + 1)))

    def APFDc(self):
        number_encoded_test_outcomes = [0] # We always start at the beginning with 0 known failures and 0 executed tests
        durations_test_outcomes = [0]
        for test_id in self.ordering:
            number_encoded_test_outcomes.append(not self.dataframe.loc[self.dataframe['test_id'] == test_id, 'outcome'].values[0])
            durations_test_outcomes.append(self.dataframe.loc[self.dataframe['test_id'] == test_id, 'duration'].values[0])

        summed_number_encoded_test_outcome = np.cumsum(number_encoded_test_outcomes) * 1 / self.number_of_failed_tests
        summed_durations_test_outcomes = np.cumsum(durations_test_outcomes) * 1 / np.sum(durations_test_outcomes)

        return np.trapz(summed_number_encoded_test_outcome, summed_durations_test_outcomes)





