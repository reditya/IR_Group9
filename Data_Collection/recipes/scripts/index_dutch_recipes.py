import requests
import json

elastic = 'http://localhost:9200'
index_dutch_endpoint = '/dutch_recipes/recipe/'

with open('../data/bitnami_new_dutch_recipes.json', 'rb') as du_recipes_file:
	for recipe_line in du_recipes_file:
		recipe = json.loads(recipe_line)	
	
		request = requests.post(elastic+index_dutch_endpoint, json=recipe)
		if(request.status_code != 201):
			print(recipe)
			print(request.content)
			break
