# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scraping_holmestrand import items
from itemadapter import ItemAdapter
import json

scrapy_items = []

class ScrapingHolmestrandPipeline:
    def process_item(self, item, spider):
        scrapy_items.extend(item["body"])
        return "processed"

    def close_spider(self, spider):
        date = scrapy_items[0]["Journaldato"]
        with open("{}_innsyn.json".format(date), 'w', encoding='utf8') as f:
            json.dump(scrapy_items, f, indent=4, ensure_ascii=False)