import requests
import json
import re

# make sure number fields are really numbers
non_decimal = re.compile(r'[^\d.]+')

elastic = 'http://localhost:9200'
index_english_endpoint = '/english_recipes/recipe/'

mapping = {}
mapping['Step by step'] = 'step_by_step'
mapping['Image Link'] = 'image_link'
mapping['Ingredients'] = 'ingredients'
mapping['Title'] = 'title'
mapping['URL'] = 'url'
mapping['Rating'] = 'rating'
mapping['Finish Time'] = 'finish_time'
mapping['Count Rating'] = 'count_rating'
mapping['Preparation Time'] = 'preparation_time'

with open('../data/en_recipes.json', 'rb') as en_recipes_file:
	recipes = json.load(en_recipes_file)
	for recipe in recipes:
		recipe_index = {}
		for key in recipe:
			# Number and multi-valued fields
			if mapping[key] == 'count_rating' or mapping[key] == 'finish_time' or mapping[key] == 'preparation_time':
				for i in range(0, len(recipe[key])):
					recipe[key][i] = non_decimal.sub('', recipe[key][i]) 
				
			recipe_index[mapping[key]] = recipe[key]
		request = requests.post(elastic+index_english_endpoint, json=recipe_index)
                if(request.status_code != 201):
                        print(recipe)
                        print(request.content)
                        break
			
