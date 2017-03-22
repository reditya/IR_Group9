import time
import json
from selenium import webdriver

filename = "amsfood2.txt"
location = []

with open(filename) as f:
        for l in f:
		location.append(l)

for loc in location:
	driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
	url = "https://www.instagram.com/explore/locations/" + str(loc) + "/?__a=1&max_id="
	a = driver.get(url);
	time.sleep(2)
	content = driver.find_element_by_tag_name('pre')
	content = content.text
	j = json.loads(content)
	j = j['location']
	print str(j['id']) + "|" + j['name'].encode('utf8') + "|" + str(j['lat']) + "|" + str(j['lng'])
	#print content.text
	driver.close()
