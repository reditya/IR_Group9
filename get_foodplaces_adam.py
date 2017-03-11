import requests

api = 'https://api.foursquare.com'
endpoint = '/v2/venues/search'

# Mandatory parameters
params = {
	'client_id' : 'D1YBOR4SMZE2PUVRXXOCU1MKSIKKN01A4PCKNMTGEYZGELN1',
	'client_secret' : 'DPK3AIXZHLTP4MMFSNMPSZQEWHJLGXXXFCOLKVVDKIVLYLAW',
	'v' : '20170311'
}

params['near'] = 'Amsterdam'
# Category = food
params['categoryId'] = '4d4b7105d754a06374d81259'

request = requests.get(api+endpoint, params=params)
response = request.json()
print(response['response']['venues'])
