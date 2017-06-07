# -*- coding: utf-8 -*-
import string
import scrapy
import json

#To run without the pausing feature: scrapy runspider PoliticianFilterSpider.py -o FilteredPoliticians.json
#To run with the pausing feature (inside scrapy project): scrapy crawl PoliticianFilterSpider -s JOBDIR=crawls/PoliticianFilterSpider-1 -o FilteredPoliticians.json

#The purpose of this spider is to filter the list of politicians in 'politicians.json' in order to select the ones more relevant to the crawl.
#The politicians selected will be those who have at least N pages filled with articles. The reasoning behind this criteria is the following:
# 1 - We will filter the politicians who don't have much to add in terms of quantity of articles
# 2 - Since the politicians who have few articles generally only have brief articles on election campaigning

N_PAGINATION = 3
POLITICIANS = {}

class PoliticianFilterSpider(scrapy.Spider):
	name = "PoliticianFilterSpider"

	custom_settings = {'LOG_LEVEL' : 'INFO',
    				   'FEED_EXPORT_ENCODING' : 'utf-8',
				       'FEED_FORMAT':'json'}

	def __init__(self, *args, **kwargs):
		super(PoliticianFilterSpider, self).__init__(*args, **kwargs)

		with open('Politicians.json') as data_file:
			for politician in json.load(data_file):
				paginationPageLink = politician["Page"][:-5]+"/feed/pagina-"+str(N_PAGINATION)+".html"
				self.start_urls.append(paginationPageLink)
				POLITICIANS[paginationPageLink] = politician

	def parse(self, response):

		currentURL = response.url
		if 'redirect_urls' in  response.request.meta:
			currentURL = response.request.meta['redirect_urls'].pop()

		print "Parsing:"+currentURL

		articleLinks = response.xpath("//a[re:test(@class, 'feed-post-link')]/@href").extract()

		# Adds if there are any articles in the pagination webpage of number N_PAGINATION
		if len(articleLinks) > 0:
			return POLITICIANS[currentURL]
