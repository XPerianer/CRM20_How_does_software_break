import pandas as pd
import editdistance

from sklearn.preprocessing import OrdinalEncoder


def cleanse_data(mutants_and_tests):
    # Encode None as false in the context
    for column in ["contains_branch_mutant", "contains_loop_mutant", "contains_math_operands_mutant", "contains_equality_comparison_mutant",
                   "contains_branch_execution", "contains_loop_execution", "contains_math_operands_execution", "contains_equality_comparison_execution",
                    "teardown_outcome", "setup_outcome", "call_outcome", "outcome"]:
        mutants_and_tests.loc[mutants_and_tests[column].isnull(), column] = False

    #Encode NaN as 0 in the duration stuff
    for column in ["teardown_duration", "setup_duration", "call_duration"]:
        mutants_and_tests.loc[pd.isnull(mutants_and_tests[column]), column] = 0

        
# Sometimes, test_ids only occur very rarely and make problems in the reordering. They can be removed here from the dataset
def remove_test_ids(test_ids_to_remove, mutants_and_tests): # e.g.: [82, 83]
    for test_id in test_ids_to_remove:
        mutants_and_tests = mutants_and_tests.loc[mutants_and_tests['test_id'] != test_id]
    mutants_and_tests = mutants_and_tests.copy()
    
def edit_distance_feature(row_one: [], row_two: []) -> []:
    return list(map(editdistance.eval, row_one, row_two))
    
def add_edit_distance_feature(mutants_and_tests):
    # Fix object and fill null values
    mutants_and_tests["name"] = mutants_and_tests["name"].astype('string')
    mutants_and_tests["modified_method"] = mutants_and_tests["modified_method"].astype('string')

    mutants_and_tests["name"].loc[pd.isnull(mutants_and_tests["name"])] = ""
    mutants_and_tests["modified_method"].loc[pd.isnull(mutants_and_tests["modified_method"])] = ""

    mutants_and_tests['edit_distance'] = edit_distance_feature(
        mutants_and_tests['modified_method'],
        mutants_and_tests['name']
    )
    mutants_and_tests['edit_distance'].value_counts()

def encode_columns(X, columns):
    X = X.copy()
    enc = OrdinalEncoder()
    X_enc = enc.fit_transform(X[columns])
    i = 0
    for column_name in columns:
        X[column_name] = X_enc[:,i]
        i += 1
    return X


def filter_NaN_values(name, dataset):
    previous_length = len(dataset)
    dataset = dataset.loc[dataset.isnull().any(axis=1) == False]
    print(name + ": Kicked out " + str(previous_length - len(dataset)) + " values from " + str(previous_length) + " total values. (" + str((1 - len(dataset) / previous_length) * 100) + "%) (NaN value filter)")
    return dataset

# Split test and train # TODO: document why it is good that we have a hard split here
def train_test_split(mutants_and_tests, test_size=0.3):
    split_mutant = mutants_and_tests['mutant_id'].max() * (1 - test_size)
    
    train = mutants_and_tests.loc[mutants_and_tests['mutant_id'] <= split_mutant]
    test = mutants_and_tests.loc[mutants_and_tests['mutant_id'] > split_mutant]

    X_train = train.drop(['outcome'], axis=1)
    y_train = train['outcome']
    
    X_test = test.drop(['outcome'], axis=1)
    y_test = test['outcome']
    
    return (X_train, y_train, X_test, y_test)