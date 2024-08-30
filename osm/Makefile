OSM_PBF_PATH = ~/osm/vietnam-latest.osm.pbf

TIMESCITY_OSM_PBF = timescity.osm.pbf
TIMESCITY_OSM = timescity.osm

TIMESCITY_BOUNDS = 105.86546820281349,20.99039866680133,105.87028835772978,20.99885847356933

PEDESTRIAN_OSM = timescity-pedestrian.osm
PEDESTRIAN_OSM_PBF = timescity-pedestrian.osm.pbf

all: extract filter

extract:
	@osmconvert $(OSM_PBF_PATH) -b=$(TIMESCITY_BOUNDS) -o=$(TIMESCITY_OSM_PBF)
	@osmium cat --overwrite $(TIMESCITY_OSM_PBF) -o $(TIMESCITY_OSM)

filter:
	@osmfilter $(TIMESCITY_OSM) \
		--keep="highway=footway =pedestrian =path =living_street =service =steps" \
		-o=$(PEDESTRIAN_OSM)
	@osmconvert $(PEDESTRIAN_OSM) -o=$(PEDESTRIAN_OSM_PBF)