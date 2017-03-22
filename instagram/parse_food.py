import sys
import json
import datetime

filename = sys.argv[1]

with open(filename) as f:
        for l in f:
                d = json.loads(l)
                if d['locationId'] is not None and d['caption'] is not None:
                        print d['locationId']
