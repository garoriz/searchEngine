import os
import xml

import nltk
import re
import spacy
from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def remove_btn_text_if_equals(url):
    if 'href' in dict(code_tag.attrs) and code_tag['href'] == url:
        code_tag.extract()


def remove_btn_text_if_contains(url):
    if 'href' in dict(code_tag.attrs) and url in code_tag['href']:
        code_tag.extract()


if __name__ == '__main__':
    sp = spacy.load('en_core_web_sm')

    webpage_index = 0
    while webpage_index <= 0:
        with open(os.path.join("webpages", str(webpage_index) + '.html'), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), "lxml")

            codetags = soup.find_all('a')
            for code_tag in codetags:
                remove_btn_text_if_equals('https://ruitunion.org/en/')
                remove_btn_text_if_equals('https://ruitunion.org/uk/')
                remove_btn_text_if_equals('https://ruitunion.org/')
                remove_btn_text_if_equals('https://ruitunion.org/news/')
                remove_btn_text_if_equals('https://ruitunion.org/posts/')
                remove_btn_text_if_equals('https://ruitunion.org/about/')
                remove_btn_text_if_equals('https://ruitunion.org/materials/')
                remove_btn_text_if_equals('https://ruitunion.org/archives/')
                remove_btn_text_if_equals('https://ruitunion.org/search/')
                remove_btn_text_if_equals('https://t.me/itunion_feedback_bot')
                remove_btn_text_if_equals('https://t.me/+0KToPESuk4s3NmJi')
                remove_btn_text_if_contains('https://ruitunion.org/tags/')
                remove_btn_text_if_contains('https://gitlab.com/itunion/site/-/tree/main/content/posts/')

            clean_txt = soup.text
            clean_txt = re.sub(r"\n", " ", clean_txt)
            clean_txt = re.sub(r"\s+", " ", clean_txt)
            # clean_txt = cleanhtml(clean_txt)
            clean_txt = clean_txt.strip()

            print(clean_txt)

        webpage_index = webpage_index + 1
