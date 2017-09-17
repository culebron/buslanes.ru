import geolib
import geopandas as gpd
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
	loader=FileSystemLoader('./html'),
	autoescape=select_autoescape(['html', 'xml'])
)

@geolib.autoargs
def main(html_template, df: gpd.GeoDataFrame, html_target):
	tpl = env.get_template('index.template.html')
	rendered = tpl.render(cities_json=df.to_json(), cities=df.to_dict(orient='records'))
	with open(html_target, 'w', encoding='utf-8') as f:
		f.write(rendered)

