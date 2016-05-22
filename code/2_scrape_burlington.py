# example with Burlington news - data all on multiple pages
# strictly need to reload pages

import requests
from bs4 import BeautifulSoup
import urlparse
import unicodecsv
import time


def parse(item, base_url):
    title = item.a.text.strip()
    url = urlparse.urljoin(base_url, item.a['href'])
    date = item.select('.newsItem_PostedDate')[0].text
    date = date.replace('Posted ', '').strip()
    return (title, date, url)


urlformat = 'https://www.burlington.ca/en/Modules/News/search.aspx?feedId=\
0b11ae3a-b049-4262-8ca4-762062555538&page=%s'

results = []
page = 1
sleeplvl = 5
while page <= 5:
    url = urlformat % page
    print 'requesting url: %s' % url
    request = requests.get(url)
    html = request.text
    print 'parsing results...'
    soup = BeautifulSoup(html, "lxml")
    soupitems = soup.select('.newsItem')
    parsedresults = [parse(row, url) for row in soupitems]
    print 'extracted %s results' % len(parsedresults)
    results.extend(parsedresults)
    page = page + 1
    print 'sleeping for %s seconds' % sleeplvl
    time.sleep(sleeplvl)

print 'completed parsing with %s results' % len(results)

fname = 'burlington_news.csv'
print 'writine results to file: %s' % fname
with open(fname, 'wb') as csvfile:
    csvwriter = unicodecsv.writer(csvfile, encoding='utf-8',
                                  delimiter=',', quotechar='"')
    csvwriter.writerow(('title', 'date', 'url'))
    csvwriter.writerows(results)

print 'writing results complete'
