#! usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
import simplejson as json 
import pysal
import numpy as np
import shapefile as sp
import math

script, in_file1, in_file2, out_file, out_file_2 = argv


#def tweets_to_geo(in_file1,in_file2, out_file):


# This function takes tweets input and return number of data, number of categories and list of categories.
def pre_info_tweets(in_file1):
    data = json.load(open(in_file1))

    nb_data = 0;
    for d in data['hits']['hits']:
        nb_data = nb_data + 1
   

    # Find the nmber of different food terms

    nb_type = 0;
    ref_list = []

    for d in data['hits']['hits']:
        category = d['_source']['food']
        for cat in category:
            if cat not in ref_list:
                ref_list.append(cat)
    nb_type = len(ref_list)

    coor = np.zeros(shape=(nb_data,2))
    weight = np.zeros(shape=(nb_data,nb_type))
    index = 0;
    for d in data['hits']['hits']:
        coor[index][0] = d['_source']["coordinate"]['lon']
        coor[index][1] = d['_source']["coordinate"]['lat']
        category = d['_source']['food']
        for cat in category:
            i = ref_list.index(cat)    
            weight[index][i] = 1
        index = index + 1


    return nb_data, nb_type, ref_list, coor, weight

def pre_info_insta(in_file2):
    data = json.load(open(in_file2))

    nb_data = 0;
    for d in data['hits']['hits']:
        nb_data = nb_data + 1

    ref_list = []
    nb_type = 0;

    for d in data['hits']['hits']:
        category = d['_source']['food']
        for cat in category:
            if cat not in ref_list:
                ref_list.append(cat)
    nb_type = len(ref_list)

    coor = np.zeros(shape=(nb_data,2))
    weight = np.zeros(shape=(nb_data,nb_type))
    index = 0;
    for d in data['hits']['hits']:
        coor[index][0] = d['_source']["coordinate"]['lon']
        coor[index][1] = d['_source']["coordinate"]['lat']
        category = d['_source']['food']
        for cat in category:
            i = ref_list.index(cat)    
            weight[index][i] = 1
        index = index + 1


    return nb_data, nb_type, ref_list, coor, weight


def merge_datasets(ref_list1,ref_list2, nb_data1,nb_data2,nb_type_1, nb_type_2, coor1, coor2, weight1, weight2):    
    new_ref_list = ref_list1;
    for i in ref_list2:
        if i not in new_ref_list:
            new_ref_list.append(i)
    new_nb_type = len(new_ref_list)
    new_nb_data = nb_data1 + nb_data2        

    new_coor = np.zeros(shape=(new_nb_data,2))
    new_weight = np.zeros(shape=(new_nb_data,new_nb_type))
    
    zero_compl = np.zeros(shape=(new_nb_type - nb_type_1))
    
    for i in range(0,nb_data1):
        new_coor[i] = coor1[i]
        new_row =  np.hstack((weight1[i],zero_compl))
        new_weight[i] = new_row
    for i in range(0,nb_data2):
        idx_w = 0;
        new_coor[nb_data1+ i] = coor2[i]
        for j in weight2[i]:
            if j > 0:
                new_idx = new_ref_list.index(ref_list2[idx_w])
                new_weight[nb_data1+ i][new_idx] = j 
            idx_w = idx_w + 1
    

    return new_coor, new_weight, new_ref_list, new_nb_data            


def remove_duplication_coor(coor, weight):
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
    return new_coor, new_weight



