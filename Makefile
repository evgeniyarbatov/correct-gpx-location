RUN_OSM_FILE = gpx/30-08-2024/run.osm
RUN_NODES_FILE = gpx/30-08-2024/nodes.csv

VENV_PATH = ~/.venv/correct-gpx

all: venv install jupyter

venv:
	@python3 -m venv $(VENV_PATH)

install: venv
	@source $(VENV_PATH)/bin/activate && \
	pip install --disable-pip-version-check -q -r requirements.txt

jupyter:
	@source $(VENV_PATH)/bin/activate && \
	python3 -m ipykernel install \
	--user --name=myenv \
	--display-name "Python (correct-gpx)"

nodes:
	source $(VENV_PATH)/bin/activate && \
	python3 scripts/get-osm-nodes.py $(RUN_OSM_FILE) $(RUN_NODES_FILE)