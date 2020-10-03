import argh
from jinja2 import Environment, FileSystemLoader, select_autoescape


def render(template_path, displayed_lanes, stat_table, output_path):
	env = Environment(
		loader=FileSystemLoader('./html'),
		autoescape=select_autoescape(['html', 'xml'])
	)

	tpl = env.get_template(template_path.replace('html/', ''))
	print('rendering')
	rendered = tpl.render(cities_json=displayed_lanes.to_json(), cities=stat_table.to_dict(orient='records'))
	with open(output_path, 'w', encoding='utf-8') as f:
		f.write(rendered)

if __name__ == '__main__':
	argh.dispatch_command(render)
