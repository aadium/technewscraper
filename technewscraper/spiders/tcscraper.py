from technewscraper.items import ArticleItem
from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class TechCrunchScraper(CrawlSpider):
    name = "tcscraper"
    start_urls = ["https://techcrunch.com/"]

    today = datetime.now()
    allow_patterns = []

    # Generate allow patterns for the last three days
    for i in range(1):
        previous_date = today - timedelta(days=i)
        year = previous_date.year
        month = previous_date.month
        day = previous_date.day
        allow_patterns.append(rf'https://techcrunch.com/{year}/{month:02d}/{day:02d}/')

    rules = (
        Rule(LinkExtractor(allow=allow_patterns, deny=[r'/page/']), callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "TechCrunch"
        article_item["title"] = response.css(".wp-block-post-title::text").get().strip()
        category = response.css(".is-taxonomy-category::text").get().strip()
        categories = []
        categories.append(category)
        article_item["categories"] = categories
        article_item["author"] = response.css(".wp-block-tc23-author-card-name a::text").get().strip()
        article_item["published_datetime"] = response.css(".wp-block-post-date time::attr(datetime)").get()
        article_item["summary"] = response.xpath("normalize-space(//p[@id='speakable-summary'])").get()

        return article_item