import scrapy
from scrapy.spider import Spider

class EkoHomePrice(scrapy.Spider): 
    
    name = 'home'
    
    allowed_domains = 'propertypro.ng'

    start_urls = ['https://www.propertypro.ng/property-for-rent/flat-apartment/?search=lagos&bedroom=&min_price=&max_price=']

    #setting the location of the output csv file
    custom_settings = {
        'FEED_URI' : 'home_price.csv'

    def parse(self, response):

        #Extracting the content using css selectors
        description =  response.css(".listings-property-title::text").extract()
        location =  response.xpath('//div[@class="single-room-text"]/h4/text()').extract()
        feature = response.css(".listings-property-title2::text").extract()
        bedroom = response.xpath('//div[@class="fur-areea"]/span[1]/text()').extract()
        bathroom = response.xpath('//div[@class="fur-areea"]/span[2]/text()').extract()
        toilet =  response.xpath('//div[@class="fur-areea"]/span[3]/text()').extract()
        grade = response.xpath('//div[@class="n50 "]/h4/text()').extract()
        price = response.xpath('//div[@class="n50 "]/h3/span[2]/text()').extract()
       
        #Give the extracted content row wise
        for item in zip(description, location, feature, bedroom, bathroom, toilet, grade, price):
            #create a dictionary to store the scraped info
            scraped_info = {
                'description' : item[0],
                'location' : item[1],
                'feature' : item[2],
                'bedroom' : item[3],
                'bathroom' : item[4],
                'toilet' : item[5],
                'toilet' : item[6],
                'price' : item[7]
            }

            #yield or give the scraped info to scrapy
            yield scraped_info

            NEXT_PAGE_SELECTOR = '.page-link page-active + a::attr(href)'
            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)