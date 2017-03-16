import requests
import json

api = 'https://api.foursquare.com'
cat_endpoint = '/v2/venues/categories'
search_endpoint = '/v2/venues/search'

# Mandatory api parameters
params = {
	'client_id' : 'D1YBOR4SMZE2PUVRXXOCU1MKSIKKN01A4PCKNMTGEYZGELN1',
	'client_secret' : 'DPK3AIXZHLTP4MMFSNMPSZQEWHJLGXXXFCOLKVVDKIVLYLAW',
	'v' : '20170311'
}

# Get all sub food categories
cat_request = requests.get(api+cat_endpoint, params=params)
cat_response = cat_request.json()
categories = cat_response['response']['categories']
food_categories = []
for category in categories:
	if(category['name'] == 'Food'):
		food_categories = category['categories']

# Get all restaurants in sub food categories near Amsterdam
restaurants = []
params['near'] = 'Amsterdam'
# max = 50
params['limit'] = 50
for food_category in food_categories:
	params['categoryId'] = food_category['id']
	search_request = requests.get(api+search_endpoint, params=params)
	search_response = search_request.json()
	restaurants += search_response['response']['venues']

with open('restaurants.json', 'w') as outfile:
	json.dump(restaurants, outfile)
