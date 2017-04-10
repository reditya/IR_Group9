#! usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

from sys import argv
from os.path import exists
import simplejson as json 

import pandas
from collections import Counter

import matplotlib.pyplot as plt

script, in_file = argv

# Total number of judgements
nb_judge = 0
# Percentage of well describing food terms
nb_correct_food = 0
# Percentage of right sentiment
nb_correct_sentiment = 0
# List of missing food terms and their frequency
term_list = []
nb_not_forgotten = 0
# Not evaluated term lists
NA_food = 0
# Nb agreement for the different questions
agree_corr_sentiment = 0
agree_corr_term = 0

# Percentages only for the data with total agreement
# Percentage of well describing food terms
nb_correct_food_a = 0
# Percentage of right sentiment
nb_correct_sentiment_a = 0



with open(in_file) as f:
    for line in f:
        j_content = json.loads(line)
        if j_content['judgments_count'] == 1:
            judge = j_content['results']['judgments'][0]
            if judge['worker_trust']  > 0.8: # We only keep data when the worker is trusted
                nb_judge += 1
                agree_corr_term += 1
                agree_corr_sentiment += 1
                # Food terms
                if judge['data']['are_all_the_food_terms_retrieved_used_to_describe_actual_food_here'] == 'yes':
                    nb_correct_food += 1
                    nb_correct_food_a += 1
                # Sentiment 
                if judge['data']['is_the_post_giving_a_neutral_or_positive_appreciation_yespositive_or_neutral__no_negative'] == 'yes': 
                    nb_correct_sentiment += 1
                    nb_correct_sentiment_a += 1
                food = judge['data']['please_mention_all_food_terms_in_the_post_that_are_not_contained_in_the_food_list_separate_each_food_by_comma_and_which_are_used_to_desribe_actual_food_if_no_term_is_missing_write_a_dot__if_the_post_is_in_a_language_you_dont_understand_write_na']
                if food == ".":
                    nb_not_forgotten += 1
                elif food == "NA":
                    NA_food += 1    
                else:
                    bool_c = False
                    for i in range(0, len(food)):
                        if food[i]==",":
                            bool_c = True
                    if bool_c:  
                        print food
                        food = [x.strip() for x in food.split(',')]    
                        print food  
                        term_list.extend(food)
                    else:
                        term_list.extend(food)
        else:
            # Q1
            nb_judge += j_content['judgments_count']

            # When agreement needed
            judge = j_content['results']['are_all_the_food_terms_retrieved_used_to_describe_actual_food_here']
            if judge['confidence'] == 1.0:
                agree_corr_term += j_content['judgments_count']
                if judge['agg'] == "yes":
                    nb_correct_food_a += j_content['judgments_count']
            
            judge = j_content['results']['is_the_post_giving_a_neutral_or_positive_appreciation_yespositive_or_neutral__no_negative']   
            if judge['confidence'] == 1.0:
                agree_corr_sentiment += j_content['judgments_count']
                if judge['agg'] == "yes":
                    nb_correct_sentiment_a += j_content['judgments_count']
            
            # When no agreement needed
            judge = j_content['results']['judgments']
            for i in judge:
                if i['worker_trust']  > 0.8: # We only keep data when the worker is trusted
                    # Food terms
                    if i['data']['are_all_the_food_terms_retrieved_used_to_describe_actual_food_here'] == 'yes':
                        nb_correct_food += 1
                    # Sentiment 
                    if i['data']['is_the_post_giving_a_neutral_or_positive_appreciation_yespositive_or_neutral__no_negative'] == 'yes': 
                        nb_correct_sentiment += 1
                    food = i['data']['please_mention_all_food_terms_in_the_post_that_are_not_contained_in_the_food_list_separate_each_food_by_comma_and_which_are_used_to_desribe_actual_food_if_no_term_is_missing_write_a_dot__if_the_post_is_in_a_language_you_dont_understand_write_na']
                    if food == ".":
                        nb_not_forgotten += 1
                    elif food == "NA":
                        NA_food += 1    
                    else:
                        bool_c = False
                        for i in range(0, len(food)):
                            if food[i]==",":
                                bool_c = True
                        if bool_c:   
                            print food     
                            food = [x.strip() for x in food.split(',')]      
                            term_list.extend(food)
                            print food
                        else:
                            term_list.extend(food)
                            print food


print "nb judgement: ", nb_judge, "nb not forgotten terms: ", nb_not_forgotten
print "% total correct food: ", (nb_correct_food/nb_judge) , " % correct food among agreed data: ", nb_correct_food_a/nb_judge , " nb agreement: ", agree_corr_term                       
print "% total correct sentiment: ", nb_correct_sentiment/nb_judge , " % correct sentiment among agreed data: ", nb_correct_sentiment_a/nb_judge, " nb agreement: ", agree_corr_sentiment

term_counts = Counter(term_list)
print term_counts
df = pandas.DataFrame.from_dict(term_counts, orient='index')
df.plot(kind='bar')                     
print df