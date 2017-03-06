import scrapy
import re

class AllrecipesSpider(scrapy.Spider):
	name = "Allrecipes"
	# TODO : iterate over url_list.txt for all links
	# This is just an example of scraping brood pages with max 38 page recipes
	base_url = "http://allrecipes.nl/recepten/brood-recepten.aspx?page="
	max_page = 38
	page_list = range(1,max_page)
	start_urls = []
	for i in page_list:
		start_urls.append(base_url + str(i))

	# Entry point for spider
	def parse(self, response):
		for href in response.css('.col-sm-7 a::attr(href)'):
			url = href.extract()
			yield scrapy.Request(url, callback=self.parse_item)

	# parse the output
	def parse_item(self, response):
		title = response.css('.recipeSummary__title2 span::text').extract()[0]
		ingredients = response.css('.recipeIngredients li span::text').extract()
		star_rating = response.css('.recipeStats .starRating .mediumStar').extract()
		count_rating = response.css('.recipeSummaryRatingCount::text').extract()
		preparation_time = response.css('span:nth-child(1) .accent::text').extract()
		finish_time = response.css('#reviewsLink~ tr+ tr .accent::text').extract()
		image_link = response.css('.active .xlargeImg::attr(src)').extract()
		step_by_step = response.css('.recipeDirections li span::text').extract()

		ingredients_list = "|".join(ingredients)
		step_list = "|".join(step_by_step)

		yield {
			'Title': title,
			'Ingredients': ingredients_list,
			'Rating': star_rating,
			'Count Rating': count_rating,
			'Preparation Time': preparation_time, 
			'Finish Time': finish_time,
			'Image Link': image_link,
			'Step by step': step_list
		}

