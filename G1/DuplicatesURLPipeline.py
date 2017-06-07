from scrapy.exceptions import DropItem

class DuplicatesURLPipeline(object):

    def __init__(self):
        self.urls_known = set()

    def process_item(self, item, spider):
        if item['URL'] in self.urls_known:
            raise DropItem("Duplicate URL found: %s" % item)
        else:
            self.urls_known.add(item['URL'])
            return item
