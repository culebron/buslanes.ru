import geolib
import geopandas as gpd

@geolib.autoargs
def main(df: gpd.GeoDataFrame, outfile):
	df['lanes_per_1K'] = df.lanes_length / df.population * 1000
	df.sort_values('lanes_per_1K', ascending=False, inplace=True)
	df = gpd.GeoDataFrame(df, crs=df.crs).to_crs(geolib.crs_dict[4326])
	return df.join(df.bounds)
