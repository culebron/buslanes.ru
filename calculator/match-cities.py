import geolib
import geopandas as gpd
import pandas as pd

@geolib.autoargs
def main(muni_df: gpd.GeoDataFrame, pop_df: pd.DataFrame, outfile):
	muni_df = muni_df[~muni_df['name'].str.contains('район')]
	def _m(n):
		l = n.lower()
		if not l or len(l) == 0:
			return None

		for city_name in pop_df['name']:
			if city_name.lower() in l:
				return city_name
			if city_name.endswith('ь') and city_name[:-1].lower() in l:
				return city_name

	muni_df['short_name'] = muni_df['name'].apply(_m)

	def find_pop(n):
		matching = pop_df[pop_df['name'] == n]
		if not matching.empty:
			return matching['population'].values[0]

	muni_df['population'] = muni_df['short_name'].apply(find_pop)
	muni_df = muni_df[~muni_df['short_name'].isnull()]
	return muni_df
