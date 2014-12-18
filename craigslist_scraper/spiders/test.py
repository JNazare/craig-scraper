from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist_scraper.items import CraigslistItem
import re
import datetime

class MySpider(CrawlSpider):
    name = "craigs"
    allowed_domains = ["boston.craigslist.org"]
    start_urls = ["http://boston.craigslist.org/jjj/"]
    download_delay = 1
    rules = (Rule (SgmlLinkExtractor(allow=("/search/jjj?", ),restrict_xpaths=('//a[@class="button next"]',))
    , callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        current_date = datetime.date.today()
        hxs = HtmlXPathSelector(response)
        titles = hxs.select("//span[@class='pl']")
        labels = hxs.select("//span[@class='pnr']")
        catagories = hxs.select("//span[@class='l2']")
        items = []
        for i in range(len(titles)):
            item = CraigslistItem()
            title = titles[i]
            item ["title"] = title.select("a/text()").extract()
            item ["link"] = title.select("a/@href").extract()
            item ["time"] = title.select("time/@datetime").extract()

            listing_date = str(item["time"][0]).split(" ")[0].split("-")
            listing_date = datetime.date(year=int(listing_date[0]), month=int(listing_date[1]), day=int(listing_date[2]))
            print current_date
            print listing_date
            if listing_date < current_date:
                break
            label = labels[i] 
            item ["location"] = label.select("small/text()").extract()
            if item ["location"]:
                item ["location"] = re.sub("[(),]", "", item ["location"][0].strip())
            catagory = catagories[i]
            item ["catagory"] = catagory.select("a/text()").extract()
            items.append(item)
        return items