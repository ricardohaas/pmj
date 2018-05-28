import scrapy
import time
import datetime
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess

class UrlSpider(scrapy.Spider):

    name = 'urlspider'

    def __init__(self, start_urls='', *args, **kwargs):
        super(UrlSpider, self).__init__(*args, **kwargs)
        self.start_urls = start_urls

    def parse(self, response):
        for list_page in response.css('.tableDados tr'):
            next_url = list_page.css('a ::attr(href)').extract_first()
            if( next_url is not None and "p=3.6" in next_url):
                #print('next_url:'+next_url)
                yield response.follow(next_url, self.parse_list)

    def parse_list(self, response):
        for list_page in response.css('.tableDados tr'):
            next_url = list_page.css('a ::attr(href)').extract_first()
            if( next_url is not None and "p=3.3.1" in next_url):
                print(next_url)
                #yield response.follow(next_url, self.parse_item)

today = datetime.datetime.now()
base_url = 'https://transparencia.joinville.sc.gov.br/?p=3.5&registros_pagina=500'
start_urls = []
for x in range(0,10):
    cur_date = today + datetime.timedelta(days=-x)
    start_urls.append(base_url + '&inicio=' + cur_date.strftime('%d/%m/%Y')+ '&fim=' + cur_date.strftime('%d/%m/%Y'))
    
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(UrlSpider, start_urls=start_urls)
process.start()
