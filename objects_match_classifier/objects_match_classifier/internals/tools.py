import pandas as pd
from geopy.distance import vincenty
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split


def get_df(file_path, sep=',', is_marked_50_50=True):
    all_df = pd.read_csv(file_path, sep=sep, na_values='None')
    if is_marked_50_50:
        marked_true = all_df.loc[all_df['mark'] == 1]
        marked_false = all_df.loc[all_df['mark'] == 0].sample(len(marked_true))
        return pd.concat([marked_false, marked_true])
    return all_df


def get_X(obj_name, other_name, obj_lat, obj_lon, other_lat, other_lon, use_dumb_bag_of_words=True):
    return [
        dumb_bag_of_words_dist(obj_name, other_name) if use_dumb_bag_of_words else 0,
        vincenty(
            (obj_lat, obj_lon), (other_lat, other_lon), ellipsoid='WGS-84'
        ).meters
    ]


def get_sets(df, test_size=0.5, get_all_as_test=False, use_dumb_bag_of_words=True):
    X = [
        get_X(
            obj_name, other_name, obj_lat, obj_lon,
            other_lat, other_lon,
            use_dumb_bag_of_words=use_dumb_bag_of_words
        )
        for obj_name, other_name, obj_lat, obj_lon, other_lat, other_lon in zip(
            df.obj_name, df.other_name, df.obj_lat, df.obj_lon, df.other_lat, df.other_lon
        )
    ]
    if get_all_as_test:
        return None, X, None, None
    y = df['mark']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
    return X_train, X_test, y_train, y_test


def get_fit_classifier(Classifier, X_train, y_train):
    clf = Classifier()
    clf.fit(X_train, y_train)
    return clf


def dumb_bag_of_words_dist(input1, input2):
    bag1 = set(str(input1).lower().split())
    bag2 = set(str(input2).lower().split())
    intersecting = len(bag1.intersection(bag2))
    bag1.update(bag2)
    return float(intersecting) / len(bag1)


def load_classifier(file_path="./classifier.pkl"):
    return joblib.load(file_path)


def serialize_classifier(clf, file_path="./classifier.pkl"):
    joblib.dump(clf, file_path)
