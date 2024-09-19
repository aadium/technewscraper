# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ArticleItem(Item):
    title = Field()
    category = Field()
    url = Field()
    published_date = Field()
    author = Field()
    content = Field()
    