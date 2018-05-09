#!/usr/bin/python3

from aqtash import autoargs, utils
from argh import CommandError
import geopandas as gpd


ALLOWED_OPERATIONS = {'sum', 'avg', 'min', 'first', 'last', 'count'}

@autoargs
def do(in_df: gpd.GeoDataFrame, groupby, aggregations):
	"""
	Aggregates columns of df2 that join df1.
	"""

	operations = {}  # 'index': 'first'}  # {'geometry': 'first'}
	for aggpair in utils.parse_column_names(aggregations):
		operation_name, field_name = aggpair
		if operation_name not in ALLOWED_OPERATIONS:
			raise CommandError('unknown operation {0}, allowed operations: {1}'.format(operation_name, ', '.join(ALLOWED_OPERATIONS)))

		operations[field_name] = operation_name

	groups = [g[0] for g in utils.parse_column_names(groupby)]
	result_df = in_df.dissolve(by=groups, aggfunc=operations)
	result_df.crs = in_df.crs
	return result_df
