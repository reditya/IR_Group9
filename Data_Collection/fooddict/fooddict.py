from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
a=[]
from aqaq.items import aqaq
import os
class aqaqspider(BaseSpider):
    name = "aqaq"
    allowed_domains = ["aqaq.com"]
    start_urls = [
                        "http://www.aqaq.com/list/female/view-all?limit=all"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites=hxs.select('//ul[@class="list"]/li')
        for site in sites:
                name=site.select('a[@class="product-name"]/@href').extract()
                a.append(name)
        f=open("url","w+")
        for i in a:
                if str(i)=='[]':
                        pass;
                else:
                        f.write(str(i)[3:-2]+os.linesep)
                        yield Request(str(i)[3:-2].rstrip('\n'),callback=self.parsed)

        f.close()
    def parsed(self,response):
        hxs = HtmlXPathSelector(response)
        sites=hxs.select('//div[@class="form"]')
        items=[]
        for site in sites:
                item=aqaq()
                item['title']=site.select('h1/text()').extract()
                item['cost']=site.select('div[@class="price-container"]/span[@class="regular-price"]/span[@class="price"]/text()').extract()
                item['desc']=site.select('div[@class="row-block"]/p/text()').extract()
                item['color']=site.select('div[@id="colours"]/ul/li/a/img/@src').extract()
                items.append(item)
                return items