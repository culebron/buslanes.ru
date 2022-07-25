# run this to render the page (render.py) without running geometry calculations (main.py)
cd calc && python3 render.py html/index.template.html build/bus-lanes.geojson build/bus-lanes.csv build/index.html
