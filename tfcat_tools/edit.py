import numpy
from astropy.table import vstack

from tfcat import TFCat 
from tfcat_tools.featureaddons import FeatureCollection

def merge(*cats: TFCat):
    crs = cats[0].crs
    properties = cats[0].properties
    fields= cats[0].data.fields
    schema = cats[0].data["$schema"]
    for cat in cats :
        if not crs == cat.crs or not properties == cat.properties or not fields == cat.data.fields:
           raise TypeError("catalogs to merged should have the same crs, properties and fields")
        event = FeatureCollection(cat.data, properties=properties, fields=fields, crs=crs, schema=schema).as_table()
        if not "merged_event" in locals() :
            merged_event = event
        else :
            merged_event = vstack([merged_event, event])
    merged_event.sort(['tmin'])
    return TFCat(FeatureCollection().from_table(table=merged_event, properties=properties, fields=fields, crs=crs, schema=schema))

def remove_feature(cat: TFCat, 
            tstart, 
            tend, 
            feature_type: str):
    crs = cat.crs
    properties = cat.properties
    fields= cat.data.fields
    schema = cat.data["$schema"]
    event = FeatureCollection(cat.data, properties=properties, fields=fields, crs=crs, schema=schema).as_table()
    removed_event = event[
                    not event['tmin'] > tstart and event['tmax'] < tend and  event['feature_type'] == feature_type
                    ]
    return TFCat(FeatureCollection().from_table(table=removed_event, properties=properties, fields=fields, crs=crs, schema=schema))

def rename_feature(cat: TFCat, 
            tstart, 
            tend, 
            feature_type: str,
            new_feature_type: str):
    crs = cat.crs
    properties = cat.properties
    fields= cat.data.fields
    schema = cat.data["$schema"]
    event = FeatureCollection(cat.data, properties=properties, fields=fields, crs=crs, schema=schema).as_table()
    event['feature_type'][numpy.where(event['tmin'] > tstart and event['tmax'] < tend and event['feature_type'] == feature_type)] = new_feature_type
    return TFCat(FeatureCollection().from_table(table=event, properties=properties, fields=fields, crs=crs, schema=schema))

#cut
#divide