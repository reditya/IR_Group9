import json
import requests

elastic = 'http://localhost:9200'
index_instagram = '/instagram/post/'

with open('../json_instagram_post_location.json', 'rb') as instagram_file:
        for line in instagram_file:
		index  = json.loads(line)
		index['coordinate']['lon'] = index['coordinate'].pop('lng')
		request = requests.post(elastic+index_instagram, json=index)
                if(request.status_code != 201):
                        print(recipe)
                        print(request.content)
                        break
