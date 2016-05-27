# -*- coding: utf-8 -*-
"""
Sketchbot project pipeline.
"""

from scrapy.exceptions import DropItem

class SketchbotPipeline(object):
    """
    Carries out post-scrape logic on items.
    """
    # common image formats
    # would consider something more comprehensive under real circumstances
    image_extensions = {"png", "svg", "jpg", "jpeg", "gif", "tif"}

    def __init__(self):
        """
        """
        self.seen = set()

    def process_item(self, item, spider):
        """
        :param item: An EmailItem yielded by EmailSpider
        :param spider: The spider (EmailSpider)
        :return: processed item (noop in this case), if accepted
        """
        # drop duplicates
        if item['email'] in self.seen:
            raise DropItem("Dropping Duplicate: %s" % item)

        # drop false positives of images with funny names
        if item['email'].split(".")[-1] in self.image_extensions:
            raise DropItem("Dropping Image: %s" % item)

        self.seen.add(item['email'])
        return item
