# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scraping_holmestrand import items
from itemadapter import ItemAdapter
import json
from datetime import datetime

scrapy_items = []

def update_json(json_list):
    for i in json_list:
        if "Avsender(e)" not in i:
            try:
                brev_dato = i["Brevdato"]
                arkiv_sak = i["Arkivsak"]
                i["Brevdato"] = arkiv_sak
                i["Arkivsak"] = brev_dato
            except Exception:
                print(i)

class ScrapingHolmestrandPipeline:
    def process_item(self, item, spider):      
        scrapy_items.extend(item["body"])
        return "processed"

    def close_spider(self, spider):
        date = datetime.strptime(scrapy_items[0]["Journaldato"], "%d.%m.%Y")
        update_json(scrapy_items)
        with open("scraping_reports/{}_innsyn.json".format(date.date().strftime("%Y-%m-%d")), 'w', encoding='utf8') as f:
            json.dump(scrapy_items, f, indent=4, ensure_ascii=False)