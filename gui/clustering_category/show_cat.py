from sys import argv
from os.path import exists
script, in_file1, in_file2, out_file, out_file_2 , cat_file, category, bool_heatmap = argv
from list_function import *

def show_all_cat(cat_file, out_file, out_file_2):
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



def show_cat_term(category, cat_file, out_file, out_file_2):
	print "show terms"
	nb_data_1, nb_type_1, ref_list_1, coor_1, weight_1 = pre_info_tweets(in_file1)
	nb_data_2, nb_type_2, ref_list_2, coor_2, weight_2 = pre_info_insta(in_file2)

	new_coor, new_weight, new_ref_list, new_nb_data = merge_datasets(ref_list_1,ref_list_2, nb_data_1,nb_data_2,nb_type_1, nb_type_2, coor_1, coor_2, weight_1, weight_2)
	cat_list, weight_category, corres_list = add_category(new_weight,new_ref_list,cat_file)
	new_weight, term_list = extract_cat(category, new_weight, new_ref_list, corres_list)
	print term_list
	new_coor, new_weight = remove_duplication_coor(new_coor,new_weight,term_list)
	
	new_weight, list_centroid, new_nb_data, list_coor = grid_creation(new_coor, new_weight)
	new_weight = remove_outliers(list_centroid, new_weight, term_list)
	new_nb_data = new_weight.shape[0]
	# Create the clusters inside the category
	#return_cluster_pysal(list_centroid,new_weight, term_list, new_nb_data,list_coor, out_file, out_file_2)
	cluster_with_clusterpy(list_centroid,new_weight, term_list, new_nb_data,list_coor, out_file, out_file_2,'False')
	
def show_cat_heatmap(category, cat_file, out_file, out_file_2):
	nb_data_1, nb_type_1, ref_list_1, coor_1, weight_1 = pre_info_tweets(in_file1)
	nb_data_2, nb_type_2, ref_list_2, coor_2, weight_2 = pre_info_insta(in_file2)

	new_coor, new_weight, new_ref_list, new_nb_data = merge_datasets(ref_list_1,ref_list_2, nb_data_1,nb_data_2,nb_type_1, nb_type_2, coor_1, coor_2, weight_1, weight_2)
	cat_list, weight_category, corres_list = add_category(new_weight,new_ref_list,cat_file)

	unique_cat(new_coor, weight_category ,cat_list,category, out_file, out_file_2)


if category == 'all':
	show_all_cat(cat_file, out_file, out_file_2)
else:
	print bool_heatmap
	if bool_heatmap == 'True':
		show_cat_heatmap(category,cat_file, out_file, out_file_2)
	else:
		show_cat_term(category,cat_file, out_file, out_file_2)	

