import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class VentureBeatScraper(CrawlSpider):
    name = "vbscraper"
    start_urls = ["https://venturebeat.com/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://venturebeat\.com/[a-z]+/[a-z0-9-]+/$'], deny=[r'/tag/', r'/page/', r'/category/', r'/author/']), 
             callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "VentureBeat"
        article_item["title"] = response.css(".Article__header-top h1::text").get().strip()
        category_match = re.search(r'https://venturebeat\.com/([^/]+)/', response.url)
        categories = []
        if category_match:
            category = category_match.group(1)
            if category == 'ai':
                categories.append('AI')
            else:
                categories.append(category.replace('-', ' ').title())
        article_item["categories"] = categories
        article_item["author"] = response.css(".Article__author-info a::text").get().strip()
        article_item["published_datetime"] = response.css(".article-time-container time::attr(datetime)").get()
        article_item["summary"] = response.css(".article-content p:first-child").get()

        return article_item
    