import scrapy
import json
import scrapy_splash
from scrapy_splash import SplashRequest


def parse_list(li):
    return_list = []
    for i in li:
        typer = i.css("span::text").getall()
        verdi = i.css("strong::text").getall()
        verdi.insert(2,i.css("a.col-md-10::text").get())
        verdi = [" ".join(i.split()) for i in verdi]
        typer = [i.split()[0] for i in typer]
        result = dict(zip(typer, verdi))
        result["Tema"] = " ".join(i.css("a.content-link::text").get().split())
        return_list.append(result)
    return return_list

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = ["https://holmestrand.kommune.no/innsyn.aspx?response=journalpost_postliste&MId1=307&scripturi=/innsyn.aspx&skin=infolink&fradato=2020-08-31T00:00:00"]
        for url in urls:
            yield SplashRequest(url, self.parse,
    args={
        # optional; parameters passed to Splash HTTP API
        'wait': 5

        # 'url' is prefilled from request url
        # 'http_method' is set to 'POST' for POST requests
        # 'body' is set to request body for POST requests
    },
    #endpoint='render.json', # optional; default is render.html
    #splash_url='<url>',     # optional; overrides SPLASH_URL
    #slot_policy=scrapy_splash.SlotPolicy.PER_DOMAIN,  # optional
)

    def parse(self, response):
        page = response.url.split("/")[-2]
        result = parse_list(response.css("li.i-jp"))
        
        filename = 'postliste-%s.json' % page
        with open(filename, 'w', encoding='utf8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        self.log('Saved file %s' % filename)