# https://gis.stackexchange.com/questions/222315/geopandas-find-nearest-point-in-other-dataframe

import itertools
from operator import itemgetter

import numpy as np
import pandas as pd
import osmium as osm

from scipy.spatial import cKDTree

from shapely.geometry import Point, LineString


def ckdnearest(gdfA, gdfB, gdfB_cols=['csv_id', ], k_nearest=5, use_copy=True):
    """
       A function to attach k nearest nodes from dataset B to dataset A.
       You could set use_copy to False, if you wish to join nearest nodes inplace.

       Works much faster then "nearest" of shapely.

       gdfA, gdfB: pd or gpd DataFrame
       returns: pd or gpd DataFrame
    """
    A = np.concatenate([np.array(geom.coords) for geom in gdfA.geometry.to_list()])
    B = [np.array(geom.coords) for geom in gdfB.geometry.to_list()]
    B_ix = tuple(itertools.chain.from_iterable(
        [itertools.repeat(i, x) for i, x in enumerate(list(map(len, B)))]))
    B = np.concatenate(B)
    ckd_tree = cKDTree(B)

    if use_copy:
        gdf = gdfA.copy()
    else:
        gdf = gdfA

    for near in range(1, k_nearest + 1):  # attach nearest cols to table
        dist, idx = ckd_tree.query(A, k=[near])
        idx = itemgetter(*itertools.chain.from_iterable(idx))(B_ix)
        gdf = pd.concat(
            [gdf, gdfB.loc[idx, gdfB_cols].reset_index(drop=True),
             pd.Series(itertools.chain.from_iterable(dist), name='dist_' + str(near))],
            axis=1
        )
        gdf.rename(
            columns={col: col + '_' + str(near) for col in gdfB_cols},
            inplace=True
        )
    return gdf


class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.node_location = {}
        self.way_ids = set()
        self.node_ids = set()

    def get_location(self, elem, elem_type):
        location = 0, 0
        if elem_type == "node":
            location = getattr(elem, 'location', None)
            if location:
                location = Point(location.lat, location.lon)
            self.node_location[elem.id] = location
        elif elem_type == "way":
            location = LineString([
                self.node_location.get(n.ref) for n in
                getattr(elem, 'nodes', []) if self.node_location.get(n.ref)
            ]).centroid
        return location

    def not_dependency(self, elem):
        return True

    def get_row(self, elem, elem_type):
        return []

    def tag_inventory(self, elem, elem_type):
        location = self.get_location(elem, elem_type)

        # removing dependencies from data
        if self.not_dependency(elem):
            add_to_data = True
            if elem_type == "relation":
                # relation - на потом, их 9033 - 1%
                add_to_data = False
            if add_to_data:
                self.osm_data.append(
                    self.get_row(elem, elem_type) + [location, ]
                )

    def node(self, n):
        if self.not_dependency(n):
            self.node_ids.add(n.id)
        self.tag_inventory(n, "node")

    def way(self, w):
        if self.not_dependency(w):
            self.way_ids.add(w.id)
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")
