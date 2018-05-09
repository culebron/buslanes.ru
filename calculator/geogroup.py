#!/usr/bin/python3

from aqtash import autoargs, subset
import geopandas as gpd
from argh import CommandError



ALLOWED_OPERATIONS = {'sum', 'avg', 'min', 'first', 'last', 'count'}

@autoargs
def group(df1: gpd.GeoDataFrame, df2: gpd.GeoDataFrame, aggregations, subset_names=None):
	"""
	Aggregates columns of df2 that join df1.
	"""

	operations = {}  # 'index': 'first'}  # {'geometry': 'first'}
	for aggpair in aggregations.split(';'):
		operation_name, field_name = aggpair.split(':')
		if operation_name not in ALLOWED_OPERATIONS:
			raise CommandError('unknown operation {0}, allowed operations: {1}'.format(operation_name, ', '.join(ALLOWED_OPERATIONS)))

		operations[field_name] = operation_name

	df1 = df1[df1.geometry.notnull()]
	df2 = df2[df2.geometry.notnull()]

	matches = gpd.sjoin(df1, df2, how='inner', op='intersects')

	gr = matches.groupby(matches.index).agg(operations)
	result_df = df1.join(gr)
	return subset.do(result_df, subset_names)
