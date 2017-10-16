import geopandas as gpd
from math import radians, cos
from aqtash import autoargs, WGS

@autoargs
def do(df: gpd.GeoDataFrame, outfile, fieldname='length'):
	length = df['geometry'].length
	coslats = df.geometry.to_crs(WGS).apply(lambda p: p.centroid.y).apply(radians).apply(cos)
	df[fieldname] = length * coslats * df['lanes']
	return df
