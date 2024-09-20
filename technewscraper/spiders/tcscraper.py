from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class TechCrunchScraper(CrawlSpider):
    name = "tcscraper"
    start_urls = ["https://techcrunch.com/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://techcrunch.com/\d{4}/\d{2}/\d{2}/'], deny=[r'/page/']), callback="parse_article", follow=True),
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
        article_item["summary"] = response.css("#speakable-summary").get()

        return article_item
    