import pandas as pd

# Load datasets
def load_dataset(filename, sparsify=False):
    mutants_and_tests = pd.read_pickle(filename)
    mutants_and_tests.reset_index()
    mutants_and_tests["outcome"] = mutants_and_tests["outcome"].astype('bool')
    mutants_and_tests["outcome"]
    #display(mutants_and_tests)
    if sparsify:
        keep_fraction = 0.05 # Keep 5% of the dataset (roughly, since we delete tests and mutants smaller than that)
        max_mutant_id = mutants_and_tests['mutant_id'].max()
        max_test_id = max(mutants_and_tests['test_id'].max(), 10) # At least use 10 tests
        return mutants_and_tests.loc[mutants_and_tests['test_id'] < max_test_id * keep_fraction].loc[mutants_and_tests['mutant_id'] < max_mutant_id * keep_fraction]
    return mutants_and_tests

def load_datasets(name_and_filename, sparsify=False):
    datasets = {}
    for name, filename in name_and_filename.items():
        datasets[name] = load_dataset(filename, sparsify)
    return datasets