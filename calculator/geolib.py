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
	if fname.endswith('.geojson'):
		source_df = gpd.read_file(fname)
		if crs:
			source_df.crs = crs

	elif fname.endswith('.csv'):
		source_df = pd.read_csv(fname)
		if 'geometry' in source_df:
			source_df['geometry'] = source_df.geometry.apply(lambda g: shapely.wkt.loads(g))
			source_df = gpd.GeoDataFrame(source_df)
		if crs:
			source_df.crs = crs
	elif fname.endswith('.json'):
		source_df = pd.read_json(fname)
	return source_df


def write_file(df, fname):
	if isinstance(df, gpd.GeoDataFrame):
		if os.path.exists(fname):
			os.unlink(fname)
		if fname.endswith('.csv'):
			df = pd.DataFrame(df)
			df.to_csv(fname, index=False, encoding='utf-8')
		else:
			df.to_file(fname, driver='GeoJSON', encoding='utf-8')
	elif isinstance(df, pd.DataFrame):
		if fname.endswith('.csv'):
			df.to_csv(fname, encoding='utf-8')
		elif fname.endswith('.json'):
			df.to_json(fname)


class AnyDataFrame:
	pass


@decorator
def _autoargs(func, *args, **kwargs):
	func_signature = signature(func)
	newargs = list(a for a in args)

	writer = None
	for i, (value, param) in enumerate(zip(args, func_signature.parameters.values())):
		if (
			param.annotation == AnyDataFrame or
			(param.annotation == gpd.GeoDataFrame and (value.endswith('.csv') or value.endswith('.geojson'))) or
			param.annotation == pd.DataFrame
		):
			value = read_file(value)
		elif param.name == 'outfile':
			# сохранить outfile_name в отдельную переменную, потому что value меняется
			outfile_name = value
			def writer(df):
				write_file(df, outfile_name)
		elif param.annotation == int and value:
			value = int(value)
		elif param.annotation == float and value:
			value = float(value)

		newargs[i] = value

	retval = func(*newargs, **kwargs)
	if writer:
		writer(retval)


def autoargs(func):
	"""
	Добавляем функции в диспетчера только если это было сделано из корня модуля. Если модуль был импортирован из другого, то не надо диспетчеризовать, иначе это перезапишет сигнатуру скрипта, который был вызван.

	Например, closest_point.py импортирует buffer.py, чтобы вызвать buffer.main и передать в неё GeoDataFrame. Если диспетчеризовать buffer.main, изменится сигнатура closest_point.main, он будет ждать другие аргументы.

	"""
	import inspect
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	func2 = _autoargs(func)
	if mod.__name__ == '__main__':
		argh.dispatch_command(func2)
	else:
		# если команда не дефолтная, то надо сделать ручку для неё, чтобы вызывать из шелл-скриптов через setup.py
		def fn2():
			argh.dispatch_command(func2)

		mod._argh = fn2

	return func


def df_subset(df, names_string):
	if names_string:
		cnames = [cname.split(':') for cname in names_string.split(';')]
		subset = [c[0] for c in cnames]
		rename = dict(c for c in cnames if len(c) == 2)

		df = df[subset]
		df = df.rename(columns=rename)

	return df
