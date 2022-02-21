import scrapy


class ToScrapeXPath(scrapy.Spider):
    name = 'toscrape-xpath'

    def start_requests(self):
        url = 'https://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract(),
                'author': quote.xpath('./span/small[@class="author"]/text()').extract(),
                'tags': quote.xpath('./div[@class="tags"]/a/text()').extract()
            }

        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
