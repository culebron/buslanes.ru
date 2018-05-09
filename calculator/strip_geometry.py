import aqtash
import geopandas as gpd

@aqtash.autoargs
def do(df: gpd.GeoDataFrame):
	cols = set(list(df)) - {'geometry'}
	return df[list(cols)]
