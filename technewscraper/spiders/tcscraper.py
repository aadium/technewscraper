from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class TechCrunchScraper(CrawlSpider):
    name = "tcscraper"
    start_urls = ["https://techcrunch.com/"]

    rules = (
        Rule(LinkExtractor(allow=r'/\d{4}/\d{2}/\d{2}/'), callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["title"] = response.css(".wp-block-post-title::text").get().strip()
        article_item["category"] = response.css(".is-taxonomy-category::text").get().strip()
        article_item["author"] = response.css(".wp-block-tc23-author-card-name a::text").get().strip()
        article_item["published_date"] = response.css(".wp-block-post-date time::attr(datetime)").get()
        article_item["content"] = response.css(".wp-block-post-content").get().strip()

        return article_item
    