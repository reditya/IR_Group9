import requests
import csv
import re

# make sure number fields are really numbers
non_decimal = re.compile(r'[^\d.]+')

elastic = 'http://localhost:9200'
index_dutch_endpoint = '/dutch_recipes/recipe/'

with open('../data/du_recipes.csv', 'rb') as du_recipes_file:
	du_recipes_reader = csv.reader(du_recipes_file, delimiter=',', quotechar='"')
	header = du_recipes_reader.next()
	for recipe in du_recipes_reader:
		recipe_index = {}
		for i in range(0, len(recipe)):
			if header[i] == 'count_rating' or header[i] == 'finish_time' or header[i] == 'preparation_time':
				recipe[i] = non_decimal.sub('', recipe[i])
				recipe[i] = recipe[i].replace(',','.')
			recipe_index[header[i]] = recipe[i]
		request = requests.post(elastic+index_dutch_endpoint, json=recipe_index)
		if(request.status_code != 201):
			print(recipe)
			print(request.content)
			break
