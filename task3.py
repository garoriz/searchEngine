import os
import re

from bs4 import BeautifulSoup


def remove_btn_text_if_contains(url, code_tag):
    if 'href' in dict(code_tag.attrs) and url in code_tag['href']:
        code_tag.extract()


def remove_btn_text_if_equals(url, code_tag):
    if 'href' in dict(code_tag.attrs) and code_tag['href'] == url:
        code_tag.extract()


def remove_next_or_prev_button(class_value, code_tag):
    if 'class' in dict(code_tag.attrs) and code_tag['class'] == [class_value]:
        code_tag.extract()


def write_doc_id(webpage_index):
    with open('inverted_index.txt', 'a', encoding='utf-8') as file:
        file.write(" " + str(webpage_index))


def find_doc_id(lemmas, clean_txt, webpage_index):
    lemma_index = 0
    while lemma_index < len(lemmas):
        for word in lemmas[lemma_index]:
            if word in clean_txt:
                inverted_index[lemma_index].append(webpage_index)
                break
        lemma_index = lemma_index + 1


def get_clean_text(lemmas):
    webpage_index = 0
    while webpage_index <= 155:
        with open(os.path.join("webpages", str(webpage_index) + '.html'), 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), "lxml")

            codetags = soup.find_all('a')
            for code_tag in codetags:
                remove_btn_text_if_equals('https://ruitunion.org/en/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/uk/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/news/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/posts/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/about/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/materials/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/archives/', code_tag)
                remove_btn_text_if_equals('https://ruitunion.org/search/', code_tag)
                remove_btn_text_if_equals('https://t.me/itunion_feedback_bot', code_tag)
                remove_btn_text_if_equals('https://t.me/+0KToPESuk4s3NmJi', code_tag)
                remove_btn_text_if_contains('https://ruitunion.org/tags/', code_tag)
                remove_btn_text_if_contains('https://gitlab.com/itunion/site/-/tree/main/content/posts/', code_tag)
                remove_next_or_prev_button('next', code_tag)
                remove_next_or_prev_button('prev', code_tag)

                codetags = soup.find_all('footer')
            for code_tag in codetags:
                if 'class' in dict(code_tag.attrs) and code_tag['class'] == ['footer']:
                    code_tag.extract()
            clean_txt = soup.text
            clean_txt = re.sub(r"\n", " ", clean_txt)
            clean_txt = re.sub(r"\s+", " ", clean_txt)
            clean_txt = clean_txt.strip()
            find_doc_id(lemmas, clean_txt, webpage_index)
        webpage_index = webpage_index + 1


def write_main_word(word):
    with open('inverted_index.txt', 'a', encoding='utf-8') as file:
        file.write(word)


def add_a_line_break():
    with open('inverted_index.txt', 'a', encoding='utf-8') as file:
        file.write("\n")


def read_word_from_lemmas():
    with open('lemmas.txt', 'r', encoding='utf-8') as file:
        read_line = file.readline()
        lemmas = []
        while read_line:
            words = read_line.split(' ')
            last_index = len(words) - 1
            words.pop(last_index)
            inverted_index.append([words[0]])
            lemmas.append(words)
            read_line = file.readline()
    get_clean_text(lemmas)


def write_inverted_index():
    with open('inverted_index.txt', 'w', encoding='utf-8') as file:
        for line in inverted_index:
            for element in line:
                file.write(str(element) + " ")
            file.write("\n")


if __name__ == '__main__':
    inverted_index = []
    read_word_from_lemmas()
    write_inverted_index()
