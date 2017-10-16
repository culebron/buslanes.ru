from aqtash import autoargs, utils, CRS_DICT
import geopandas as gpd

@autoargs
def do(df: gpd.GeoDataFrame, outfile, fieldname='area'):
	length = df['geometry'].area()
	df4326 = df.to_crs(CRS_DICT[4326])
	coslats = df4326['geometry'].apply(utils.coslat)
	df[fieldname] = length * coslats * coslats
	return df
