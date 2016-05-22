# example with Mississauga news - single html page with all results

import requests
from bs4 import BeautifulSoup
import urlparse
import unicodecsv


def parse(row, base_url):
    _, item = row.select('td')
    link = item.a.extract()
    url = urlparse.urljoin(base_url, link['href'])
    title = link.text.strip()
    date = item.text.strip()
    return (title, date, url)

url = 'http://www.mississauga.ca/portal/cityhall/pressreleases?paf_gear_id=\
9700020&returnUrl=%2Fportal%2Fcityhall%2Fpressreleases'

print 'requesting url: %s' % url
request = requests.get(url)
# TODO: validation that request came back successfully
html = request.text

print 'parsing results...'
soup = BeautifulSoup(html, "lxml")
souprows = soup.select(".blockcontentclear tr")

results = [parse(row, url) for row in souprows]
print 'completed parsing with %s results' % len(results)

fname = 'misssissauga_news.csv'
print 'writine results to file: %s' % fname
with open(fname, 'wb') as csvfile:
    csvwriter = unicodecsv.writer(csvfile, encoding='utf-8',
                                  delimiter=',', quotechar='"')
    csvwriter.writerow(('title', 'date', 'url'))
    csvwriter.writerows(results)

print 'writing results complete'
