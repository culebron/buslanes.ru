import geopandas as gpd
import geolib

@geolib.autoargs
def length(df: gpd.GeoDataFrame, outfile, fieldname='length'):
	length = df['geometry'].length

	df4326 = df.to_crs(geolib.CRS4326)
	coslats = df4326['geometry'].apply(geolib.coslat)

	df[fieldname] = length * coslats * df['lanes']
	return df
