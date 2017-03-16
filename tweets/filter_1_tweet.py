import json
import urlparse

# Document to write in
outfile = open('test_twitter_crawling_2_clean.json', 'w')
for line in open('test_twitter_crawling_2.json', 'r'):
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
    		data['coordinates'] = coor
    		data['date'] = test['created_at']
    		json.dump(data, outfile)
    		outfile.write('\n')
