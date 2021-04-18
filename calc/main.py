from fastkml import kml
from render import render
from shapely.geometry import LineString
import argh
import geopandas as gpd
import os
import pandas as pd
import pyproj


OUTPUT_PATH = 'build/index.html'
STATS_PATH = 'build/bus-lanes.csv'
MUNICIPALITIES_PATH = 'src/muni.geojson'
POPULATION_PATH = 'src/city-population.csv'
TEMPLATE_PATH = 'html/index.template.html'


WGS = CRS4326 = 'epsg:4326'
SIB = pyproj.crs.ProjectedCRS(pyproj.crs.coordinate_operation.AlbersEqualAreaConversion(52, 64, 0, 105, 18500000, 0), name='Albers Siberia')


def download_kml(map_id, file_name):
	lanes_map_file = f'/tmp/{file_name}.kml'
	if not os.path.exists(lanes_map_file):
		print(f'downloading map http://www.google.com/maps/d/kml?mid={map_id}&forcekml=1')
		os.system(f'wget "http://www.google.com/maps/d/kml?mid={map_id}&forcekml=1" -O "{lanes_map_file}"')

	k = kml.KML()
	# open & encoding - для декодирования файлов при открытии, потому что в системе по умолчанию может стоять кодировка ascii
	with open(lanes_map_file, encoding='utf-8') as f:
		# а плагин сам ещё раскодирует utf-8, поэтому закодировать обратно
		k.from_string(f.read().encode('utf-8'))

	data = []
	for f in list(k.features())[0].features():
		lanes = None
		if f.name == 'односторонние сущ.' or f.name == 'Существующие. Односторонние':
			lanes = 1
		elif f.name == 'двусторонние сущ.' or f.name == 'Существующие':
			lanes = 2
		if lanes:
			for f2 in f.features():
				data.append({'lanes': lanes, 'geometry': f2.geometry})

	gdf = gpd.GeoDataFrame(data, crs=WGS)
	gdf['length'] = gdf['geometry'].to_crs(SIB).length  # в проекции альберса сибирь метры -- это реальные метры, в пределах бСССР, вне этого прямоугольника координат начинаются сильные нелинейные искажения.
	return gdf


def short_name(n, pop_df):
	if n is None:
		return

	l = n.lower().split()
	if not l or len(l) == 0:
		return

	for city_name in pop_df['name']:
		if city_name.lower() in l:  # делим на массив, чтобы не искать во всей строке, иначе омск/томск путаются
			return city_name
		if city_name.endswith('ь') and any(city_name[:-1].lower() in i for i in l):
			return city_name
		if ' ' in city_name and city_name.lower() in n.lower():  # если в имени из справочника населения есть пробел (набережные челны), тогда надо сравнить всю строку
			return city_name


def find_population(n, pop_df):
	matching = pop_df[pop_df['name'] == n]
	if not matching.empty:
		return matching['population'].values[0]


@argh.dispatch_command
def kml2gdf():
	print('reading russia file')
	# https://www.google.com/maps/d/u/0/viewer?hl=en&mid=1PWvRWfdKEV4SVs5ONkDgRPLbRiQ
	russia_gdf = download_kml('1PWvRWfdKEV4SVs5ONkDgRPLbRiQ', 'ВП в СНГ')
	population_df = pd.read_csv(POPULATION_PATH)

	municipalities = gpd.read_file(MUNICIPALITIES_PATH)
	municipalities['short_name'] = municipalities['name'].apply(short_name, args=(population_df,))
	municipalities['population'] = municipalities['short_name'].apply(find_population, args=(population_df,))

	russia = gpd.sjoin(russia_gdf, municipalities)

	print('reading moscow file')
	# https://www.google.com/maps/d/u/0/viewer?hl=en&mid=1GO7k2n2_8FgvzaaZCKtRhVCPr5s
	moscow = download_kml('1GO7k2n2_8FgvzaaZCKtRhVCPr5s', 'ВП в Москве')

	# выбираю ту строку из муниципалитетов, где написана москва и джойню
	print('calculating stats')
	moscow['_merge_'] = 1
	moscow_data = population_df[population_df['name'] == 'Москва'].copy()
	moscow_data['short_name'] = 'Москва'
	moscow_data['_merge_'] = 1
	moscow = moscow.merge(moscow_data, on='_merge_').drop('_merge_', axis=1)

	displayed_lanes = pd.concat([russia, moscow], sort=True)
	displayed_lanes['lanes_length'] = displayed_lanes['length'] * displayed_lanes['lanes']
	displayed_lanes = displayed_lanes[displayed_lanes['geometry'].apply(lambda g: len(g.coords) > 1)].copy()
	displayed_lanes['geometry'] = displayed_lanes['geometry'].apply(lambda g: LineString([xy[:2] for xy in list(g.coords)]))

	result_geojson = 'build/bus-lanes.geojson'
	displayed_lanes.to_file(result_geojson, driver='GeoJSON')

	stat_table = displayed_lanes.dissolve(by='short_name', aggfunc={'lanes_length': 'sum', 'population': 'first'}).reset_index()
	stat_table['lanes_per_1K'] = stat_table.lanes_length / stat_table.population * 1000
	stat_table.sort_values('lanes_per_1K', ascending=False, inplace=True)
	stat_table = stat_table.join(stat_table.bounds).drop('geometry', axis=1)

	stat_table.to_csv(STATS_PATH)

	render(TEMPLATE_PATH, displayed_lanes, stat_table, OUTPUT_PATH)
