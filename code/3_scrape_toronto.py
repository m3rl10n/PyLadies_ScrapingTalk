# example with Toronto news - shell page with data loaded through
# JavaScript - parsing text + json

import requests
import unicodecsv
import time
import json


def parse(item, urlformatnewsitem):
    title = item['txtTitle']
    date = '%s-%s-%s' % (item['dtPubDate']['year'],
                         item['dtPubDate']['month'], item['dtPubDate']['day'])
    url = urlformatnewsitem % item['txtID']
    return (title, date, url)


urlformat = 'http://wx.toronto.ca/inter/it/newsrel.nsf/ag_createNewsRelease\
JSON?openAgent&start=%s&count=%s&_=1463533372174'
urlformatnewsitem = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid\
=af71df79b2df6410VgnVCM10000071d60f89RCRD&nrkey=%s'

start = 1
pagecount = 10
results = []
sleeplvl = 5

while start <= 5 * 10:
    url = urlformat % (start, pagecount)
    print 'requesting url: %s' % url
    request = requests.get(url)
    print 'parsing results...'
    jsontext = request.text.replace('jsonCallBack(', '')[:-4]
    newsitems = json.loads(jsontext)
    parsedresults = \
        [parse(item, urlformatnewsitem) for item in newsitems['Newsroom']]
    print 'extracted %s results' % len(parsedresults)
    results.extend(parsedresults)
    start = start + pagecount
    print 'sleeping for %s seconds' % sleeplvl
    time.sleep(sleeplvl)

print 'completed parsing with %s results' % len(results)

fname = 'toronto_news.csv'
print 'writine results to file: %s' % fname
with open(fname, 'wb') as csvfile:
    csvwriter = unicodecsv.writer(csvfile, encoding='utf-8',
                                  delimiter=',', quotechar='"')
    csvwriter.writerow(('title', 'date', 'url'))
    csvwriter.writerows(results)

print 'writing results complete'
