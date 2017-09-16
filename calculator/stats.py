import geolib
import geopandas as gpd

@geolib.autoargs
def main(df: gpd.GeoDataFrame, outfile):
	gr = df.groupby([df['short_name']])
	popgeom = gr.first()[['population', 'geometry']]
	lanes = gr.sum()['length']


	popgeom['lanes'] = lanes

	f = popgeom.reset_index()
	f.fillna(0)
	f = f[f.lanes > 0]
	f['lanes_per_1K'] = f.lanes / f.population * 1000
	f.sort_values('lanes_per_1K', ascending=False, inplace=True)
	f = gpd.GeoDataFrame(f, crs=df.crs).to_crs(geolib.crs_dict[4326])
	return f.join(f.bounds)
