# -*- coding: utf-8 -*-
import FaultyArticlePipeline
import string
import scrapy
import json
import re

#To run without the pausing feature: scrapy runspider ArticlesSpider.py -o ArticlesCrawled.json
#To run with the pausing feature (inside scrapy project): scrapy crawl ArticlesSpider -s JOBDIR=crawls/PoliticianFilterSpider-1 -o ArticlesCrawled.json

#The purpose of this spider is to structure and register all the politicians present in the file ArticlesLinks.json

G1_URL = 'http://g1.globo.com'

class Article(scrapy.Item):
	URL = scrapy.Field()
	Title = scrapy.Field()
	Subtitle = scrapy.Field()
	Text = scrapy.Field()
	Entities = scrapy.Field()

class ArticlesSpider(scrapy.Spider):
	name = "ArticlesSpider"

	custom_settings = {'ITEM_PIPELINES': {'FaultyArticlePipeline.FaultyArticlePipeline': 100},
					   'LOG_LEVEL' : 'INFO',
					   'FEED_EXPORT_ENCODING' : 'utf-8',
					   'LOG_FILE' : 'ArticlesSpider.log',
					   'LOG_ENABLED' : 'true',
					   'LOG_ENCODING' : 'utf-8'}

	def __init__(self, *args, **kwargs):
		super(ArticlesSpider, self).__init__(*args, **kwargs)

	 	#Load the articles file for query and to determine which sites will be crawled
		with open('ArticlesLinks.json') as data_file:
			for article in json.load(data_file):
				self.start_urls.append(article["URL"])

	def parse(self, response):
		print "Parsing:"+response.url

		item = Article()
		item["URL"] = response.url
		item["Title"] = self.getTitleOfArticle(response)
		item["Subtitle"] = self.getSubtitleOfArticle(response)
		item["Text"] = self.getTextOfArticle(response)
		item["Entities"] = self.getEntitiesOfArticle(response)

		return item

	def getSubtitleOfArticle(self, response):

		#case 1 - i.e. http://g1.globo.com/bahia/noticia/corpo-achado-em-ilha-de-mare-e-de-jovem-que-sumiu-ao-buscar-bola-no-mar-da-barra-diz-dpt.ghtml
		subtitleCase1 = response.css("h2.content-head__subtitle")
		if len(subtitleCase1)>0:
				return subtitleCase1.xpath('text()').extract_first()

		#case 2 - i.e. http://g1.globo.com/pr/parana/noticia/2017/03/em-dia-cheio-moro-ouve-testemunhas-em-casos-de-lula-palocci-e-cabral.html
		subtitleCase2Container = response.xpath("//div[re:test(@class, 'materia-titulo')]")
		if len(subtitleCase2Container)>0:
			subtitleCase2 = subtitleCase2Container.css("h2")
			if len(subtitleCase2)>0:
				return subtitleCase2.xpath('text()').extract_first()

		return ""

	def getTitleOfArticle(self, response):
		cases = ["h1.content-head__title","h1.entry-title"]

		for case in cases:
			titleContainer = response.css(case)
			if len(titleContainer)>0:
				return titleContainer.xpath('text()').extract_first()

		return ""

	def getTextOfArticle(self, response):
		paragraphs = []

		#case 1 - i.e. http://g1.globo.com/bahia/noticia/corpo-achado-em-ilha-de-mare-e-de-jovem-que-sumiu-ao-buscar-bola-no-mar-da-barra-diz-dpt.ghtml
		cases = ["p.content-text__container theme-color-primary-first-letter","p.content-text__container"]
		for case in cases:
			texts = response.css(case)
			for paragraph in texts:
				paragraphs.append(paragraph.xpath("string()").extract())

		#case 2 - i.e. http://g1.globo.com/pr/parana/noticia/2017/03/em-dia-cheio-moro-ouve-testemunhas-em-casos-de-lula-palocci-e-cabral.html
		textContainer = response.xpath("//div[re:test(@class, 'materia-conteudo entry-content clearfix')]")
		if len(textContainer)>0:
			texts = textContainer.css("p")
			for paragraph in texts:
				paragraphs.append(paragraph.xpath("string()").extract())
		else:
			textContainer = response.xpath("//div[re:test(@id, 'materia-letra')]")
			if len(textContainer)>0:
				texts = textContainer.css("p")
				for paragraph in texts:
					paragraphs.append(paragraph.xpath("string()").extract())

		return paragraphs

	def	getEntitiesOfArticle(self,response):
		entities = list()

		#These are the possibilities of enclosing tags for the entity list for
		cases = ["//div[re:test(@class, 'lista-de-entidades')]","//ul[re:test(@class, 'entities__list')]"]
		for case in cases:
			entitiesContainer = response.xpath(case)
			if len(entitiesContainer)>0:
				for link in entitiesContainer.css('a'):
					entityLink = link.xpath("@href").extract_first()
					entityName = link.xpath("text()").extract_first()

					if G1_URL not in entityLink:
						entityLink = G1_URL+entityLink

					entity =  {"Names":[entityName],"Page":entityLink,"Type":""}
					if not any(entity["Page"]==entityLink  for entity in entities):
						entities.append(entity)

		return entities
