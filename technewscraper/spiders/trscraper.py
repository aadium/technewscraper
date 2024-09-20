from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class TechRadarScraper(CrawlSpider):
    name = "trscraper"
    start_urls = ["https://www.techradar.com/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://www.techradar.com/[a-z]+/[a-z0-9-]+/'], deny=[r'/tag/', r'/page/', r'/category/', r'/author/']), 
             callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "TechRadar"
        article_item["title"] = response.css(".news-article h1::text").get().strip()
        categories = response.css("nav.breadcrumb a::text").getall()
        article_item["categories"] = [category.strip() for category in categories if category.strip()]
        article_item["author"] = response.css(".author-byline__link::text").get().strip()
        article_item["published_datetime"] = response.css(".relative-date::attr(datetime)").get()
        article_item["summary"] = response.css(".bodyCopy p").get()

        return article_item
    