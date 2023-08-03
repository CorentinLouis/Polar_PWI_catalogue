import pandas as pd
import glob
import scipy.io as io
import numpy
from tfcat import TFCat
from shapely.geometry import MultiPoint, Point, Polygon, MultiPolygon
from astropy.time import Time
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
import h5py
from h5py import File
import numpy as np
from datetime import datetime
from os import path
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import csv
from tqdm import tqdm
import seaborn as sns 
from scipy.stats import binned_statistic_2d
from shapely.ops import unary_union

plt.rcParams["figure.figsize"] = (200,100)


def get_polygons(polygon_fp,start, end, type_):
    date_time = [start, end]
    #Convert start/stop times to unix from isoformat.
    unix_start, unix_end = Time(date_time,format='isot').to_value('unix')
    if path.exists(polygon_fp):
        catalogue = TFCat.from_file(polygon_fp)

    #array of polygons found within time interval specified.
    polygon_dict = {}

    for key in type_ :
        features_polygon = []
        for i in range(len(catalogue)):
            label = catalogue.data.features[i]['properties']['feature_type']
            time_points = numpy.array(catalogue.data.features[i]['geometry']['coordinates'][0])[:,0]
            if any((time_points[time_points >= unix_start])) and any((time_points[time_points <= unix_end])):
                if label == key:
                    features_polygon.append(Polygon(catalogue.feature(i).geometry.coordinates[0]))
        polygon_dict[key] = unary_union(MultiPolygon(features_polygon))
    return polygon_dict


def compute_data_points(data, time, freq):
    times_coords = numpy.zeros_like(data)
    freqs_coords = numpy.zeros_like(data)
    times_coords[:,:], freqs_coords[:,:] = numpy.copy(time[:,None]), numpy.copy(freq[None, :])
    coords = [(t, f) for t, f in zip(times_coords.flatten(), freqs_coords.flatten())]
    _data = data.flatten()
    index = numpy.arange(len(_data), dtype=int)
    data_points = MultiPoint([Point(x, y, z) for (x, y), z in zip(coords, index)]) 
    return(data_points)


def compute_mask(data, time, freq, polygon_array, feature_type, data_points):
    mask = {}
    for key in tqdm(feature_type):
        _mask_array = numpy.zeros((data.size,))
        print(key)
        if not polygon_array[key].is_empty :
            select_points = polygon_array[key].intersection(data_points)
            _mask_array[[int(geom.z) for geom in select_points.geoms]] = 1
            _mask_array = _mask_array.reshape(time.shape[0], freq.shape[0])
        mask[key] = (_mask_array > 0).reshape(time.shape[0], freq.shape[0])
    return mask


def apply(data,mask,
            feature_type: str,
            invert : bool = False):
    for key in feature_type :
        if not "mask_final" in locals() :
            mask_final = numpy.copy(mask[key])
            print(key)
        else : 
            mask_final += mask[key]
            print(key)
    if invert == True :
        return data*~mask_final
    else : 
        return data*mask_final



