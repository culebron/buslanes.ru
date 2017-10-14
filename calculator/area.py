import geopandas as gpd
import geolib

@autoargs
def do(df: gpd.GeoDataFrame, outfile, fieldname='area'):
	length = df['geometry'].area()
	df4326 = df.to_crs(geolib.CRS4326)
	coslats = df4326['geometry'].apply(geolib.coslat)
	df[fieldname] = length * coslats * coslats
	return df
