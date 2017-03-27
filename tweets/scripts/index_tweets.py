import json
import requests

elastic = 'http://localhost:9200'

with open('../twitter_food.json', 'rb') as twitter_file:
        for line in twitter_file:
		index  = json.loads(line)
		index['coordinate']['lon'] = index['coordinate'].pop('lng')
		index['createdTime'] = int(index['createdTime'])
		if index['lang'] == 'nl':
			index_tweet = '/dutch_tweets/tweet/'
		elif index['lang'] == 'en':
			index_tweet = '/english_tweets/tweet/'
		else:
			print('Tweet not in English, nor in Dutch')
			continue
		index.pop('lang')
		request = requests.post(elastic+index_tweet, json=index)
                if(request.status_code != 201):
                        print(index)
                        print(request.content)
                        break
