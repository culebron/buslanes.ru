import geopandas as gpd
import aqtash

@aqtash.autoargs
def do(infile, crs_in, outfile, crs_out):
	if crs_in not in ('4326', '3857'):
		raise ValueError('crs-in must be 4326 or 3857')
	else:
		crs_in = aqtash.CRS_DICT[int(crs_in)]

	if crs_out not in ('4326', '3857'):
		raise ValueError('crs-in must be 4326 or 3857')
	else:
		crs_out = aqtash.CRS_DICT[int(crs_out)]

	df = gpd.read_file(infile)
	df.crs = crs_in
	new_df = df.to_crs(crs_out)
	return new_df