def return_cluster(new_coor, new_weight, ref_list, nb_data, list_coor, out_file, out_file_2):
    # The k value might have to change!
    wknn3 = pysal.weights.KNN(new_coor, k = 5)
    #print wknn3

    # The floor value should also be tuned.
    r = pysal.Maxp(wknn3, new_weight, floor = 3, floor_variable = np.ones((nb_data, 1)), initial = 99)
    #print r.regions


    ### Create geoson file for the map
    cluster_id = np.zeros(shape=(new_coor.shape[0],1))
    nb_cluster = 0
    for M_list in r.regions:
        nb_cluster = nb_cluster + 1
        for m_list in M_list:
            cluster_id[m_list] = nb_cluster
    print nb_cluster
    
    # Centroid points
    # Polygon preparation

    feature_list = []
    polygon_list = []
    idx = 0
    for feat in new_coor:
        food_list = []
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
        polygon_list.append({
            "type": "Feature",
            "geometry" : {
                "type": "Polygon",
                "coordinates": [[list_coor[idx]]],
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

    geojson_2 = {
        "type": "FeatureCollection",
        "features": polygon_list
        }
    output = open(out_file, 'w')
    json.dump(geojson, output)
    output_2 = open(out_file_2, 'w')
    json.dump(geojson_2, output_2)







def grid_creation(coor, weight):
    w = sp.Writer(sp.POLYGON)

    # Grid definition
    print "intitialisation"
    #Position, decimal degrees
    lat = 52.29
    lon = 4.73
    lat_max = 52.42
    lon_max = 4.98

    #Earth’s radius, sphere
    R=6378137

    #offsets in meters
    dn = 200
    de = 200

    #Coordinate offsets in radians
    dLat = dn/R
    dLon = de/(R*math.cos(math.pi*lat/180))

    #OffsetPosition, decimal degrees
    lat_add = 0.001 #dLat * 180/math.pi
    lon_add = dLon * 180/math.pi 
    print lat_add
    print lon_add
    i = lon
    j = lat
    nb_data = 0
    list_coor = []
    list_centroid = np.array([0,0])
    nb_i = 1
    print "preparation of coordinates"
    while (i < lon_max):
        nb_j = 1
        j = lat
        while (j < lat_max):
            nb_data = nb_data + 1
            point = [[[i,j],[i+lon_add,j],[i+lon_add,j+lat_add],[i,j+lat_add],[i,j]]]
            list_coor.append([[i,j],[i+lon_add,j+lat_add]])
            list_centroid = np.vstack([list_centroid, [i+lon_add/2,j+lat_add/2]])
            w.poly(parts=point, shapeType=sp.POLYLINE)
            j = j + lat_add
            nb_j = nb_j + 1
        i = i + lon_add  
        nb_i = nb_i + 1
    print len(list_coor)
    list_centroid = np.delete(list_centroid, (0), axis=0)
    print nb_i, nb_j

    print list_centroid.shape
    print "preparation of weights"
    print weight.shape[1]
    new_weight = np.zeros(shape=(nb_data,weight.shape[1]))
    idx_coor = 0
    for coordinate in coor:
        #print coordinate[0]
        #print coordinate[1]
        bool_test = False
        list_idx = 0
        while (not bool_test and list_idx < len(list_coor)):
            #print list_coor[list_idx][1][0] , list_coor[list_idx][0][0], list_coor[list_idx][1][1], list_coor[list_idx][0][1]
            if (coordinate[0] < list_coor[list_idx][1][0] and coordinate[0] >= list_coor[list_idx][0][0] and coordinate[1] < list_coor[list_idx][1][1] and coordinate[1] >= list_coor[list_idx][0][1]):
                bool_test = True
                new_weight[list_idx] = new_weight[list_idx] + weight[idx_coor]
            list_idx = list_idx + 1
        idx_coor = idx_coor + 1     
    w.save("map_test/test_big_grid")

    print new_weight
    return new_weight, list_centroid, nb_data, list_coor    

nb_data_1, nb_type_1, ref_list_1, coor_1, weight_1 = pre_info_tweets(in_file1)
nb_data_2, nb_type_2, ref_list_2, coor_2, weight_2 = pre_info_insta(in_file2)

new_coor, new_weight, new_ref_list, new_nb_data = merge_datasets(ref_list_1,ref_list_2, nb_data_1,nb_data_2,nb_type_1, nb_type_2, coor_1, coor_2, weight_1, weight_2)

new_coor, new_weight = remove_duplication_coor(new_coor,new_weight)

new_weight, list_centroid, new_nb_data, list_coor = grid_creation(new_coor, new_weight)

return_cluster(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)










