import sys
import json
import datetime

filename = sys.argv[1]
param = sys.argv[2]

with open(filename) as f:
	for l in f:
		d = json.loads(l)
		if d['locationId'] is not None and d['caption'] is not None:
			if param == "getLocationPost":
				print d
			elif param == "getLocationId":
				print d['locationId']
