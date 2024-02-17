import urllib.request as urllib2

from bs4 import *
import requests
import os


directory = "webpages"


def save_page(url, webpage_index):
    r = requests.get(url)
    with open(os.path.join(directory, str(webpage_index) + '.html'), 'w', encoding='utf-8') as file:
        file.write(r.content.decode())


def write_in_index(webpage_index, href):
    with open('index.txt', 'a', encoding='utf-8') as file:
        file.write(webpage_index + " " + href + " \n")


def crawl(page):
    os.mkdir(directory)

    webpage_index = 0
    while webpage_index < 150:
        try:
            c = urllib2.urlopen(page)
        except:
            print("Could not open %s" % page)
        soup = BeautifulSoup(c.read(), features="html.parser")
        links = soup('a')

        for link in links:
            if 'class' in dict(link.attrs) and link['class'] == ['entry-link']:
                href = link['href']
                save_page(href, webpage_index)
                write_in_index(str(webpage_index), href)
                webpage_index = webpage_index + 1
            if 'class' in dict(link.attrs) and link['class'] == ['next']:
                page = link['href']


if __name__ == '__main__':
    page = "https://ruitunion.org/posts/"
    crawl(page)
