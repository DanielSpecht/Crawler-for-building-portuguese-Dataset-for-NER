from scrapy.exceptions import DropItem
import logging

class FaultyArticlePipeline(object):

    def __init__(self):
        self.urls_known = set()
        self.logger = logging.getLogger('FAULTY ITEM')

	#Detects errors in the structure of the article
    def process_item(self, item, sp1ider):

        for key in item.keys():
            if not item[key]:
                self.logger.info('Item without '+key+' in %s', item["URL"])

        if (not item["Text"]) or (not item["Entities"]):
            raise DropItem('Crucial information not found, item droped %s' % item["URL"])

        else:
            return item
