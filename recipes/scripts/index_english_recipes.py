import requests
import json

elastic = 'http://localhost:9200'
index_en_endpoint = '/english_recipes/recipe/'

with open('../data/bitnami_new_english_recipes.json', 'rb') as en_recipes_file:
        for recipe_line in en_recipes_file:
                recipe = json.loads(recipe_line)

                request = requests.post(elastic+index_en_endpoint, json=recipe)
                if(request.status_code != 201):
                        print(recipe)
                        print(request.content)
                        break
