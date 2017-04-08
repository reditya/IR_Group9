#! usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
import simplejson as json 
import pysal
import numpy as np
import shapefile as sp
import math
import clusterpy as cp
import csv
import sklearn.decomposition as sc
from sklearn.feature_selection import SelectKBest
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph
from collections import Counter

#script, in_file1, in_file2, out_file, out_file_2 , cat_file = argv


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


def remove_duplication_coor(coor, weight,ref_list,file_n = ''):
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
    #print new_weight.shape
    #unique = [x for i, x in enumerate(l) if not i or x != b[l-1]]
    #a_unique = np.asarray(unique) 
    #print a_unique


    """
    # Plot frequency of terms
    freq = np.sum(new_weight,axis=0)
    e = sorted((e,i) for i,e in enumerate(freq))
    
    labels = []
    values = []
    label_name = []    
    term_freq = []
    for i in e:
        labels.append(i[1])
        values.append(i[0])
        label_name.append(ref_list[i[1]])
        term_freq.append([ref_list[i[1]],i[0]])
    width = 0.2
    plt.bar(labels, values,width)
    plt.show()
    f = open(file_n,'w')
    l_t = list(reversed(term_freq))
    for i in l_t:
        f.write(i[0])
        f.write('  ')
        f.write(str(i[1]))
        f.write("\n")
    f.close    
    """
    return new_coor, new_weight

def func(z,i,j):
    print z
    #print z[i], z[j]
    q = np.sum(z[i]-z[j])
    return q

def return_cluster_pysal(new_coor, new_weight, ref_list, nb_data, list_coor, out_file, out_file_2):
    # The k value might have to change!
    wknn3 = pysal.weights.KNN(new_coor, k = 4)
    wknn3.transform = 'r'
    #print wknn3[0]
    
    """
    # statistic
    np.random.seed(12345)
    g4 = pysal.Gamma(new_weight, wknn3,operation = 'a')#operation=func)
    print g4.g
    # result 0
    print "%.3f"%g4.g_z
    # - 1.9111
    print g4.p_sim_g
    # 0.001
    print g4.min_g
    #  6
    print g4.max_g
    # 260
    print g4.mean_g
    # 38.1761761762
    """
    # The floor value should also be tuned.
    nb_try = 0
    condition = False
    floor_v = 4
    """
    while nb_try < 100 and not condition:
        print nb_try
        r = pysal.Maxp(wknn3, new_weight, floor = floor_v, floor_variable = np.ones((nb_data, 1)), initial = 40)
        mid_cond = True;
        reg_idx = 0;
        while mid_cond:
            sum_w = 0
            for i in r.regions[reg_idx]:
                sum_w = sum_w + np.sum(new_weight[i])
            if sum_w == 0:
                mid_cond = False    
            reg_idx = reg_idx + 1
        if mid_cond == True:
            condition = True
        nb_try = nb_try + 1
        if (nb_try%3 == 0):
            floor_v = floor_v + 1 
    #print r.regions
    """



    
    r = pysal.Maxp(wknn3, new_weight, floor = floor_v, floor_variable = np.ones((nb_data, 1)), initial = 99)

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

        # If the food list is empty, it's not an interesting cluster, we transform it into white
        #if not food_list:
        #    cluster_id[idx][0] = nb_cluster+1       
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
    


def hierarchical_clustering(nb_clust,nb_feat, centroid,cluster_init, dataCentroid):
    # Preparation of the contiguity matrix
    X = np.zeros(shape=(len(centroid),2))
    for key, value in centroid.iteritems():
        X[key] = value
    knn_graph = kneighbors_graph(X, 8, include_self=False)
    linkage = 'ward'
    dataModel = np.zeros(shape=(len(centroid),nb_feat))
    for key, value in dataCentroid.iteritems():
        dataModel[key] = value[1:(nb_feat+1)]
        #dataModel[key] = value
    
    model = AgglomerativeClustering(linkage=linkage, connectivity=knn_graph, n_clusters=nb_clust)
    model.fit(dataModel)
    new_id_clust = []
    for row in cluster_init:
        clust = model.labels_[row]
        new_id_clust.append(clust)
        print clust
    return new_id_clust

