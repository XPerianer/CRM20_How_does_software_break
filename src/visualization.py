import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import numpy as np

def plot_covariance_matrix(name, mutants_and_tests):
    pivot = mutants_and_tests.set_index('mutant_id').pivot(columns='test_id', values='outcome')
    pivot = pivot.astype('bool')
    fig, ax = plt.subplots(figsize=(18,18))
    ax.matshow(pivot.cov(), cmap=plt.get_cmap('binary'))
    #plt.axis('off')
    plt.title(name)
    plt.show()

def plot_failure_histogram(name, mutants_and_tests):
    failures = mutants_and_tests[mutants_and_tests['outcome'] == False]

    fails_per_test_id = failures.groupby(['test_id']).count()['outcome']
    #display(xy)

    plt.plot(fails_per_test_id)
    plt.xlabel('test_id')
    plt.ylabel('failures')
    plt.title(name)
    plt.show()
    
def plot_failures_vs_duration(name, mutants_and_tests):
    failures = mutants_and_tests[mutants_and_tests['outcome'] == False]
    fails_per_test_id = failures.groupby(['test_id']).count()['outcome']
    average_duration_per_test_id = failures.groupby(['test_id']).mean()['duration']
    
    plt.scatter(average_duration_per_test_id, fails_per_test_id)
    plt.title(name)
    plt.xlabel('Average Duration')
    plt.ylabel('Failures')
    plt.show()
    

def plot_hierarchical_failures(name, mutants_and_tests, arrows=True):
    failures = mutants_and_tests[mutants_and_tests['outcome'] == False]
    fails_per_test_id = failures.groupby(['test_id']).count()['outcome']
    
    y = fails_per_test_id
    x = failures.reset_index().groupby(['test_id']).mean()['mutant_id']
    
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    ax.set_xlim(mutants_and_tests['mutant_id'].min(), mutants_and_tests['mutant_id'].max())
    ax.set_ylim(0,y.max())
    ax.scatter(x=x, y=y)
    
    if(arrows):
        i = 0
        for test_failure in failures.reset_index().itertuples():
            x_start = test_failure.mutant_id
            y_start = 0
            test_id = test_failure.test_id
            x_end = x[test_id]
            y_end = y[test_id]
            ax.annotate("", xy=(x_end, y_end), xytext=(x_start, y_start), arrowprops={'arrowstyle': '-', 'color': '#A0A0A005'})
            
    plt.title(name)
    plt.show()
    
def plot_edit_distance_roc_curve(datasets):
    for name, mutants_and_tests in datasets.items():
        fpr, tpr, thresholds = metrics.roc_curve(mutants_and_tests['outcome'], mutants_and_tests['edit_distance'])
        auc = metrics.roc_auc_score(mutants_and_tests['outcome'], mutants_and_tests['edit_distance'])
        plt.plot(fpr,tpr,label=name + ", auc="+str(auc))
    plt.legend(loc=4)
    plt.title("ROC Curve for edit_distance feature")
    plt.show()


def plot_confusion_matrix(name, trained_predictor, X_test, y_test):
    """This plots a confusion matrix for an already trained predictor (it will just call predictor.predict(X_test), not predictor.fit(...))
       This can be used to check wether the given predictor performs well"""
    
    fig, ax = plt.subplots()
    fig.tight_layout()
    cm = confusion_matrix(y_test, trained_predictor.predict(X_test), normalize='all')
    cm_display = ConfusionMatrixDisplay(cm, display_labels=['False', 'True']).plot(ax=ax)
    plt.title(name)
    

def plot_feature_importances(name, forest, test_train_data):
    """Plot the impurity-based feature importances of a random forest"""
    
    
    X_train, y_train, X_test, y_test = test_train_data[name]
    plt.figure()
    plt.title(name + ": Feature importances")
    importances = forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    plt.barh(range(X_test.shape[1]), importances[indices],
            color="blue", xerr=std[indices], align="center")
    plt.yticks(range(X_test.shape[1]), X_test.columns)
    plt.show()