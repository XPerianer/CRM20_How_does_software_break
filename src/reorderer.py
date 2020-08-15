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
    
    
# https://dl.acm.org/doi/pdf/10.1145/3395363.3397383
# Query the fastest tests first
# Because X_train does not have to contain the duration (since in the real world scenario, you also would not now in advance, we spoil this in the constructor)
class QTF(Reorderer):
    
    def __init__(self, test_ids_and_durations):
        self.test_ids_and_durations = test_ids_and_durations
    
    def name(self):
        return "QTF"
    def fit(self, X_train, y_train):
        # Calculate the average duration of the job
        sorted_test_ids = self.test_ids_and_durations.groupby(['test_id'])['duration'].mean().sort_values(ascending=True)
        # This is directly how we want our permutation to be:
        self.ordering = list(sorted_test_ids.index)
        
        
    def predict(self, X_test):
        orderings = X_test.groupby('mutant_id').count()
        orderings['order'] = None
        orderings['order'] = orderings['order'].astype('object')
        for row in orderings.itertuples():
            orderings.at[row.Index, 'order'] = self.ordering
        return orderings


# TODO: Sort the predicted failures after duration, such that short tests get executed first.
# TODO: It should probably also weight the predicted not failing tests after the average, to perform well if only few failures are predicted
class BinaryPredictionReorderer(Reorderer):
    """BinaryPredictionReorderer can convert a prediction of true/false for each test case into an order of tests.
    Therefore it will first predict, and then put the tests in front that were predicted failing."""
    
    
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
    """OrdinalPredictionReorderer can convert a prediction of failure probability in [0, 1] for each test case into an order of tests.
    Therefore it will first predict, and then put the tests in front that were predicted most likely to be failing.
    
    Similar to BinaryPredictionReorderer, but can make finer decisions if the model can give out probabilities of failure.
    """
    
    def __init__(self, predictor):
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
        
        index_of_false_class = list(self.predictor.classes_).index(False)
        self.prediction = self.predictor.predict_proba(X_test)[:, index_of_false_class]
        X_test['outcome_prediction'] = self.prediction
        for row in orderings.itertuples():
            predictions_for_mutant = X_test.loc[X_test['mutant_id'] == row.Index]
            sorted_test_ids = predictions_for_mutant.sort_values(by=['outcome_prediction'], ascending=False)['test_id']
            orderring = list(sorted_test_ids)
            orderings.at[row.Index, 'order'] = orderring
        return orderings

