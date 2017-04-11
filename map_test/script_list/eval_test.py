# -*- coding: utf-8 -*-

from sys import argv
from os.path import exists
from list_function import pre_info_tweets, pre_info_insta, merge_datasets, remove_duplication_coor, add_category, grid_creation, remove_outliers, cluster_with_clusterpy



script, in_file1, in_file2, cat_file, out_file, out_file_2 = argv
nb_data_1, nb_type_1, ref_list_1, coor_1, weight_1 = pre_info_tweets(in_file1)
nb_data_2, nb_type_2, ref_list_2, coor_2, weight_2 = pre_info_insta(in_file2)

new_coor, new_weight, new_ref_list, new_nb_data = merge_datasets(ref_list_1,ref_list_2, nb_data_1,nb_data_2,nb_type_1, nb_type_2, coor_1, coor_2, weight_1, weight_2)

new_coor, new_weight = remove_duplication_coor(new_coor,new_weight,new_ref_list)

# Categories
cat_list, weight_category, corres_list = add_category(new_weight,new_ref_list,cat_file)

## Cluster by categories:


# 2 to test
new_weight, list_centroid, new_nb_data, list_coor = grid_creation(new_coor, weight_category)
new_weight = remove_outliers(list_centroid, new_weight, cat_list)
#return_cluster_pysal(list_centroid,new_weight, cat_list, new_nb_data,list_coor, out_file, out_file_2)
cluster_with_clusterpy(list_centroid,new_weight, cat_list, new_nb_data,list_coor, out_file, out_file_2,'True')