def cluster_with_clusterpy(new_coor, new_weight, ref_list, nb_data, list_coor, out_file, out_file_2, hierarchi='False'):
    # GeoSOM
    data = cp.importArcData("map_test/test_big_grid")
    var = data.fieldNames
    var_algo = var[0:len(var)-1]
    
    if hierarchi == 'False':
        it = 100
        nRow = 22
        nCol = 22
    else:
        it = 300
        nRow = 30
        nCol = 30
    data.cluster('geoSom', var_algo,wType='queen', nRows = nRow, nCols = nCol,iters=it)
    #data.exportRegions2area("test.csv")
    
    """
    with open('test.csv','rb') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        for row in reader:
            id_clust.append(int(row[1]))
    """
    cluster_init = data.region2areas
    id_clust = []

    for row in cluster_init:
        id_clust.append(row)
    ### Create geoson file for the map
    nb_clust = nRow*nCol
    print nb_clust
    print new_weight.shape
    # Centroid points
    # Polygon preparation

    # Preparation of hierarchical clustering
    centroid = data.oCentroid
    dataCentroid = data.dataCentroid
    nb_feat = new_weight.shape[1]
    
    if hierarchi == 'True':
        nb_clust = 800
        id_clust = hierarchical_clustering(nb_clust,nb_feat, centroid,cluster_init, dataCentroid)
    else:
        nb_clust = 380
        id_clust = hierarchical_clustering(nb_clust,nb_feat, centroid,cluster_init, dataCentroid)
    
    feature_list = []
    polygon_list = []
    idx = 0


    # Creation of the food list for each cluster (we take only the term with the highest frequency inside the cluster)
    term_list = []
    for i in range(nb_clust):
        term_list.append([])
    cor_idx = 0
    for i in new_weight:
        idx = 0
        for j in i:
            if j > 0:
                term_list[id_clust[cor_idx]].append(ref_list[idx])
            idx += 1
        cor_idx += 1   
            
    final_term_list = []
    for i in range(nb_clust):
        c = Counter(term_list[i])
        print c
        if c.values():
            m = max(c.values())
            r = [k for k in c if c[k] == m]
        else:
            r = []
        final_term_list.append(r)
        print "r: ", r            



    # Modify cluster numbers so that they are consecutive
    new_clust_id = []
    list_clust = []
    for i in id_clust:
        if i not in list_clust:
            list_clust.append(i)
    print len(list_clust)
    for i in id_clust:
        new_clust_id.append(list_clust.index(i))


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
                    "cluster": new_clust_id[idx]
                }
         })
        polygon_list.append({
            "type": "Feature",
            "geometry" : {
                "type": "Polygon",
                "coordinates": [[list_coor[idx]]],
                },
            "properties" : {
                    "category": final_term_list[id_clust[idx]],
                    "cluster": new_clust_id[idx]
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


def cluster_with_several_max(new_coor, new_weight, ref_list, nb_data,bool_file):
    # give ew eights and new ref list for pysal maxp
    # Just retrieve the most frequent element of each area


    print "cluster with several max"
    new_ref_list = []
    idx_list = []
    for i in range(nb_data):
        winner = np.argwhere(new_weight[i] == np.amax(new_weight[i])).flatten().tolist()
        for j in winner:
            if j not in idx_list and new_weight[i][j] != 0:
                idx_list.append(j)
                new_ref_list.append(ref_list[j])


    weight = np.zeros(shape=(nb_data,len(new_ref_list)))
    for i in range(nb_data):
        winner = np.argwhere(new_weight[i] == np.amax(new_weight[i])).flatten().tolist()
        for j in winner:
            if new_weight[i][j] != 0:
                v = new_weight[i][j]       
                weight[i][(idx_list.index(j))] = v

    return new_ref_list, weight
        
def multi_delete(list_, args):
    indexes = sorted((args), reverse=True)
    for index in indexes:
        del list_[index]
    return list_

def PCA_use(new_weight, new_ref_list):
    print "Feature selection"
    #freq = np.zeros(shape=(1,new_weight.shape[1]))
    freq = np.sum(new_weight,axis=0)
   
    column_idx = []
    for i in range(freq.shape[0]):
        #print freq[i] , i
        if freq[i] < 6:
            column_idx.append(i)
    weight = np.delete(new_weight,np.s_[column_idx],axis=1)
    ref_list = multi_delete(new_ref_list,column_idx)
    print weight.shape

    return weight, ref_list    
    """
    X = new_weight
    y = np.array(new_weight.shape[0])
    for i in range(new_weight.shape[0]):
        food_list = []
        for j in new_weight[i]:
            print j
            if j != 0:
                food_list.append(new_ref_list[j])
        y[i] = food_list    
    # PCA: feature extraction
    
    pca = sc.PCA(n_components=new_weight.shape[1], svd_solver='full')
    pca.fit(X)
    nb = pca.n_components_
    pca = sc.PCA(n_components=nb, svd_solver='full')
    pca.fit(X)
    print pca.explained_variance_ratio_
    new_weight = pca.fit_transform(X,y)
    # Feature selection
    """

def cluster_with_max(new_coor, new_weight, ref_list, nb_data, list_coor, out_file, out_file_2):
    # Just retrieve the most frequent element of each area

    id_clust_p = []
    for i in new_weight:
        if i[np.argmax(i)] != 0:
            id_clust_p.append(str(np.argmax(i)))
        else:
            id_clust_p.append(str(-1))

    ### Create geoson file for the map
    nb_cluster = len(set(id_clust_p))
    print nb_cluster
    mydict={}
    i = 0
    for item in id_clust_p:
        if(i>0 and item in mydict):
            continue
        else:    
            i = i+1
            mydict[item] = i

    id_clust=[]
    for item in id_clust_p:
        id_clust.append(mydict[item]-1)
    # Centroid points
    # Polygon preparation

    feature_list = []
    polygon_list = []
    idx = 0
    for feat in new_coor:
        food_list = []
        #for f in range(new_weight.shape[0]):
        if int(id_clust_p[idx]) > 0:
            food_list.append(ref_list[int(id_clust_p[idx])])
        elif int(id_clust_p[idx]) == 0 and new_weight[idx][0] != 0:
            food_list.append(ref_list[int(id_clust_p[idx])])
        

        feature_list.append({
            "type": "Feature",
            "geometry" : {
                "type": "Point",
                "coordinates": [feat[0], feat[1]],
                },
            "properties" : {
                    "category": food_list,
                    "cluster": id_clust[idx]
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
                    "cluster": id_clust[idx]
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


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

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
    print lat_add, lon_add
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
    list_centroid = np.delete(list_centroid, (0), axis=0)

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


    # Addition of the weights to the shapefile
    for i in range(0,weight.shape[1]):
        w.field(str(i),'F')
    w.field('sum_var','F') 
    
    for i in range(0,len(list_coor)):
        w.record(np.append(new_weight[i],np.sum(new_weight[i])))
   
    #w.record(totuple(str(new_weight[0]))
    
    w.save("map_test/test_big_grid")

    return new_weight, list_centroid, nb_data, list_coor    




def unique_food(coor, weight, ref_list, term):
    idx_f = ref_list.index(term)
    coor_list = []
    int_list = []
    nb_p = 0
    for i in range(weight.shape[0]):
        if weight[i][idx_f] > 0:
            coor_list.append(coor[i])
            int_list.append(weight[i][idx_f])
            if nb_p < weight[i][idx_f]:
                nb_p = weight[i][idx_f]
    # DBSCAN use
    db = DBSCAN(eps=0.003, min_samples=2).fit(coor_list)        
    labels = db.labels_
    print len(labels)
    unique_labels = set(labels)
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    list_list = []
    for k in range(len(unique_labels)):
        list_list.append([])
    idx = -1    
    for k in labels:
        idx = idx + 1
        if k >= 0:
            list_list[k].append([coor[idx][0], coor[idx][1]])


    # Centroid points
    # Polygon preparation

    feature_list = []
    polygon_list = []
    idx = 0
    food_list = [term]
    for feat in coor_list:
        if labels[idx] >= 0:
            feature_list.append({
                "type": "Feature",
                "geometry" : {
                    "type": "Point",
                    "coordinates": [feat[0], feat[1]],
                    },
                "properties" : {
                        "category": food_list,
                        "cluster": labels[idx],
                        "intensity":int_list[idx]/nb_p*10
                    }
             })
        idx = idx + 1
    
    for i in range(len(list_list)):
        polygon_list.append({
                "type": "Feature",
                "geometry" : {
                    "type": "Polygon",
                    "coordinates": [[list_list[i]]],
                    },
                "properties" : {
                        "category": food_list,
                        "cluster": i
                    }

                })    

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
    


def remove_outliers(coor, weight, ref_list):
    removed = 0
    for term in ref_list:
        idx_f = ref_list.index(term)
        coor_list = []
        for i in range(weight.shape[0]):
            if weight[i][idx_f] > 0:
                coor_list.append(coor[i])
        #print "term: ", term, "idx: ", idx_f, " nb points: ", len(coor_list)  
        if len(coor_list) > 0:      
            # DBSCAN use
            db = DBSCAN(eps=0.003, min_samples=3).fit(coor_list)        
            labels = db.labels_
            unique_labels = set(labels)
            n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

            #print('Estimated number of clusters: %d' % n_clusters_)

            list_list = []
            for k in range(len(unique_labels)):
                list_list.append([])
            idx = -1    
            for k in labels:
                idx = idx + 1
                if k >= 0:
                    list_list[k].append([coor[idx][0], coor[idx][1]])
                if k < 0:
                    removed = removed + 1
                    weight[idx][idx_f] = 0
    print "removed " , removed                
    return weight            


def add_category(weight, ref_list, cat_file):
    food_cat = []
    with open(cat_file,'r') as f:
        next(f)
        for line in f:
            currentline = line.split(",")
            food_cat.append([currentline[0],currentline[1].rstrip('\n')])


    cat_list = []
    # List of different categories
    for i in food_cat:
        if i[1] not in cat_list:
            cat_list.append(i[1])

    # Array of weights for the categories        
    weight_category = np.zeros(shape=(weight.shape[0],len(cat_list)))
    idx_coor = 0
    for i in weight:
        idx_food = 0
        for j in i:
            if j>0:
                food = ref_list[idx_food]
                for sublist in food_cat:
                    if sublist[0] == food:
                        cat = sublist[1]
                        weight_category[idx_coor][cat_list.index(cat)] += 1
                        break
            idx_food += 1            
        idx_coor += 1  

    return cat_list , weight_category, food_cat      


def select_category(cat_term, corres_list, ref_list ,point_weight):
    list_idx = []
    new_ref_list = []
    for i in corres_list:
        if i[0] == cat_term:
            idx_t = ref_list.index(i[1])
            list_idx.append(idx_t)
            new_ref_list.append(i[1])
    # Eliminate all terms which are not in the category.
    new_weight = np.zeros(shape=(point_weight.shape[0], len(new_ref_list)))
    idx_coor = 0
    for i in point_weight:
        idx_t = 0
        for j in list_idx:
            new_weight[idx_coor][idx_t] = point_weight[idx_coor][j]
            idx_t += 1
        idx_coor += 1
        
    return new_ref_list, new_weight        

def extract_cat(category, weight, ref_list, corres_list):
    # Get indexes and names of terms to keep
    idx_list = []
    term_list = []
    for i in corres_list:
        if i[1] == category:
            term_list.append(i[0])
            idx_list.append(ref_list.index(i[0]))
    print len(term_list)     
    new_weight = np.zeros(shape=(weight.shape[0],len(term_list)))
    w_idx = 0
    for i in idx_list:
        new_weight[:,w_idx] = weight[:,i]
        w_idx += 1
    return new_weight, term_list    


def unique_cat(coor, weight,ref_list,category, out_file, out_file_2):
    idx_f = ref_list.index(category)
    coor_list = []
    int_list = []
    nb_p = 0
    for i in range(weight.shape[0]):
        if weight[i][idx_f] > 0:
            coor_list.append(coor[i])
            int_list.append(weight[i][idx_f])
            if nb_p < weight[i][idx_f]:
                nb_p = weight[i][idx_f]
    # DBSCAN use
    db = DBSCAN(eps=0.003, min_samples=3).fit(coor_list)        
    labels = db.labels_
    print len(labels)
    unique_labels = set(labels)
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    list_list = []
    for k in range(len(unique_labels)):
        list_list.append([])
    idx = -1    
    for k in labels:
        idx = idx + 1
        if k >= 0:
            list_list[k].append([coor[idx][0], coor[idx][1]])


    # Centroid points
    # Polygon preparation

    feature_list = []
    polygon_list = []
    idx = 0
    food_list = [category]
    for feat in coor_list:
        if labels[idx] >= 0:
            feature_list.append({
                "type": "Feature",
                "geometry" : {
                    "type": "Point",
                    "coordinates": [feat[0], feat[1]],
                    },
                "properties" : {
                        "category": food_list,
                        "cluster": labels[idx],
                        "intensity":int_list[idx]/nb_p*10
                    }
             })
        idx = idx + 1
    
    for i in range(len(list_list)):
        polygon_list.append({
                "type": "Feature",
                "geometry" : {
                    "type": "Polygon",
                    "coordinates": [[list_list[i]]],
                    },
                "properties" : {
                        "category": food_list,
                        "cluster": i
                    }

                })    

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

"""
nb_data_1, nb_type_1, ref_list_1, coor_1, weight_1 = pre_info_tweets(in_file1)
nb_data_2, nb_type_2, ref_list_2, coor_2, weight_2 = pre_info_insta(in_file2)

new_coor, new_weight, new_ref_list, new_nb_data = merge_datasets(ref_list_1,ref_list_2, nb_data_1,nb_data_2,nb_type_1, nb_type_2, coor_1, coor_2, weight_1, weight_2)

new_coor, new_weight = remove_duplication_coor(new_coor,new_weight,new_ref_list)
new_nb_data = new_coor.shape[0]

# Categories

cat_list, weight_category, corres_list = add_category(new_weight,new_ref_list,cat_file)

## Cluster by categories:


# 2 to test
new_weight, list_centroid, new_nb_data, list_coor = grid_creation(new_coor, weight_category)
new_weight = remove_outliers(list_centroid, new_weight, cat_list)
return_cluster_pysal(list_centroid,new_weight, cat_list, new_nb_data,list_coor, out_file, out_file_2)
#cluster_with_clusterpy(list_centroid,new_weight, cat_list, new_nb_data,list_coor, out_file, out_file_2)

"""
## Cluster inside category:
"""
new_ref_list, new_weight = select_category(cat_term, corres_list, ref_list ,point_weight)
new_weight, list_centroid, new_nb_data, list_coor = grid_creation(new_coor, new_weight)

return_cluster_pysal(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)
cluster_with_clusterpy(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)
"""
#new_weight, new_ref_list = PCA_use(new_weight, new_ref_list)

#new_weight = remove_outliers(list_centroid, new_weight, new_ref_list)

# 1
#new_ref_list, new_weight = cluster_with_several_max(list_centroid, new_weight, new_ref_list, new_nb_data,True)

# 2
#new_weight = remove_outliers(list_centroid, new_weight, new_ref_list)

#return_cluster_pysal(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)

# 3
#cluster_with_clusterpy(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)

#cluster_with_max(list_centroid,new_weight, new_ref_list, new_nb_data,list_coor, out_file, out_file_2)

#unique_food(list_centroid, new_weight, new_ref_list, 'coffee')







