import json

with open("json_instagram_post.json") as f:
	for l in f:
		d = json.loads(l)
		lat = d['coordinate']['lat']
		lng = d['coordinate']['lng']

		if lat != "None" and lat.replace('.','',1).isdigit() and lng != "None" and lng.replace('.','',1).isdigit() :
			print l.rstrip("\n")