import json
import sys

infile = sys.argv[1]

with open(infile) as f:
	for l in f:
		d = json.loads(l)
		fterm = d['food']
		for i in fterm:
			print i
