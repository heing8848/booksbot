import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    custom_settings = {
        "CLOSESPIDER_PAGECOUNT": 25,
        "CLOSESPIDER_TIMEOUT": 60,
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 1,
        "DOWNLOAD_TIMEOUT": 10,
        "RETRY_TIMES": 0,
        "ROBOTSTXT_OBEY": True,
        "TELNETCONSOLE_ENABLED": False,
    }

    def parse(self, response):
        for link in response.css("article.product_pod h3 a::attr(href)").getall()[:20]:
            yield response.follow(link, callback=self.parse_book_page)

    def parse_book_page(self, response):
        yield {
            "title": response.css("div.product_main h1::text").get(),
            "category": response.css("ul.breadcrumb li:nth-last-child(2) a::text").get(),
            "description": response.css("#product_description + p::text").get(),
            "price": response.css("div.product_main p.price_color::text").get(),
            "url": response.url,
        }
