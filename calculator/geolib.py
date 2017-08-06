# coding: utf-8

from inspect import signature
from decorator import decorator
from math import radians, cos
import argh
import geopandas as gpd
import os
import pandas as pd


# для GeoDataFrame
CRS3857 = {'init': 'epsg:3857'}
CRS4326 = {'init': 'epsg:4326'}
crs_dict = {4326: CRS4326, 3857: CRS3857}


def coslat(geom):
	try:
		return cos(radians(geom.centroid.y))
	except IndexError as e:
		print('error in coslat', geom.wkt)
		raise e


def read_file(fname, crs=None):
	source_df = gpd.read_file(fname)
	if crs:
		source_df.crs = crs
	return source_df


def write_file(df, fname):
	if isinstance(df, gpd.GeoDataFrame):
		if os.path.exists(fname):
			os.unlink(fname)
		df.to_file(fname, driver='GeoJSON', encoding='utf-8')
	elif isinstance(df, pd.DataFrame):
		if fname.endswith('.csv'):
			df.to_csv(fname)
		elif fname.endswith('.json'):
			df.to_json(fname)


@decorator
def _autoargs(func, *args, **kwargs):
	func_signature = signature(func)
	newargs = []
	writer = None
	for value, param in zip(args, func_signature.parameters.values()):
		if param.annotation == gpd.GeoDataFrame:
			value = read_file(value, CRS3857)
		elif param.annotation == pd.DataFrame and value.endswith('.json'):
			value = pd.read_json(value)
		elif param.annotation == pd.DataFrame:
			value = pd.read_csv(value)
		elif param.name == 'outfile':
			# сохранить outfile_name в отдельную переменную, потому что value меняется
			outfile_name = value
			def writer(df):
				write_file(df, outfile_name)

		newargs.append(value)

	retval = func(*newargs, **kwargs)
	if writer:
		writer(retval)


def autoargs(func):
	func = _autoargs(func)
	argh.dispatch_command(func)
	return func
