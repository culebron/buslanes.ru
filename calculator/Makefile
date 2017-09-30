data/russia.kml:
	wget "https://www.google.com/maps/d/kml?mid=1PWvRWfdKEV4SVs5ONkDgRPLbRiQ&forcekml=1" -O $@

data/moscow.kml:
	wget "https://www.google.com/maps/d/kml?mid=1GO7k2n2_8FgvzaaZCKtRhVCPr5s&forcekml=1" -O $@

data/lanes-rus.geojson: parsekml.py data/russia.kml
	python3 $^ $@

data/lanes-rus3857.geojson: convert_crs.py data/lanes.geojson
	python3 $^ 4326 $@ 3857

data/lanes-rus-len.geojson: length.py data/lanes-rus3857.geojson
	python3 $^ $@ -f 'lanes_length'

data/lanes-rus-len4326.geojson: convert_crs.py data/lanes-rus-len.geojson


data/lanes-rus.geojson: parsekml.py data/russia.kml
	python3 $^ $@

data/lanes-rus3857.geojson: convert_crs.py data/lanes.geojson
	python3 $^ 4326 $@ 3857

data/lanes-rus-len.geojson: length.py data/lanes-rus3857.geojson
	python3 $^ $@ -f 'lanes_length'

data/lanes-rus-len4326.geojson: convert_crs.py data/lanes-rus-len.geojson


data/matched-cities.geojson: match-cities.py src/muni.geojson src/city-population.csv
	python3 $^ $@

data/merged-lanes-rus.geojson: intersect.py data/lanes-rus-len4326.geojson data/matched-cities.geojson
	python3 $^ $@

data/grouped-lanes.geojson: dissolve.py data/merged-lanes.geojson
	python3 $^ 'index_right' 'first:population;first:short_name;sum:lanes_length' $@

build/bus-lanes.geojson: stats.py data/grouped-lanes.geojson
	python3 $^ $@

build/bus-lanes.csv: strip_geometry.py build/bus-lanes.geojson
	python3 $^ $@

build/index.html: render.py html/index.template.html build/bus-lanes.geojson html/info.html html/heading.html build/bus-lanes.geojson build/bus-lanes.csv
	python3 render.py html/index.template.html build/bus-lanes.geojson $@

all: build/index.html

