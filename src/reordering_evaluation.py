from typing import List
from pandas import DataFrame


class ReorderingEvaluation:
    def __init__(self, ordering: List[int], dataframe: DataFrame):
        self.ordering = ordering
        self.dataframe = dataframe
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
        # We first find the positions of failing tests in the given order
        summed_positions = 0.0
        for row in self.dataframe.loc[self.dataframe['outcome'] == False].itertuples(index=False):
            test_id = row.test_id
            index = self.ordering.index(test_id) + 1 # + 1 since this should not be 0 indexed
            summed_positions += index

        # This is just the formulat from the literature
        number_of_failed_tests = self.dataframe.loc[self.dataframe['outcome'] == False].shape[0]
        number_of_tests = len(self.ordering)
        return 1.0 + 1.0 / (2 * number_of_tests) - summed_positions / (number_of_tests * number_of_failed_tests)



