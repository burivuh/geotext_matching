import geopandas as gpd
import pandas as pd


from shapely.geometry import Point

from .internals.constants import (
    TOURISM_HOTELS, BUILDING_HOTELS, AMENITY_HOTELS,
    LEISURE_HOTELS, B_COLS
)
from .internals.base import ckdnearest, OSMHandler


class HotelsOSMHandler(OSMHandler):
    def not_dependency(self, elem):
        return (
            elem.tags.get('tourism') in TOURISM_HOTELS or
            elem.tags.get('building') in BUILDING_HOTELS or
            elem.tags.get('amenity') in AMENITY_HOTELS or
            elem.tags.get('leisure') in LEISURE_HOTELS
        )

    def get_row(self, elem, elem_type):
        return [
            elem_type,
            elem.id,
            len(elem.tags),
            elem.tags.get('name'),
        ]


osmhandler = HotelsOSMHandler()
# scan the input file and fills the handler list accordingly
osmhandler.apply_file("../hotels_wo_unwanted.osm")

# transform the list into a pandas DataFrame
data_colnames = ['type', 'id', 'ntags', 'name', 'geometry', ]

crs = {'init': 'epsg:4326'}  # OSM
gdf_osm = gpd.GeoDataFrame(osmhandler.osm_data, crs=crs, columns=data_colnames)


df = pd.read_csv('../hotels_booking_latest.csv', sep='\t', header=None,
                 names=[
                     'other_id', 'other_lat', 'other_lon',
                     'other_name', 'addr', 'n',
                     'm', 'i', 'rating',
                     'web', 'j', 'trans'],
                 na_values='None')
geometry = [Point(xy) for xy in zip(df.other_lat, df.other_lon)]


crs2 = {'init': 'epsg:3857'}  # google
gdf_booking = gpd.GeoDataFrame(df, crs=crs2, geometry=geometry)

c = ckdnearest(gdf_osm, gdf_booking, gdfB_cols=B_COLS)
c.sort_values(by=['type', 'id'])
c.to_csv('hotels_geomatched.csv', sep='\t', index_label='lineno')
