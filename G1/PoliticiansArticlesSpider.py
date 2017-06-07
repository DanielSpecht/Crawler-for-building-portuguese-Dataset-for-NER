# -*- coding: utf-8 -*-
import DuplicatesURLPipeline
import string
import scrapy
import json
import re

#To run without the pausing feature: scrapy runspider PoliticiansArticlesSpider.py -o ArticlesLinks.json
#To run with the pausing feature (inside scrapy project): scrapy crawl PoliticiansArticlesSpider -s JOBDIR=crawls/PoliticianFilterSpider-1 -o ArticlesLinks.json

#The purpose of this spider is to structure and register all the articles of the politicians in the file FilteredPoliticians.json

POLITICIANS = {}

class Article(scrapy.Item):
	URL = scrapy.Field()

class PoliticiansArticlesSpider(scrapy.Spider):
	name = "PoliticiansArticlesSpider"

	custom_settings = {'ITEM_PIPELINES': {'DuplicatesURLPipeline.DuplicatesURLPipeline': 100},
					   'LOG_LEVEL' : 'INFO',
    				   'FEED_EXPORT_ENCODING' : 'utf-8',
				       'FEED_FORMAT':'json'}

	def __init__(self, *args, **kwargs):
		super(PoliticiansArticlesSpider, self).__init__(*args, **kwargs)

		#For every politician adds the first pagination page to the urls to be parsed
		with open('FilteredPoliticians.json') as data_file:
			for politician in json.load(data_file):
				POLITICIANS[politician["Page"]] = politician
				paginationPageLink = politician["Page"][:-5]+"/feed/pagina-1.html"
				self.start_urls.append(paginationPageLink)

	def parse(self, response):
		currentURL = response.url
		if "redirect_urls" in response.meta:
			currentURL = response.request.meta['redirect_urls'].pop()

		print "Parsing:"+currentURL

		articles = response.xpath("//a[re:test(@class, 'feed-post-link')]/@href").extract()
		#Ends recursion if there are no more articles listed for the politician
		if len(articles) == 0:
			return

		#Structures and register all the articles in the current pagination
		for i in range(0,len(articles)+1):
			if i < len(articles):
				article = Article()
				article["URL"] = articles[i]
				yield article

		#Gets the next pagination page
		currentPaginationNum = int(re.match(r'.*-([0-9]+).html', currentURL).group(1))
		politicianPage = re.match(r'http://g1.globo.com/politica/politico/[^/]*', currentURL).group()+".html"
		nextPaginationPage = POLITICIANS[politicianPage]["Page"][:-5]+"/feed/pagina-"+str(currentPaginationNum+1)+".html"

		request = scrapy.Request(nextPaginationPage,callback=self.parse,dont_filter = True)

		yield request
