import geopandas as gpd
import argh
import geolib

def main(file_in, crs_in, file_out, crs_out):
	if crs_in not in ('4326', '3857'):
		raise ValueError('crs-in must be 4326 or 3857')
	else:
		crs_in = geolib.crs_dict[int(crs_in)]

	if crs_out not in ('4326', '3857'):
		raise ValueError('crs-in must be 4326 or 3857')
	else:
		crs_out = geolib.crs_dict[int(crs_out)]

	df = gpd.read_file(file_in)
	df.crs = crs_in
	new_df = df.to_crs(crs_out)
	geolib.write_file(new_df, file_out)

argh.dispatch_command(main)
