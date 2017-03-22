#! usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
import simplejson as json 
import pysal
import numpy as np

script, in_file, out_file = argv

data = json.load(open(in_file))


#### Create clusters


# Extract all possible fields and construct weight matrix
nb_data = 0;
for d in data['hits']['hits']:
    nb_data = nb_data + 1

nb_type = 181 # This number should be retrieved from Elastic Search

coor = np.zeros(shape=(nb_data,2))
weight = np.zeros(shape=(nb_data,nb_type))
ref_list = []
index = 0;
for d in data['hits']['hits']:
    coor[index][0] = d['_source']['location']["lon"]
    coor[index][1] = d['_source']['location']["lat"]
    category = d['_source']['category']
    if category not in ref_list:
        ref_list.append(category)
    i = ref_list.index(category)    
    weight[index][i] = 1
    index = index + 1

# The k value might have to change!
wknn3 = pysal.weights.KNN(coor, k = 10)
# The floor value should also be tuned.
r = pysal.Maxp(wknn3, weight, floor = 10, floor_variable = np.ones((nb_data, 1)), initial = 60)


### Create geoson file for the map
cluster_id = np.zeros(shape=(nb_data,1))
nb_cluster = 0
for M_list in r.regions:
    nb_cluster = nb_cluster + 1
    for m_list in M_list:
        cluster_id[m_list] = nb_cluster
idx = 0;
for d in data['hits']['hits']:
    d['_source']['cluster'] = cluster_id[idx][0]
    idx = idx + 1
print nb_cluster


geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [d['_source']['location']["lon"], d['_source']['location']["lat"]],
            },
        "properties" : {
                "category": d['_source']['category'],
                "cluster": d['_source']['cluster']
            }
     } for d in data['hits']['hits']]
}


output = open(out_file, 'w')
json.dump(geojson, output)

