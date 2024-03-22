import os
import re

import numpy as np
import spacy
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

COUNT_OF_WEBPAGES = 156
DIRECTORY_TF_IDF = "tf_idf"
TOKENS = "tokens"
LEMMAS = "lemmas"


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


def get_count_of_docs_contains_word(word):
    count_of_docs_contains_word = 0
    for i in range(COUNT_OF_WEBPAGES):
        if word in word_frequency_dictionaries[i]:
            count_of_docs_contains_word += 1
    return count_of_docs_contains_word


def create_lemma_frequency_dictionaries():
    for i in range(COUNT_OF_WEBPAGES):
        lemma_count = {}
        for line_in_lemmas in all_lemmas:
            count_of_lemmas = 0
            for lemma in line_in_lemmas:
                if lemma in word_frequency_dictionaries[i]:
                    count_of_lemmas += word_frequency_dictionaries[i][lemma]
            if count_of_lemmas != 0:
                lemma_count[line_in_lemmas[0]] = count_of_lemmas
        lemma_frequency_dictionaries.append(lemma_count)


def get_count_of_docs_contains_lemma(lemma):
    count_of_docs_contains_lemma = 0
    for i in range(COUNT_OF_WEBPAGES):
        if lemma in lemma_frequency_dictionaries[i]:
            count_of_docs_contains_lemma += 1
    return count_of_docs_contains_lemma


def compute_tf_idf_for_words():
    for i in range(COUNT_OF_WEBPAGES):
        with open(os.path.join(DIRECTORY_TF_IDF, TOKENS, "tokens" + str(i) + ".txt"), 'a', encoding='utf-8') as tokens_file:
            for word, frequency in word_frequency_dictionaries[i].items():
                tf = frequency / counts_of_words_in_docs[i]

                count_of_docs_contains_word = get_count_of_docs_contains_word(word)
                idf = np.log10(COUNT_OF_WEBPAGES / count_of_docs_contains_word)
                tf_idf = tf * idf
                tokens_file.write(word + " " + str(idf) + " " + str(tf_idf) + "\n")


def compute_tf_idf_for_lemmas():
    for i in range(COUNT_OF_WEBPAGES):
        with open(os.path.join(DIRECTORY_TF_IDF, LEMMAS, "lemmas" + str(i) + ".txt"), 'a', encoding='utf-8') as lemma_file:
            for lemma, frequency in lemma_frequency_dictionaries[i].items():
                tf = frequency / counts_of_words_in_docs[i]

                count_of_docs_contains_lemma = get_count_of_docs_contains_lemma(lemma)
                idf = np.log10(COUNT_OF_WEBPAGES / count_of_docs_contains_lemma)
                tf_idf = tf * idf
                lemma_file.write(lemma + " " + str(idf) + " " + str(tf_idf) + "\n")


if __name__ == '__main__':
    sp = spacy.load("ru_core_news_sm")

    webpage_index = 0
    word_frequency_dictionaries = []
    lemma_frequency_dictionaries = []
    counts_of_words_in_docs = []
    all_lemmas = []
    os.mkdir(DIRECTORY_TF_IDF)
    os.mkdir(DIRECTORY_TF_IDF + "/" + TOKENS)
    os.mkdir(DIRECTORY_TF_IDF + "/" + LEMMAS)
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
            counts_of_words_in_docs.append(len(filtered_tokens))

            word_frequency_dictionaries.append(get_word_frequency_dictionary())
        webpage_index = webpage_index + 1

    compute_tf_idf_for_words()
    with open("lemmas.txt", 'r', encoding='utf-8') as lemmas_file:
        for line in lemmas_file:
            all_lemmas.append(line.split())
    create_lemma_frequency_dictionaries()
    compute_tf_idf_for_lemmas()
