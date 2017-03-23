import scrapy
import re
import json

class OxfordFoodSpider(scrapy.Spider):
	name = "OxfordFood"
	# TASK : Retrieving food terms from the Oxford Reference
	#base_url_1 = "https://www.instagram.com/explore/locations/"
	#base_url_2 = "/?__a=1&max_id=\\n"
	start_urls = []

	with open("instagram_id") as f:
		for line in f:
			#url = base_url_1 + str(line) + base_url_2
			start_urls.append(line)

	# Entry point for spider
	def parse(self, response):
		yield scrapy.Request(response.url, callback=self.parse_item)

	# parse the output
	def parse_item(self, response):
		json_response = json.loads(response.body_as_unicode)
		latitude = json_response['lat']
		longitude = json_response['lng']
		id = json_response['id']
		name = json_response['name']
		print response.url

		yield {
			'id' : id,
			'name' : name,
			'longitude' : longitude, 
			'latitude' : latitude
		}

