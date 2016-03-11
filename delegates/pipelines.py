# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from delegates.items import StateResult, StateDate

class NumberifyPipeline(object):
    def process_item(self, item, spider):
        if type(item) is StateDate:
            item['total_pledged'] = int(item['total_pledged'])
            item['total_unpledged'] = int(item['total_unpledged'])
            return item
        for i in ('pledged_delegates', 'unpledged_delegates', 'popular_vote'):
            if not item[i]:
                item[i] = '0'
            item[i] = int(item[i].replace(',', ''))
        item['popular_vote_pct'] = float(item['popular_vote_pct'].replace('%', '') + '0')
        return item

class CandidateFilterPipeline(object):
    to_filter = ['Sanders', 'Clinton', 'Trump', 'Cruz', 'Kasich', 'Rubio']
    def process_item(self, item, spider):
        if type(item) is not StateResult or item['candidate'] in self.to_filter:
            return item

class JsonPipeline(object):
    def __init__(self):
        self.output = {}

    def process_item(self, item, spider):
        if not item:
            return
        if not self.output.get(item['state_abbrev']):
            self.output[item['state_abbrev']] = {'name': item['state']}
        st = self.output[item['state_abbrev']]
        if not st.get(item['party']):
            st[item['party']] = {'results': []}

        if type(item) is StateResult:
            i = dict(item)
            del i['state_abbrev']
            del i['state']
            del i['party']
            st[item['party']]['results'].append(i)

        elif type(item) is StateDate:
            st[item['party']]['date'] = item['date']
            st[item['party']]['total_pledged'] = item['total_pledged']
            st[item['party']]['total_unpledged'] = item['total_unpledged']
        return item

    def close_spider(self, spider):
        with open('output.json', 'w') as f:
            json.dump(self.output, f)

class TotalResultPipeline(object):
    def __init__(self):
        self.output = {'D': {}, 'R': {}}

    def process_item(self, item, spider):
        if not item:
            return item
        if type(item) is StateDate:
            p = item['party']
            if not self.output[p].get('total'):
                self.output[p]['total'] = {'pledged': 0, 'unpledged': 0}
            self.output[p]['total']['pledged'] += item['total_pledged']
            self.output[p]['total']['unpledged'] += item['total_unpledged']
            return item
        p = item['party']
        c = item['candidate']
        if not self.output[p].get(c):
            self.output[p][c] = {'pledged': 0, 'unpledged': 0, 'popular': 0}
        self.output[p][c]['pledged'] += item['pledged_delegates']
        self.output[p][c]['unpledged'] += item['unpledged_delegates']
        self.output[p][c]['popular'] += item['popular_vote']
        return item

    def close_spider(self, spider):
        with open('totals.json', 'w') as f:
            json.dump(self.output, f)
