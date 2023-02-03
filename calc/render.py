import geopandas as gpd
import pandas as pd
import argh
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(template_path, displayed_lanes, stat_table, output_path):
	'''
	This function is generating html page using Jinja2.
	'''
	env = Environment(
		loader=FileSystemLoader('./html'),
		autoescape=select_autoescape(['html', 'xml'])
	)

	tpl = env.get_template(template_path.replace('html/', ''))
	print('rendering')

	# popullation to calculate small and big cities
	threshold = 400_000 
	big_cities = stat_table[stat_table['population'] > threshold].copy()
	small_cities = stat_table[stat_table['population'] <= threshold].copy()
	
	print('big:', len(big_cities))
	print('small:', len(small_cities))
	print('columns of cities:', list(big_cities))

	rendered = tpl.render(cities_json=displayed_lanes.to_json(), big_cities=big_cities.to_dict(orient='records'), small_cities=small_cities.to_dict(orient='records'))
	
	with open(output_path, 'w', encoding='utf-8') as f:
		f.write(rendered)

def render_cli(template_path, displayed_lanes, stat_table, output_path):
	lanes = gpd.read_file(displayed_lanes)
	stats = pd.read_csv(stat_table)
	return render(template_path, lanes, stats, output_path)

if __name__ == '__main__':
	argh.dispatch_command(render_cli)
	