from pathlib import Path
import scrapy
from ..items import AmazonetutorialItem


class AmazonSpiderSpider(scrapy.Spider):
    name = "amazon_spider"
    allowed_domains = ["amazon.com"]
    #start_urls = ["https://www.amazon.in/s?k=books&i=stripbooks&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page=1&crid=150LJ70XOBTBR&qid=1705562243&rnid=2684818031&sprefix=books%2Caps%2C192&ref=sr_pg_1"]
    page_number = 2

        
    def start_requests(self):    # function name should not change
        urls = [
            "https://www.amazon.in/s?k=books&i=stripbooks&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page=1&crid=150LJ70XOBTBR&qid=1705562243&rnid=2684818031&sprefix=books%2Caps%2C192&ref=sr_pg_1",
            # "https://quotes.toscrape.com/page/1/",
            # "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,meta={"proxy": "http://203.192.217.6:8080"})

    def parse(self, response):
        items = AmazonetutorialItem()

        items_list = response.css('.puis-card-border > .a-section > .puisg-row')

        for item in items_list:
            items["product_name"] = item.css('.a-color-base.a-text-normal::text').extract()
            items["product_price"] = item.css('.a-price-whole::text').extract()
            items["product_author"] = item.css('.a-color-secondary .a-row .a-size-base::text').extract()
            items["product_imagelink"] = item.css('.s-image::attr(src)').extract()

            yield items
        print("HEY++++++++++++++++++++=======================>")
        next_page = f'https://www.amazon.in/s?k=books&i=stripbooks&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page={AmazonSpiderSpider.page_number}&crid=150LJ70XOBTBR&qid=1705562243&rnid=2684818031&sprefix=books%2Caps%2C192&ref=sr_pg_{AmazonSpiderSpider.page_number}'
        print(next_page)
        if AmazonSpiderSpider.page_number <= 5:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        
        
