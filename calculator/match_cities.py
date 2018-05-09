# coding: utf-8

import aqtash
import geopandas as gpd
import pandas as pd

@aqtash.autoargs
def do(muni_df: gpd.GeoDataFrame, pop_df: pd.DataFrame):
	muni_df = muni_df[~muni_df['name'].str.contains('район').fillna(False)]
	def _m(n):
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
			if ' ' in city_name and city_name.lower() in n.lower(): # если в имени из справочника населения есть пробел (набережные челны), тогда надо сравнить всю строку
				return city_name


	muni_df['short_name'] = muni_df['name'].apply(_m)

	def find_pop(n):
		matching = pop_df[pop_df['name'] == n]
		if not matching.empty:
			return matching['population'].values[0]

	muni_df['population'] = muni_df['short_name'].apply(find_pop)
	return muni_df[~muni_df['short_name'].isnull()]
