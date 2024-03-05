import os
import re

import spacy
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords


def remove_btn_text_if_equals(url):
    if 'href' in dict(code_tag.attrs) and code_tag['href'] == url:
        code_tag.extract()


def remove_btn_text_if_contains(url):
    if 'href' in dict(code_tag.attrs) and url in code_tag['href']:
        code_tag.extract()


def remove_next_or_prev_button(class_value):
    if 'class' in dict(code_tag.attrs) and code_tag['class'] == [class_value]:
        code_tag.extract()


def get_word_frequency_dictionary():
    word_count = {}
    for word in all_tokens:
        if word not in word_count:
            word_count[word] = 1
        elif word in word_count:
            word_count[word] += 1
    return word_count


def set_idf_dictionaries():
    idf = {}
    count_of_webpages = 156

    for w in word_frequency_dictionaries:
        k = 0

        for i in range(count_of_webpages):
            if w in corpus[i].split():
                k += 1

        idf[w] = np.log10(n_docs / k)

        print(f'{w:>15}: {idf[w]:>10}')


if __name__ == '__main__':
    sp = spacy.load("ru_core_news_sm")

    webpage_index = 0
    word_frequency_dictionaries = []
    idf_dictionaries = []
    while webpage_index <= 155:
        all_tokens = []
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
            clean_txt = clean_txt.lower()
            clean_txt = clean_txt.strip()
            word_tokens = word_tokenize(clean_txt)
            filtered_tokens_alpha = [word for word in word_tokens if word.isalpha()]
            stop_words = set(stopwords.words('russian'))
            filtered_tokens = [token for token in filtered_tokens_alpha if token.lower() not in stop_words]
            all_tokens.extend(filtered_tokens)

            word_frequency_dictionaries.append(get_word_frequency_dictionary())
        webpage_index = webpage_index + 1

    set_idf_dictionaries()
