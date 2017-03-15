import urllib
import json

outfile = open('test_twitter_crawling_2_completely_filter.json', 'w')

text = ''
for line in open('test_twitter_crawling_2_clean_filter.json', 'r'):
    test = json.loads(line)
    lang = test['lang']
    text = test['text']
    print text
    if lang == 'en':
    	language = "english"
    elif lang == 'fr':
    	language = "french"
    elif lang == 'nl':
    	language = "dutch" 

    data = urllib.urlencode({"text":text , "language":language}) 
    u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    the_page = u.read()
    value  = json.loads(the_page)

    if value['probability']['neg'] < 0.7:
    	json.dump(test, outfile)
    	outfile.write('\n')

	