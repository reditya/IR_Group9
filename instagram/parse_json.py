import sys
import json
import datetime

post_file = sys.argv[1]
coordinate_file = sys.argv[2]

outfile = sys.argv[3]
outfile = open(outfile, 'w')

location_dict = {}

# read the coordinate file
with open(coordinate_file) as f:
	for l in f:
		d = l.split("|")
		loc = {}
		#loc['id'] = d[0]
		#loc['name'] = d[1]
		loc['lat'] = d[2].rstrip()
		loc['lng'] = d[3].rstrip()
		location_dict[d[0]] = loc

# read the instagram posts file
with open(post_file) as f:
        for l in f:
    		post = {}
    		d = json.loads(l)
    		if d['locationId'] is not None and d['caption'] is not None:
				post['createdTime'] = d['createdTime']
				post['text'] = d['caption'].replace('\r', ' ').replace('\n', ' ')
				post['locationId'] = d['locationId']
				post['locationName'] = d['locationName']
				post['coordinate'] = location_dict[d['locationId']]
				#print str(d['createdTime']) + "" + d['caption'].replace('\r', ' ').replace('\n',' ').encode('utf8') + "|" + str(d['locationId'])
				json.dump(post, outfile)
				outfile.write("\n")