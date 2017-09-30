#!/usr/bin/python3

from aqtash import autoargs
from argh import CommandError
from collections import defaultdict
from shapely.geometry import Point
import geopandas as gpd
import numpy as np
import pandas as pd


ALLOWED_OPERATIONS = {'sum', 'avg', 'min', 'first', 'last', 'count'}

@autoargs
def do(in_df: gpd.GeoDataFrame, groupby, aggregations, outfile):
	"""
	Aggregates columns of df2 that join df1.
	"""

	operations = {}  # 'index': 'first'}  # {'geometry': 'first'}
	for aggpair in aggregations.split(';'):
		operation_name, field_name = aggpair.split(':')
		if operation_name not in ALLOWED_OPERATIONS:
			raise CommandError('unknown operation {0}, allowed operations: {1}'.format(operation_name, ', '.join(ALLOWED_OPERATIONS)))

		operations[field_name] = operation_name

	if groupby not in in_df:
		raise CommandError('column "{0}" not in dataframe. Available columns: "{1}"'.format(groupby, '", "'.join(list(in_df))))

	result_df = in_df.dissolve(by=groupby, aggfunc=operations)
	result_df.crs = in_df.crs
	return result_df
