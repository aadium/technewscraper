import dateutil.parser
import pytz
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem
from datetime import datetime, timedelta

class TechEUScraper(CrawlSpider):
    name = "teuscraper"
    start_urls = ["https://tech.eu/"]

    today = datetime.now()
    allow_patterns = []

    # Generate allow patterns for the last three days
    for i in range(1):
        previous_date = today - timedelta(days=i)
        year = previous_date.year
        month = previous_date.month
        day = previous_date.day
        allow_patterns.append(rf'https://tech.eu/{year}/{month:02d}/{day:02d}/')

    # Print the allow patterns for debugging
    print("Allow patterns:", allow_patterns)

    rules = (
        Rule(LinkExtractor(allow=allow_patterns), callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        def convert_date(inpDateTime):
            if "ago" in inpDateTime:
                time_parts = inpDateTime.split()
                hours_ago = int(time_parts[0])
                new_datetime = datetime.now() - timedelta(hours=hours_ago)
            else:
                new_datetime = dateutil.parser.parse(inpDateTime)
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
        article_item["summary"] = response.xpath("normalize-space(//div[@class='single-post-content']//p)").get()

        return article_item