import scrapy
import re
import json

class ThuisbezorgdSpider(scrapy.Spider):
	name = "Thuisbezorgd"
	# TODO : iterate over url_list.txt for all links
	# This is just an example of scraping brood pages with max 38 page recipes
	start_urls = []
	with open("thuisbezorgd_recipes.txt") as f:
		next(f)
		for line in f: 
			content = line.split("|")
			url = content[1]
			start_urls.append(url)

	# Entry point for spider
	def parse(self, response):
		for href in response.css('.restaurantname .restaurantname::attr(href)'):
			url = href.extract()
			url = 'https://www.thuisbezorgd.nl' + url
			yield scrapy.Request(url, callback=self.parse_item)

	# parse the output
	def parse_item(self, response):
		#title = response.css('.recipeSummary__title2 span::text').extract()[0]
		data = response.xpath("//script[@type='application/ld+json']/text()").extract()[0]
		data = json.loads(data)
		
		name = data['name']
		url = data['url']
		latitude = data['geo']['latitude']
		longitude = data['geo']['longitude']
		telephone = data['telephone']
		review_count = data['aggregateRating']['reviewCount'] if "aggregateRating" in data else 0
		review_rating = data['aggregateRating']['ratingValue'] if "aggregateRating" in data else 0
		address = data['address']['streetAddress'] + ' ' + data['address']['postalCode'] + ' ' + data['address']['addressLocality']

		title = response.css('title::text').extract()
		restaurant_type = title[0]
		restaurant_type = restaurant_type.split("-")
		restaurant_type = restaurant_type[1]

		categoryTitle = response.css('.menucardcategoryheader .menucategorytitle::text').extract()
		categoryTitle = "|".join(categoryTitle)
		productTitle = response.css('.menucardproductname::text').extract()
		productTitle = "|".join(productTitle)
		descTitle = response.css('.menucardproductdescription::text').extract()
		descTitle = "|".join(descTitle)

		yield {
			'name': name,
			'url': url,
			'latitude': latitude,
			'longitude': longitude,
			'telephone': telephone,
			'review_count': review_count,
			'review_rating': review_rating,
			'address': address,
			'restaurant_type': restaurant_type,
			'categoryTitle': categoryTitle,
			'productTitle': productTitle,
			'descTitle': descTitle
		}

