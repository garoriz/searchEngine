import os
import re

import spacy
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
TOKENS_TXT = 'tokens.txt'


def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext


def remove_btn_text_if_equals(url):
    if 'href' in dict(code_tag.attrs) and code_tag['href'] == url:
        code_tag.extract()


def remove_btn_text_if_contains(url):
    if 'href' in dict(code_tag.attrs) and url in code_tag['href']:
        code_tag.extract()


def remove_next_or_prev_button(class_value):
    if 'class' in dict(code_tag.attrs) and code_tag['class'] == [class_value]:
        code_tag.extract()


def write_tokens():
    for token in no_order:
        with open(TOKENS_TXT, 'a', encoding='utf-8') as tokens_file:
            tokens_file.write(token + "\n")


def add_tokens_to_lemma(lemmas_file, tokens):
    for token in tokens:
        lemmas_file.write(f"{token} ")
    lemmas_file.write("\n")


def write_lemmas_in_txt(lemmas_dict):
    for lemma, tokens in lemmas_dict.items():
        with open('lemmas.txt', 'a', encoding='utf-8') as lemmas_file:
            lemmas_file.write(f"{lemma} ")
            add_tokens_to_lemma(lemmas_file, tokens)


def create_lemmas():
    with open(TOKENS_TXT, 'r', encoding='utf-8') as tokens_file:
        doc = sp(tokens_file.read())

        lemmas_dict = {}

        for token in doc:
            lemma = token.lemma_
            if lemma in lemmas_dict:
                lemmas_dict[lemma].append(token.text)
            else:
                lemmas_dict[lemma] = [token.text]

        lemmas_dict.pop('\n')
        write_lemmas_in_txt(lemmas_dict)


if __name__ == '__main__':
    sp = spacy.load("ru_core_news_sm")
    all_tokens = []

    webpage_index = 0
    while webpage_index <= 155:
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
                remove_next_or_prev_button('next')
                remove_next_or_prev_button('prev')

                codetags = soup.find_all('footer')
            for code_tag in codetags:
                if 'class' in dict(code_tag.attrs) and code_tag['class'] == ['footer']:
                    code_tag.extract()
            clean_txt = soup.text
            clean_txt = re.sub(r"\n", " ", clean_txt)
            clean_txt = re.sub(r"\s+", " ", clean_txt)
            clean_txt = clean_txt.strip()
            word_tokens = word_tokenize(clean_txt)
            filtered_tokens_alpha = [word for word in word_tokens if word.isalpha()]
            stop_words = set(stopwords.words('russian'))
            filtered_tokens = [token for token in filtered_tokens_alpha if token.lower() not in stop_words]
            all_tokens.extend(filtered_tokens)
        webpage_index = webpage_index + 1

    no_order = list(set(all_tokens))
    write_tokens()
    create_lemmas()
