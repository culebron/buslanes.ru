from aqtash import autoargs, memoize, sh, WatchedFile, GOOGLE, WGS, intersect, write_file, stack, read_file
import convert_crs
import dissolve
import length
import match_cities
import pandas as pd
import parsekml
import stats
import strip_geometry
import os

@memoize
def group_data(map_id, borders_file):
	print('executing group_data')
	lanes_map_file = '/tmp/{}.kml'.format(map_id)
	if not os.path.exists(lanes_map_file):
		sh('wget "https://www.google.com/maps/d/kml?mid={}&forcekml=1" -O '.format(map_id), lanes_map_file)
	lanes = parsekml.do(lanes_map_file, None).to_crs(GOOGLE)
	lengths = length.do(lanes, None, 'lanes_length').to_crs(WGS)

	matched_cities = match_cities.do(borders_file, read_file('src/city-population.csv'), None)
	merged_lanes = intersect.do(lengths, matched_cities, None)
	return dissolve.do(merged_lanes, 'index_right', 'first:population;first:short_name;sum:lanes_length', None)

@autoargs
def render_page(outfile='build/index.html'):
	print('executing main')
	russia = group_data('1PWvRWfdKEV4SVs5ONkDgRPLbRiQ', read_file('src/muni.geojson'))
	moscow = group_data('1GO7k2n2_8FgvzaaZCKtRhVCPr5s', read_file('src/mow.geojson'))
	all_data = pd.concat([russia, moscow])


	result_geojson = 'build/bus-lanes.geojson'
	result_csv = 'build/bus-lanes.csv'

	lanes_result = stats.do(all_data, None)
	write_file(lanes_result, result_geojson)

	lanes_result = strip_geometry.do(lanes_result, None)
	write_file(lanes_result, result_csv)

	sh('python3 render.py ', WatchedFile('html/index.template.html'), ' ', result_geojson, ' ', outfile)
