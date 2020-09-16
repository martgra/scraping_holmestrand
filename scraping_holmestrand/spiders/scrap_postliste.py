import scrapy
import json
import scrapy_splash
from scrapy_splash import SplashRequest
from scrapy.exceptions import CloseSpider
import datetime
from scraping_holmestrand.items import ScrapingHolmestrandItem
import os

def _remove_colon(string_item):
    return string_item.replace(":","")
    


def parse_list(li):
    return_list = []
    for i in li:
        typer = i.css("span::text").getall()
        typer = list(map(_remove_colon, typer))
        verdi = i.css("strong::text").getall()
        verdi.insert(2,i.css("a.col-md-10::text").get())
        verdi = [" ".join(i.split()) for i in verdi]
        typer = [i.split()[0] for i in typer]
        result = dict(zip(typer, verdi))
        result["Tema"] = " ".join(i.css("a.content-link::text").get().split())
        return_list.append(result)
    return return_list

class InnsynsSpider(scrapy.Spider):
    name = "innsyn"
    def __init__(self, *args, **kwargs): 
        super(InnsynsSpider, self).__init__(*args, **kwargs) 
        if kwargs.get('start_url'):
            self.urls = [kwargs.get('start_url')] 
        else:
            self.urls = ["https://holmestrand.kommune.no/innsyn.aspx?response=journalpost_postliste&MId1=307&scripturi=/innsyn.aspx&skin=infolink&fradato={}T00:00:00".format(datetime.datetime.today().date())]


    def start_requests(self):
        # --urls = ["https://holmestrand.kommune.no/innsyn.aspx?response=journalpost_postliste&MId1=307&scripturi=/innsyn.aspx&skin=infolink&fradato={}T00:00:00".format(datetime.datetime.today().date())]
        for url in self.urls:
            yield SplashRequest(url, self.parse,
    args={
        # optional; parameters passed to Splash HTTP API
        'wait': 1
    },
)



    def parse(self, response):
        next_link = response.xpath("//a[text() = 'neste']")
        date = datetime.datetime.strptime(response.url.split("=")[5].split()[0].split("T")[0], '%Y-%m-%d') - datetime.timedelta(days=1)
        if "Det er ikke journalført noen dokument" in response.css("ul.i-jp").get():
            yield SplashRequest("https://holmestrand.kommune.no/innsyn.aspx?response=journalpost_postliste&MId1=307&scripturi=/innsyn.aspx&skin=infolink&fradato={}T00:00:00".format(date.date()), self.parse,
            args={
                # optional; parameters passed to Splash HTTP API
                'wait': 1
            },
        )
        else:
            page = response.url.split("/")[-2]
            result = parse_list(response.css("li.i-jp"))
            if result:
                item = ScrapingHolmestrandItem()
                item["body"] = result
                yield item
            if next_link.get():
                yield SplashRequest("https://holmestrand.kommune.no{}".format(next_link.css("::attr(href)").get()), self.parse,
                args={
                    # optional; parameters passed to Splash HTTP API
                    'wait': 1
                },
            )
                            
            else:
                if str(date.date()) not in [i.split("_")[0] for i in sorted(os.listdir("scraping_reports"))[-3:]]:     
                    # TODO: possible implementation of rescraping last three entries
                    print("CONTINUE")
                else:
                    print("END OF DAY")

