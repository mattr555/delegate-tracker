# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.org/en/latest/topics/items.html

from scrapy import Item, Field

class StateResult(Item):
    state = Field()
    state_abbrev = Field()
    party = Field()
    candidate = Field()
    popular_vote = Field()
    popular_vote_pct = Field()
    pledged_delegates = Field()
    unpledged_delegates = Field()

class StateDate(Item):
    state = Field()
    state_abbrev = Field()
    party = Field()
    date = Field()
    total_pledged = Field()
    total_unpledged = Field()
