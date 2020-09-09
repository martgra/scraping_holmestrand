# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class ScrapingHolmestrandPipeline:
    def process_item(self, item, spider):
        print(item)
        #print(item["liste"][1]["Journaldato"])

        # with open(filename, 'a', encoding='utf8') as f:
        #     json.dump(result, f, indent=4, ensure_ascii=False)
        #return item
