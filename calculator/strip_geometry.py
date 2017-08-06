import geolib
import geopandas as gpd

@geolib.autoargs
def main(df: gpd.GeoDataFrame, outfile):
	cols = set(list(df)) - {'geometry'}
	return df[list(cols)]
