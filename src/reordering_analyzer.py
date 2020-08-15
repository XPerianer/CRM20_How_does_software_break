import pandas as pd
from src.reordering_evaluation import ReorderingEvaluation


# TODO: This should gracefully handle test ids not in the trainset. The Predictor can then not know that such a test case exists, and won't have it in the order.
class ReorderingAnalyzer:
    """This can be used to compare the reordering performance of different given orderers.
    Since steps can take very long, after each step outcomes are safed in the member variables `predictions`, `orderers`, and `raw_data`.
    """
    
    def __init__(self, orderers):
        self.orderers = orderers
        self.raw_data = {}

    def fit(self, X_train, y_train):
        for orderer in self.orderers:
            orderer.fit(X_train.copy(), y_train.copy())

    def predict(self, X_test):
        self.predictions = []
        self.X_test = X_test
        for orderer in self.orderers:
            self.predictions.append(orderer.predict(X_test.copy()))

    def evaluate(self, mutants_and_tests):
        m = mutants_and_tests.copy()
        test_count = m.groupby('test_id').count().shape[0]
        data = {}
        for i, ordering in enumerate(self.predictions):
            print('Starting evaluation ', end='')
            for row in ordering.itertuples():
                if row.Index % 50 == 0:
                    print('.', end='')
                mutant_executions = m.loc[m['mutant_id'] == row.Index]
                # Only execute the metrics if we have at least one failure
                if mutant_executions['outcome'].values.all() == False:
                    order = ordering.loc[row.Index].order
                    if len(order) != test_count:
                        print('Not a full ordering was specified, skipping...')
                        continue
                    r = ReorderingEvaluation(order, mutant_executions)
                    data.update({(self.orderers[i].name(), row.Index):
                                     ReorderingEvaluation(order, mutant_executions).to_dict()

                                 })

            print(' finished.')
        self.raw_data = data

        return pd.DataFrame(data)
    
    def boxplot(self):
        evaluation_data = pd.DataFrame(self.raw_data)
        orderers_count = len(self.orderers)
        x_size = orderers_count * 5
        y_size = 10
        evaluation_data.transpose().groupby(level=0).boxplot(column = ['APFD', 'APFDc'], figsize=(x_size, y_size), layout=(1,orderers_count))
        evaluation_data.transpose().groupby(level=0).boxplot(column = ['first_failing_duration', 'last_failing_duration'], figsize=(x_size, y_size), layout=(1,orderers_count))
        
