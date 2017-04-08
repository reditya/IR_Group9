import requests
import csv
import json

elastic = 'http://localhost:9200'
index_endpoint = '/thuisbezorgd/restaurant/'

with open('../thuisbezorgd.csv', 'rb') as thuis_file:
	reader = csv.reader(thuis_file, delimiter=',', quotechar='"')
 	header = reader.next()
	for restaurant in reader:
		restaurant_index = {}
		restaurant_index['location'] = {}
		for i in range(0, len(restaurant)):
			if header[i] == 'longitude':
				restaurant_index['location']['lon'] = restaurant[i]
			elif header[i] == 'latitude':
				restaurant_index['location']['lat'] = restaurant[i]
			elif header[i] == 'review_rating':
				restaurant_index[header[i]] = json.dumps(float(restaurant[i]))
			else:
				restaurant_index[header[i]] = restaurant[i]
		request = requests.post(elastic+index_endpoint, json=restaurant_index)
		if(request.status_code != 201):
  			print(request.content)
			break
