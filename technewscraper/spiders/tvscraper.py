import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class TheVergeScraper(CrawlSpider):
    name = "tvscraper"
    start_urls = ["https://www.theverge.com/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://www.theverge.com/202[3-9]/']), 
             callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "The Verge"
        article_item["title"] = response.css(".text-45::text").get().strip()
        categories = response.css("li.font-polysans-mono a::text").getall()
        article_item["categories"] = [category.strip() for category in categories if category.strip()]
        article_item["author"] = response.css("span.font-medium a::text").get().strip()
        article_item["published_datetime"] = response.css(".duet--article--timestamp::attr(datetime)").get()
        article_item["summary"] = response.xpath("normalize-space(//div[contains(@class, 'duet--article--article-body-component')]//p)").get()

        return article_item
    