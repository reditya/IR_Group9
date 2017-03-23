import requests
import csv
import re
import json

non_decimal = re.compile(r'[^\d.]+')

with open('../data/en_recipe.json', 'rb') as en_recipes_file:
	#du_recipes_reader = csv.reader(du_recipes_file, delimiter=',', quotechar='"')
	#header = du_recipes_reader.next()
	for recipe in en_recipes_file:
		print recipe
		recipe = json.loads(recipe)
		recipe_index = {}
		for i in range(0, len(recipe)):
			if header[i] == 'count_rating' or header[i] == 'finish_time' or header[i] == 'preparation_time':
				recipe[i] = non_decimal.sub('', recipe[i])
				recipe[i] = recipe[i].replace(',','.')
			# process the rating
			if header[i] == 'rating':
				rat = re.findall(r"([0-9][0-9]*)", recipe[i])
				if(rat[0]>10):
					rat[0] = int(rat[0])/10
				recipe[i] = str(rat[0])
			recipe_index[header[i]] = recipe[i]
		print json.dumps(recipe_index)	

