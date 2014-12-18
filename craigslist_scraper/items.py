from scrapy.item import Item, Field

class CraigslistItem(Item):
  title = Field()
  link = Field()
  time = Field()
  location = Field()
  catagory = Field()