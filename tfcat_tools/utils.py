import json
from tfcat import TFCat
from tfcat.validate import JSONSCHEMA_URI

def write_json_file(cat: TFCat, json_path: str):
    with open(json_path, 'w') as file_json:
        json.dump(
            {
                "type": "FeatureCollection",
                "schema": JSONSCHEMA_URI,
                "features": cat.data.features,
                "fields" : cat.data.fields,
                "crs": cat.data.crs
            },
            file_json
        )