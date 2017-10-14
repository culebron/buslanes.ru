import aqtash
import geopandas as gpd

@aqtash.autoargs
def do(df: gpd.GeoDataFrame, outfile):
	cols = set(list(df)) - {'geometry'}
	return df[list(cols)]
