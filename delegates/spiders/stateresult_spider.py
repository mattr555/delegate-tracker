import scrapy
from delegates.items import StateResult, StateDate
from itertools import product
import arrow

states = 'AK AL AR AS AZ CA CO CT DA DC DE FL GA GU HI IA ID IL IN KS KY LA MA MD ME MI MN MO MP MS MT NC ND NE NH NJ NM NV NY OH OK OR PA PR RI SC SD TN TX UN UT VA VI VT WA WI WV WY'.split(' ')

class StateSpider(scrapy.Spider):
    name = "state_result"
    allowed_domains = ['thegreenpapers.com']
    start_urls = []

    def start_requests(self):
        for i, j in product(states, ['D', 'R']):
            yield scrapy.Request('http://www.thegreenpapers.com/P16/{}-{}'.format(i, j), self.parse)

    def parse(self, response):
        state = ' '.join(response.css('#namL::text').extract()[0].split(' ')[:-1])
        race = response.url.split('/')[-1].split('-')
        rows = response.xpath("//td[@id='whi']/table/tr")[2:]
        for row in rows:
            candidate = row.xpath('.//a/text()').extract()
            if candidate:
                res = StateResult()
                res['state'] = state
                res['state_abbrev'] = race[0]
                res['party'] = race[1]
                res['candidate'] = candidate[0].split(',')[0]
                pop = [i for i in row.xpath('td[2]/tt/text()').extract()[0].split(u'\xa0') if i]
                if not pop:
                    pop = ['0', '0']
                res['popular_vote'] = pop[0]
                res['popular_vote_pct'] = pop[1]
                res['pledged_delegates'] = row.xpath('td[3]/tt/text()').extract()[0].split(u'\xa0')[0]
                res['unpledged_delegates'] = row.xpath('td[4]/tt/text()').extract()[0].split(u'\xa0')[0]
                if pop[0] == '0' and res['unpledged_delegates'] == '':
                    continue
                yield res

        date = StateDate()
        date['state'] = state
        date['state_abbrev'] = race[0]
        date['party'] = race[1]
        s = response.css('#evtmaj::text').extract()[0].replace(u'\xa0', ' ')
        date['date'] = arrow.get(s, 'D MMMM YYYY').timestamp
        row = rows[-1]
        date['total_pledged'] = row.xpath('td[3]/tt/text()').extract()[0].split(u'\xa0')[0] or '0'
        date['total_unpledged'] = row.xpath('td[4]/tt/text()').extract()[0].split(u'\xa0')[0] or '0'
        yield date
