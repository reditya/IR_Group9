from __future__ import division
import requests
import csv
import re
import json
import sys

non_decimal = re.compile(r'[^\d.]+')

input = sys.argv[1]

# order Step by step,Rating,Image Link,Count Rating,Description,Title,URL,Ingredients,Preparation Time,Finish Time

with open(input, 'rb') as du_recipes_file:
	du_recipes_reader = csv.reader(du_recipes_file, delimiter=',', quotechar='"')
	header = du_recipes_reader.next()
	for recipe in du_recipes_reader:
		recipe_index = {}
		for i in range(0, len(recipe)):
			if header[i] == 'finish_time' or header[i] == 'preparation_time':
				time = recipe[i].split(",")
				if len(time) > 1:
					recipe[i] = int(time[0])*60 + int(time[1])
				else:
					recipe[i] = time[0]
				#recipe[i] = non_decimal.sub('', recipe[i])
				#recipe[i] = recipe[i].replace(',','.')
			# process the rating
			if header[i] == 'rating':
				rat = re.findall(r"([0-9][0-9]*)", recipe[i])
				if(int(rat[0])>10):
					rat[0] = int(rat[0])/10
				recipe[i] = str(rat[0])
			if header[i] == 'count_rating':
				rat = re.findall(r"([0-9][0-9]*)", recipe[i])
				recipe[i] = str(rat[0])

			recipe_index[header[i]] = recipe[i]
		print json.dumps(recipe_index)	

