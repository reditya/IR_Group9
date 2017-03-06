import scrapy
import re

class AllrecipesSpider(scrapy.Spider):
	name = "Allrecipes"
	start_urls = ["http://allrecipes.nl/recepten/salades-recepten.aspx?page=9"]

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

