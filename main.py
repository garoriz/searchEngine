import urllib.request as urllib2
from bs4 import *
from urllib.parse import urljoin


def crawl(page):
    result_urls = []

    while len(result_urls) < 150:
        try:
            c = urllib2.urlopen(page)
        except:
            print("Could not open %s" % page)
        soup = BeautifulSoup(c.read(), features="html.parser")
        links = soup('a')

        for link in links:
            if 'class' in dict(link.attrs) and link['class'] == ['entry-link']:
                result_urls.append(link['href'])
            if 'class' in dict(link.attrs) and link['class'] == ['next']:
                page = link['href']
    return result_urls


if __name__ == '__main__':
    page = "https://ruitunion.org/posts/"
    urls = crawl(page)
    print(urls)
    print(len(urls))
