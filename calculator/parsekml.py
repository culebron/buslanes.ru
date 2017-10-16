
from aqtash import autoargs, WGS
import geopandas as gpd
from fastkml import kml

@autoargs
def do(kmlfile, outfile):
	k = kml.KML()
	# open & encoding - для декодирования файлов при открытии, потому что в системе по умолчанию может стоять кодировка ascii
	with open(kmlfile, encoding='utf-8') as f:
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

	return gpd.GeoDataFrame(data, crs=WGS)

