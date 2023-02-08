import scrapy
import re
import ast

class LamudiSpider(scrapy.Spider):
    name = 'lamudi'
    start_urls = [
        'https://www.lamudi.com.ph/buy'
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        listings = response.xpath('//div[contains(@class,"ListingCell-content")]')
        print('listings', listings)
        for listing in listings:
            price = listing.xpath('.//div[contains(@class,"ListingCell-AllInfo")]/@data-price').get()
            geopoint = listing.xpath('.//div[contains(@class,"ListingCell-AllInfo")]/@data-geo-point').get()
            href = listing.xpath('.//a[@class="js-listing-link"]/@href').get()
            title = listing.xpath('.//a[@class="js-listing-link"]/@title').get()
            yield {'price': price, 'link': href, 'title': self.sanitize(title), 'geopoint': ast.literal_eval(geopoint) }

    def sanitize(self, str):
        str = re.sub('\n+', '\n', str)
        str = re.sub('\s+$', '', str)
        return str
        

