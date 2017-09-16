data/lanes.kmz:
	wget https://www.google.com/maps/d/kml?mid=1PWvRWfdKEV4SVs5ONkDgRPLbRiQ -O $@

data/doc.kml: data/lanes.kmz
	unzip $^ -d data && touch $@

data/lanes.geojson: parsekml.py data/doc.kml
	python3 $^ $@

data/lanes2.geojson: convert_crs.py data/lanes.geojson
	python3 $^ 4326 $@ 3857

data/lanes3.geojson: length.py data/lanes2.geojson
	python3 $^ $@

data/muni3857.geojson: convert_crs.py src/muni.geojson
	python3 $^ 4326 $@ 3857

data/matched-cities.geojson: match-cities.py data/muni3857.geojson src/city-population.csv
	python3 $^ $@

data/merged.geojson: intersect.py data/matched-cities.geojson data/lanes3.geojson
	python3 $^ --how left $@

results/stats.geojson: stats.py data/merged.geojson
	python3 $^ $@

results/rating.csv: strip_geometry.py results/stats.geojson
	python3 $^ $@
