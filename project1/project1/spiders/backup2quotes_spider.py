from pathlib import Path

import scrapy
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser
from ..items import Project1Item


class QuotesSpider(scrapy.Spider): # Class name can be anything makesure you import the "scrapy.Spider"
    name = "quotes"  # this should be unique
    
    def start_requests(self):    # function name should not change
        urls = [
            "https://quotes.toscrape.com/login",
            # "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):     # function should not change

        token = response.css('form input::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'antompk@gmail.com',
            'password': 'assdasd'
        }, callback = self.start_scraping)
    
    def start_scraping(self, response):
        open_in_browser(response)
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
        
