import requests
import json

elastic = 'http://localhost:9200'
index_endpoint = '/restaurants/restaurant/'

with open('restaurants.json', 'r') as restaurants_file:
	restaurants = json.loads(restaurants_file.read())

for restaurant in restaurants:
	restaurant_index = {}
	restaurant_index['location'] = {}

	restaurant_index['name'] = restaurant['name']
	restaurant_index['category'] = restaurant['categories'][0]['name']
	restaurant_index['location']['lat'] = restaurant['location']['lat']
	restaurant_index['location']['lon'] = restaurant['location']['lng']
	request = requests.post(elastic+index_endpoint, json=restaurant_index)

