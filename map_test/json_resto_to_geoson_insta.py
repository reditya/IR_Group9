#! usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
import simplejson as json 
import pysal
import numpy as np

script, in_file, out_file = argv


def insta_to_geo(in_file, out_file, nb_type):

    data = json.load(open(in_file))

    nb_data = 0;
    for d in data['hits']:
        nb_data = nb_data + 1

    #### Create clusters

    # Extract all possible fields and construct weight matrix
    nb_type = 954 # This number should be retrieved from Elastic Search

    coor = np.zeros(shape=(nb_data,2))
    weight = np.zeros(shape=(nb_data,nb_type))
    ref_list = []
    index = 0;
    for d in data['hits']:
        coor[index][0] = d["coordinate"]['lng']
        coor[index][1] = d["coordinate"]['lat']
        category = d['food']
        for cat in category:
            if cat not in ref_list:
                ref_list.append(cat)
            i = ref_list.index(cat)    
            weight[index][i] = 1
        index = index + 1

    l = coor.tolist()

    # We will have to delete the repeated rows and add weights according to that.
    e = sorted((e,i) for i,e in enumerate(l))

    # Creation of the non-repetitive arrays
    new_coor = [np.array(coor[0,:])]
    new_weight = [np.array(weight[0,:])]
    #print new_coor[0]
    #new_coor = np.vstack([new_coor,coor[1,:]])
    #print new_weight
    #print new_coor[1]
    idx = 0
    for row in e:
        #print row[1]
        if row[0][0] == new_coor[idx][0] and row[0][1] == new_coor[idx][1]:
            new_weight[idx] = new_weight[idx] + weight[row[1],:]
            #print weight[row[1],:]
            #print new_weight[idx]
        else:
            new_coor = np.vstack([new_coor,row[0]])
            new_weight = np.vstack([new_weight, weight[row[1],:]])
            idx = idx + 1    
    print new_weight.shape
    #unique = [x for i, x in enumerate(l) if not i or x != b[l-1]]
    #a_unique = np.asarray(unique) 
    #print a_unique

    #print weight
    # The k value might have to change!
    wknn3 = pysal.weights.KNN(new_coor, k = 5)
    #print wknn3

    # The floor value should also be tuned.
    r = pysal.Maxp(wknn3, new_weight, floor = 5, floor_variable = np.ones((nb_data, 1)), initial = 99)
    print r.regions


    ### Create geoson file for the map
    cluster_id = np.zeros(shape=(new_coor.shape[0],1))
    nb_cluster = 0
    for M_list in r.regions:
        nb_cluster = nb_cluster + 1
        for m_list in M_list:
            cluster_id[m_list] = nb_cluster
    """
    idx = 0;
    for d in data['hits']:
        d['cluster'] = cluster_id[idx][0]
        idx = idx + 1
    """

    feature_list = []
    idx = 0
    for feat in new_coor:
        food_list = []
        print feat
        f_idx = 0
        for f in new_weight[idx]:
            if f > 0:
                food_list.append(ref_list[f_idx])
            f_idx = f_idx + 1    
        feature_list.append({
            "type": "Feature",
            "geometry" : {
                "type": "Point",
                "coordinates": [feat[0], feat[1]],
                },
            "properties" : {
                    "category": food_list,
                    "cluster": cluster_id[idx][0]
                }
         })
        idx = idx + 1

    geojson = {
        "type": "FeatureCollection",
        "features": feature_list
        }

    output = open(out_file, 'w')
    json.dump(geojson, output)


insta_to_geo(in_file,out_file,1)