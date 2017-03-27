import sys
import json
import urlparse
import time
import datetime

# Document to write in
infile = sys.argv[1]
outfile = sys.argv[2]
outfile_non = sys.argv[3] # to detect non-language

# processing
outfile = open(outfile, 'w')
outfile_non = open(outfile_non, 'w')

for line in open(infile, 'r'):
	try:
    		test = json.loads(line)
    		if test['lang'] == 'nl' or test['lang'] == 'en' or test['lang'] == 'fr':
    			if test['coordinates'] is not None or test['place']['place_type'] == 'poi':
    				text = test['text']
    				new_text = ''
    				for i in text.split():
    					s, n, p, pa, q, f = urlparse.urlparse(i)
	    				if s and n:
	         				pass
	     				elif i[:1] == '@':
	         				pass
	     				elif i[:1] == '#':
	         				new_text = new_text.strip() + ' ' + i[1:]
	     				else:
	         				new_text = new_text.strip() + ' ' + i
	        		if test['coordinates'] is not None:
	        			coor = test['coordinates']['coordinates']
	        		elif test['place']['bounding_box']['coordinates'] == 'poi':
	        			coor = test['place']['place_type']	
    				data = {}
    				data['text'] = new_text	
    				data['lang'] = test['lang']
    				data['coordinate'] = {}
    				data['coordinate']['lng'] = coor[0]
    				data['coordinate']['lat'] = coor[1]    				
    				#data['date'] = test['created_at']
    				data['createdTime'] = test['created_at'].replace('+0000 ','')
    				data['createdTime'] = time.mktime(datetime.datetime.strptime(data['createdTime'],"%a %b %d %H:%M:%S %Y").timetuple()) + 3600
    				json.dump(data, outfile)
    				outfile.write('\n')
    		else:
    			if test['coordinates'] is not None or test['place']['place_type'] == 'poi':
    				text = test['text']
    				new_text = ''
    				for i in text.split():
    					s, n, p, pa, q, f = urlparse.urlparse(i)
	    				if s and n:
	         				pass
	     				elif i[:1] == '@':
	         				pass
	     				elif i[:1] == '#':
	         				new_text = new_text.strip() + ' ' + i[1:]
	     				else:
	         				new_text = new_text.strip() + ' ' + i
	        		if test['coordinates'] is not None:
	        			coor = test['coordinates']['coordinates']
	        		elif test['place']['bounding_box']['coordinates'] == 'poi':
	        			coor = test['place']['place_type']	
    				data = {}
    				data['text'] = new_text	
    				data['lang'] = test['lang']
    				data['coordinate'] = {}
    				data['coordinate']['lng'] = coor[0]
    				data['coordinate']['lat'] = coor[1]    				
    				#data['date'] = test['created_at']
    				data['createdTime'] = test['created_at'].replace('+0000 ','')
    				data['createdTime'] = time.mktime(datetime.datetime.strptime(data['createdTime'],"%a %b %d %H:%M:%S %Y").timetuple()) + 3600
    				json.dump(data, outfile_non)
    				outfile_non.write('\n')    				

	except ValueError,e:
		print "error"
