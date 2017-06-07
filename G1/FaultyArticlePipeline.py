from scrapy.exceptions import DropItem
import logging

class FaultyArticlePipeline(object):

    def __init__(self):
        self.urls_known = set()
        self.logger = logging.getLogger('FAULTY ITEM')

	#Detects errors in the structure of the article
    def process_item(self, item, sp1ider):
        faultyItemFlag = False

        for key in  item.keys():
            if not item[key]:
                faultyItemFlag = False
                self.logger.info('Item without '+key+' in %s', response.url)

        if faultyItemFlag:
            raise DropItem("Faulty item found: %s" % item)
