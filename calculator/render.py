from aqtash import autoargs
import geopandas as gpd
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
	loader=FileSystemLoader('./html'),
	autoescape=select_autoescape(['html', 'xml'])
)

@autoargs
def do(html_template, df: gpd.GeoDataFrame, stats_df: pd.DataFrame, html_target):
	tpl = env.get_template(html_template.replace('html/', ''))

	rendered = tpl.render(cities_json=df.to_json(), cities=stats_df.to_dict(orient='records'))
	with open(html_target, 'w', encoding='utf-8') as f:
		f.write(rendered)

