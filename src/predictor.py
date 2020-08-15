from abc import ABC, abstractmethod


class Predictor(ABC):
    """Abstract Base Class for Predictors"""

    @abstractmethod
    def name(self):
        """Output a concise name that makes it easy to identify"""
        raise NotImplementedError

    @abstractmethod
    def fit(self, X_train, y_train):
        raise NotImplementedError

    @abstractmethod
    def predict(self, X_test):
        raise NotImplementedError
        

class NearestMutantPredictor(Predictor):
    """Chooses the same test outcomes as the mutant with the smallest absolute difference in mutant_id"""
    
    def name(self):
        return "NearestMutant"
    
    def fit(self, X_train, y_train):
        self.X = X_train.copy()
        self.X['outcome'] = y_train
        
    def predict(self, X_test):
        predictions = []
        for index, row in X_test.iterrows():
            # Select only rows from X_train with the same test_id
            correct_tests = self.X.loc[self.X['test_id'] == row['test_id']]
            mutant_id = row['mutant_id']
            nearest_mutant_id_index = abs(correct_tests['mutant_id'] - mutant_id).idxmin()
            predictions.append(self.X['outcome'][nearest_mutant_id_index])
        return predictions
