from abc import ABC, abstractmethod


class Reorderer(ABC):

    # Should output a concise name that makes it easy to identify
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def fit(self, X_train, y_train):
        raise NotImplementedError

    # Task: make an ordering for every mutant in X_test
    @abstractmethod
    def predict(self, X_test):
        raise NotImplementedError


# Just uses a linear (naive) ordering
class NaiveReorderer(Reorderer):
    def name(self):
        return "NaiveReorderer"

    def fit(self, X_train, y_train):
        pass

    def predict(self, X_test):
        test_ids = list(X_test.groupby('test_id').count().index)
        orderings = X_test.groupby('mutant_id').count()
        orderings['order'] = None
        orderings['order'] = orderings['order'].astype('object')
        for row in orderings.itertuples():
            orderings.at[row.Index, 'order'] = test_ids
        return orderings


# Executes the most often failing tests first
class AverageReorderer(Reorderer):
    def name(self):
        return "AverageReorderer"

    def fit(self, X_train, y_train):
        # Count how often the test failed in the 'mutant_id' column
        X_train = X_train.copy()
        X_train['outcome'] = y_train
        sorted_test_ids = X_train.groupby(['test_id', 'outcome']).count().unstack().loc[:,
                          ('mutant_id', False)].sort_values(ascending=False)
        # This is directly how we want our permutation to be:
        self.ordering = list(sorted_test_ids.index)

    def predict(self, X_test):
        orderings = X_test.groupby('mutant_id').count()
        orderings['order'] = None
        orderings['order'] = orderings['order'].astype('object')
        for row in orderings.itertuples():
            orderings.at[row.Index, 'order'] = self.ordering
        return orderings


# This is magic: It will first predict using a binary predictor, and then put the tests in front that you said are gonna fail.
# TODO: It will even help you more: it will sort your predicted failures after duration, so that you get short durations for the first test failing
# TODO: It should probably also weight the predicted not failing tests after the average
class BinaryPredictionReorderer(Reorderer):
    def __init__(self, predictor):
        # This predictor should be in the 
        self.predictor = predictor

    def name(self):
        return "BinaryPredictionReorderer(" + type(self.predictor).__name__ + ")"

    def fit(self, X_train, y_train):
        self.predictor.fit(X_train, y_train)

    def predict(self, X_test):
        X_test = X_test.copy()
        orderings = X_test.groupby('mutant_id').count()
        orderings['order'] = None
        orderings['order'] = orderings['order'].astype('object')
        self.prediction = self.predictor.predict(X_test)
        X_test['outcome_prediction'] = self.prediction
        for row in orderings.itertuples():
            predictions_for_mutant = X_test.loc[X_test['mutant_id'] == row.Index]
            # print(predictions_for_mutant.loc[predictions_for_mutant['outcome_prediction'] == False]['test_id'])
            fail_predictions = predictions_for_mutant.loc[predictions_for_mutant['outcome_prediction'] == False][
                'test_id']
            success_predictions = predictions_for_mutant.loc[predictions_for_mutant['outcome_prediction'] == True][
                'test_id']
            orderring = list(fail_predictions.append(success_predictions))
            # print(len(orderring))
            orderings.at[row.Index, 'order'] = orderring
            # print(list(fail_predictions.append(success_predictions)))
        return orderings


class OrdinalPredictionReorderer(Reorderer):
    def __init__(self, predictor):
        # This predictor should be in the
        self.predictor = predictor

    def name(self):
        return "OrdinalPredictionReorderer(" + type(self.predictor).__name__ + ")"

    def fit(self, X_train, y_train):
        self.predictor.fit(X_train, y_train)

    def predict(self, X_test):
        X_test = X_test.copy()
        orderings = X_test.groupby('mutant_id').count()
        orderings['order'] = None
        orderings['order'] = orderings['order'].astype('object')
        self.prediction = self.predictor.predict(X_test)
        X_test['outcome_prediction'] = self.prediction
        for row in orderings.itertuples():
            predictions_for_mutant = X_test.loc[X_test['mutant_id'] == row.Index]
            # print(predictions_for_mutant.loc[predictions_for_mutant['outcome_prediction'] == False]['test_id'])
            predictions_for_mutant.sort(['outcome_prediction'], ascending=False)
            orderring = list(predictions_for_mutant.Index)
            # print(len(orderring))
            orderings.at[row.Index, 'order'] = orderring
            # print(list(fail_predictions.append(success_predictions)))
        return orderings

