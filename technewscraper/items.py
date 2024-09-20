# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ArticleItem(Item):
    publisher = Field()
    title = Field()
    categories = Field()
    url = Field()
    published_datetime = Field()
    author = Field()
    summary = Field()
    