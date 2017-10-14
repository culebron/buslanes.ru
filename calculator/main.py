from aqtash import autoargs, memoize, sh, WatchedFile, GOOGLE, WGS, intersect, write_file, read_file
import dissolve
import length
import match_cities
import os
import pandas as pd
import parsekml
import stats
import strip_geometry

@memoize
def group_data(map_id, borders_file):
	print('executing group_data')
	lanes_map_file = '/tmp/{}.kml'.format(map_id)
	if not os.path.exists(lanes_map_file):
		sh('wget "https://www.google.com/maps/d/kml?mid={}&forcekml=1" -O '.format(map_id), lanes_map_file)
	lanes = parsekml.do(lanes_map_file, None).to_crs(GOOGLE)
	lengths = length.do(lanes, None, 'lanes_length').to_crs(WGS)

	matched_cities = match_cities.do(borders_file, read_file('src/city-population.csv'), None)
	return intersect.do(lengths, matched_cities, None)

@autoargs
def render_page(outfile='build/index.html'):
	print('executing main')
	russia = group_data('1PWvRWfdKEV4SVs5ONkDgRPLbRiQ', read_file('src/muni.geojson'))
	moscow = group_data('1GO7k2n2_8FgvzaaZCKtRhVCPr5s', read_file('src/mow.geojson'))
	displayed_lanes = pd.concat([russia, moscow])


	result_geojson = 'build/bus-lanes.geojson'
	write_file(displayed_lanes, result_geojson)

	stat_table = dissolve.do(displayed_lanes, 'short_name', 'sum:lanes_length;first:population', None)
	stat_table = strip_geometry.do(stats.do(stat_table, None), None)
	result_csv = 'build/bus-lanes.csv'
	write_file(stat_table, result_csv)

	sh('python3.6 render.py ', WatchedFile('html/index.template.html'), ' ', result_geojson, ' ', result_csv, ' ', outfile)
