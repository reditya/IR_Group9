import requests

api = 'https://api.foursquare.com'
cat_endpoint = '/v2/venues/categories'
search_endpoint = '/v2/venues/search'

# Mandatory api parameters
params = {
	'client_id' : 'D1YBOR4SMZE2PUVRXXOCU1MKSIKKN01A4PCKNMTGEYZGELN1',
	'client_secret' : 'DPK3AIXZHLTP4MMFSNMPSZQEWHJLGXXXFCOLKVVDKIVLYLAW',
	'v' : '20170311'
}

cat_request = requests.get(api+cat_endpoint, params=params)
cat_response = cat_request.json()
categories = cat_response['response']['categories']
food_categories = []

for category in categories:
	if(category['name'] == 'Food'):
		food_categories = category['categories']

print(len(food_categories))

params['near'] = 'Amsterdam'
# max = 50
params['limit'] = 50
# Category = food
params['categoryId'] = '4d4b7105d754a06374d81259'

search_request = requests.get(api+search_endpoint, params=params)
search_response = search_request.json()
print(len(search_response['response']['venues']))
