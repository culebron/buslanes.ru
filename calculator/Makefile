data/lanes.kmz:
	wget https://www.google.com/maps/d/kml?mid=1PWvRWfdKEV4SVs5ONkDgRPLbRiQ -O $@

data/doc.kml: data/lanes.kmz
	unzip -o $^ -d data && touch $@

data/lanes.geojson: parsekml.py data/doc.kml
	python3 $^ $@

data/lanes2.geojson: convert_crs.py data/lanes.geojson
	python3 $^ 4326 $@ 3857

data/lanes3.geojson: length.py data/lanes2.geojson
	python3 $^ $@ -f 'lanes_length'

data/muni3857.geojson: convert_crs.py src/muni.geojson
	python3 $^ 4326 $@ 3857

data/matched-cities.geojson: match-cities.py data/muni3857.geojson src/city-population.csv
	python3 $^ $@

data/merged-lanes.geojson: intersect.py data/lanes3.geojson data/matched-cities.geojson
	python3 $^ $@

data/grouped-lanes.geojson: dissolve.py data/merged-lanes.geojson
	python3 $^ 'index_right' 'first:population;first:short_name;sum:lanes_length' $@

results/stats.geojson: stats.py data/grouped-lanes.geojson
	python3 $^ $@

html/index.html: render.py html/index.template.html results/stats.geojson
	python3 $^ $@


all: results/stats.geojson html/index.html

