from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem
from datetime import datetime, timedelta
from dateutil import parser
import pytz

class TechEuScraper(CrawlSpider):
    name = "teuscraper"
    start_urls = ["https://tech.eu/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://tech.eu/\d{4}/\d{2}/\d{2}/']), callback="parse_article", follow=True),
    )
    

    def parse_article(self, response):
        def convert_date(inpDateTime):
            if "ago" in inpDateTime:
                time_parts = inpDateTime.split()
                hours_ago = int(time_parts[0])
                new_datetime = datetime.now() - timedelta(hours=hours_ago)
            else:
                new_datetime = parser.parse(inpDateTime)
            new_datetime = new_datetime.astimezone(pytz.UTC)
            return new_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "Tech.eu"
        article_item["title"] = response.css(".single-post-title::text").get().strip()
        category = response.css(".single-post-category a::attr(title)").get().strip()
        categories = []
        categories.append(category)
        article_item["categories"] = categories
        article_item["author"] = response.css(".single-post-meta-text strong::text").get().strip()
        inpDateTime = response.css(".sp-date::text").get()
        article_item["published_datetime"] = convert_date(inpDateTime)
        article_item["summary"] = response.css(".single-post-content p").get()

        return article_item
    