import sys

import pandas as pd
from shapely import wkt
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier

from objects_match_classifier.internals.constants import B_COLS
from objects_match_classifier.internals.tools import (
    get_df, get_sets, get_fit_classifier,
    load_classifier, serialize_classifier,
)

def prepare_cols(num):
    rename_map = {'name': 'obj_name'}
    a_cols = ['lineno', 'type', 'id', 'name', 'geometry']
    b_cols = [i + f'_{num}' for i in B_COLS]
    for col in b_cols:
        rename_map[col] = col.replace(f'_{num}', '')
    return a_cols + b_cols, rename_map


def get_flat_predicted_dfs(full_df, clf):
    nearest_dfs = []
    for i in range(1, 6):
        cols, rename_map = prepare_cols(i)
        nearest_df = pd.DataFrame(data=full_df[cols]).rename(columns=rename_map)
        if 'geometry' in nearest_df.columns:
            nearest_df['geometry'] = nearest_df['geometry'].apply(wkt.loads)
            nearest_df['obj_lat'] = [i.x for i in nearest_df['geometry']]
            nearest_df['obj_lon'] = [i.y for i in nearest_df['geometry']]
            nearest_df = nearest_df.drop(columns=['geometry', ])
        nearest_df = nearest_df.drop(columns=['lineno',])
        _, X, _, _ = get_sets(nearest_df, get_all_as_test=True)
        y_pred = clf.predict(X)
        nearest_df['predicted'] = y_pred
        nearest_dfs.append(nearest_df)
    return nearest_dfs


def union_predicted(dfs, drop_osm_duplicates=True):
    """
    Unions dataframes containing only matched rows.
    drop_osm_duplicates is used to drop reoccuring OSM objects. Multiple OSM
    objects will be matched to one Booking object. One OSM object will be
    matched to one Booking.
    """
    resulting_dfs = []
    for df in dfs:
        resulting_dfs.append(df[df['predicted'] == 1])
    df_union_all = pd.concat(resulting_dfs)
    if drop_osm_duplicates:
        df_union_all = df_union_all[~df_union_all.duplicated(['type', 'id'])]
    return df_union_all


if __name__ == '__main__':
    if '-serialize' in sys.argv:
        dataset_filepath = sys.argv[2]
        marked_df = get_df(dataset_filepath)
        marked_df = marked_df.rename(columns={'obj_meta': 'obj_name', 'other_meta': 'other_name'})
        X_train, X_test, y_train, y_test = get_sets(marked_df)
        clf = get_fit_classifier(DecisionTreeClassifier, X_train, y_train)
        serialize_classifier(clf)
        print(f"Serialized")
        y_pred = clf.predict(X_test)
        clf_score = accuracy_score(y_test, y_pred)
        print(f"DecisionTreeClassifier accuracy: {clf_score}")
    else:
        clf = load_classifier("./classifier.pkl")
        geomatched_filepath = sys.argv[1]
        full_df = get_df(geomatched_filepath, sep='\t', is_marked_50_50=False)
        print('Preprocess')
        dfs = get_flat_predicted_dfs(full_df, clf)
        print('Unioning results')
        result = union_predicted(dfs, drop_osm_duplicates=True)
        result = result.drop(columns=['predicted'])
        print('Writing to file')
        result.to_csv('predictions.csv', mode='a', header=True)
