# -*- coding: utf-8 -*-
import scrapy
import string
import sys

#To run without the pausing feature: scrapy runspider PoliticiansSpider.py -o Politicians.json
#To run with the pausing feature (inside scrapy project): scrapy crawl PoliticiansSpider -s JOBDIR=crawls/PoliticianFilterSpider-1 -o Politicians.json

#The purpose of this spider is to structure and register all the politicians present in the index page: http://g1.globo.com/politica/politicos/indice/

G1_URL = 'http://g1.globo.com'

class PoliticianItem(scrapy.Item):
	ShortName = scrapy.Field()
	FullName = scrapy.Field()
	Page = scrapy.Field()

class PoliticiansSpider(scrapy.Spider):
	name = "PoliticiansSpider"

	custom_settings = {'LOG_LEVEL' : 'INFO',
    				   'FEED_EXPORT_ENCODING' : 'utf-8',
				       'FEED_FORMAT':'json'}

	def __init__(self, *args, **kwargs):
		super(PoliticiansSpider, self).__init__(*args, **kwargs)

		indexPage = G1_URL+"/politica/politicos/indice/"
		alphabet = list(string.ascii_lowercase)

		#Adds all the pages of the politician index (i.e. http://g1.globo.com/politica/politicos/indice/a.html)
		map(lambda x: self.start_urls.append(indexPage+x+".html"), alphabet)

	def parse(self, response):

		print "Parsing:"+response.url

		for politician_page in response.xpath("//a[re:test(@class, 'glb-index-item glb-index-item-link gui-color-primary-link')]"):

			politician = PoliticianItem()

			#Link for the politician page (i.e. http://g1.globo.com/politica/politico/lula.html)
			politician["Page"] = G1_URL+politician_page.xpath('@href').extract_first()
			politician["ShortName"] = politician_page.xpath(".//span[re:test(@class, 'glb-index-item-title')]/text()").extract_first()
			politician["FullName"] = politician_page.xpath(".//span[re:test(@class, 'glb-index-item-posttitle')]/text()").extract_first()

			yield politician
