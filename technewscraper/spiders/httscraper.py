import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from technewscraper.items import ArticleItem

class HTTechScraper(CrawlSpider):
    name = "httscraper"
    start_urls = ["https://tech.hindustantimes.com/"]

    rules = (
        Rule(LinkExtractor(allow=[r'https://tech.hindustantimes.com/[a-z]+/[a-z]+/[a-z0-9-]+/$']), 
             callback="parse_article", follow=True),
    )

    def parse_article(self, response):
        article_item = ArticleItem()

        article_item["url"] = response.url
        article_item["publisher"] = "HT Tech"
        article_item["title"] = response.css(".storyContent h1::text").get().strip()
        category_match = re.search(r'https://tech.hindustantimes.com/([^/]+)/', response.url)
        categories = []
        if category_match:
            category = category_match.group(1)
            categories.append(category.replace('-', ' ').title())
        article_item["categories"] = categories
        article_item["author"] = response.css(".name::text").get().strip()
        article_item["published_datetime"] = response.css(".date").get()
        article_item["summary"] = response.css(".htStoryDetail p").get()

        return article_item
    