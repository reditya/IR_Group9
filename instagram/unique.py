import json

with open("json_instagram_post_location.json") as f:
	for l in f:
		d = json.loads(l)
		fterm = d['food']
		for i in fterm:
			print i