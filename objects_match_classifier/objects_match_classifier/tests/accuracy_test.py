import os
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from ..internals.tools import get_df, get_sets, get_fit_classifier

marked_df = get_df(os.environ['MARKED_DATA'])

# Here we get 50/50 true and false marked objects
X_train, X_test, y_train, y_test = get_sets(marked_df, test_size=0.5, get_all_as_test=False)


clf = get_fit_classifier(DummyClassifier, X_train, y_train)
y_pred = clf.predict(X_test)
dummy_score = accuracy_score(y_test, y_pred)


clf = get_fit_classifier(DecisionTreeClassifier, X_train, y_train)
y_pred = clf.predict(X_test)
clf_score = accuracy_score(y_test, y_pred)

print("50/50 dataset")
print(f"Dummy accuracy: {dummy_score}, should be ~0.5")
print(f"DecisionTreeClassifier accuracy: {clf_score}, should be more than Dummy accuracy")


_, X_test, _, y_test = get_sets(marked_df, test_size=0.5, get_all_as_test=True)

y_pred = clf.predict(X_test)
clf_score = accuracy_score(y_test, y_pred)

print("Full dataset")
print(f"DecisionTreeClassifier accuracy: {clf_score}, should be more than Dummy accuracy")
