import scrapy
import re

class OxfordFoodSpider(scrapy.Spider):
	name = "OxfordFood"
	# TASK : Retrieving food terms from the Oxford Reference
	base_url_1 = "http://www.oxfordreference.com/view/10.1093/acref/9780199234875.001.0001/acref-9780199234875?btog=chap&hide=true&page="
	base_url_2 = "&pageSize=100&skipEditions=true&sort=titlesort&source=%2F10.1093%2Facref%2F9780199234875.001.0001%2Facref-9780199234875"
	start_urls = []
	for i in range(1,78):
		url = base_url_1 + str(i) + base_url_2
		start_urls.append(url)

	# Entry point for spider
	def parse(self, response):
		yield scrapy.Request(response.url, callback=self.parse_item)

	# parse the output
	def parse_item(self, response):
		food = response.css('#searchContent a::text').extract()

		yield {
			'Food' : food
		}

