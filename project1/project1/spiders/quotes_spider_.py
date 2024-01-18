from pathlib import Path

import scrapy
from ..items import Project1Item


class QuotesSpider(scrapy.Spider): # Class name can be anything makesure you import the "scrapy.Spider"
    name = "quotes"  # tis should be unique
    page_number = 2
    def start_requests(self):    # function name should not change
        urls = [
            "https://quotes.toscrape.com/",
            # "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(   url=url, 
                                    callback=self.parse,
                                    meta={"proxy": "http://203.192.217.6:8080"},
                                    )

    def parse(self, response):     # function should not change

        items = Project1Item() 
        all_div_quotes = response.css('div.quote')

        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()

            # make sure the key name must mach with the varable defined in items.py file
            items['title'] = title
            items['author'] = author
            items ['tag'] = tag

            yield items

        next_page = f'https://quotes.toscrape.com/page/{QuotesSpider.page_number}/'
        
        if QuotesSpider.page_number <= 11:
            QuotesSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)
        
        '''
        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
        '''