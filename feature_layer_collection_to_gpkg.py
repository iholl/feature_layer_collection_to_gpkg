import json
import arcgis
import geopandas as gpd
from decouple import config

PORTAL_URL = "https://ndow.maps.arcgis.com"
PORTAL_USERNAME = config('ARCGIS_ONLINE_USERNAME')
PORTAL_PASSWORD = config('ARCGIS_ONLINE_PASSWORD')

feature_layer_collection_id = "8728c607a7064c7a9a47793d3bd03cd2"
gis = arcgis.GIS(PORTAL_URL, PORTAL_USERNAME, PORTAL_PASSWORD)
feature_layer_collection = gis.content.get(feature_layer_collection_id)

for fl in range(len(feature_layer_collection.layers)):
  layer = feature_layer_collection.layers[fl]
  layer_name = layer.properties.name
  feature_set = layer.query()
  geojson_string = feature_set.to_geojson
  geojson_dictionary = json.loads(geojson_string)
  gdf = gpd.GeoDataFrame.from_features(geojson_dictionary['features'])
  gdf.to_file("winter_raptor_data.gpks", layer=layer_name, driver="GPKG")
