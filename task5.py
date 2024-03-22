import os
import re

import numpy as np
import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords
from scipy import spatial

COUNT_OF_WEBPAGES = 156


def get_lemmas():
    result_lemmas = []
    with open('lemmas.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            result_lemmas.append(line.split()[0])
            line = file.readline()
    return result_lemmas


def get_vectors():
    result_vectors = []
    index = 0
    while index <= 155:
        result_vector = [0 for _ in range(len(all_lemmas))]
        with open(os.path.join("tf_idf", "lemmas", "lemmas" + str(index) + ".txt"), 'r',
                  encoding='utf-8') as lemma_file:
            line = lemma_file.readline()
            while line:
                split_line = line.split()
                result_vector[all_lemmas.index(split_line[0])] = float(split_line[2])
                line = lemma_file.readline()
        result_vectors.append(result_vector)
        index = index + 1
    result_vectors = np.array(result_vectors)
    return result_vectors


def get_string(query_param):
    string = ""
    for token in query_param:
        string = string + token + " "
    return string


def prepare_query(query_param):
    query_param = re.sub(r"\n", " ", query_param)
    query_param = re.sub(r"\s+", " ", query_param)
    query_param = query_param.lower()
    query_param = query_param.strip()
    query_param = word_tokenize(query_param)
    query_param = [word for word in query_param if word.isalpha()]
    stop_words = set(stopwords.words('russian'))
    query_param = [token for token in query_param if token.lower() not in stop_words]
    sp = spacy.load("ru_core_news_sm")
    query_param = sp(get_string(query_param))
    result = []
    for token in query_param:
        result.append(token.lemma_)
    return result


def get_lemma_count():
    query_lemma_count = {}
    for lemma in query:
        if lemma in query_lemma_count:
            query_lemma_count[lemma] += 1
        else:
            query_lemma_count[lemma] = 1
    return query_lemma_count


def get_count_of_docs_contains_lemma(lemma):
    count_of_docs_contains_lemma = 0
    for index in range(COUNT_OF_WEBPAGES):
        with open(os.path.join("tf_idf", "lemmas", "lemmas" + str(index) + ".txt"), 'r', encoding='utf-8') as file:
            line = file.readline()
            while line and lemma != line.split()[0]:
                line = file.readline()
            if line and lemma == line.split()[0]:
                count_of_docs_contains_lemma += 1
    return count_of_docs_contains_lemma


def get_query_tf_idf():
    query_lemma_count = get_lemma_count()
    query_lemma_tfidf = {}
    for lemma, count in query_lemma_count.items():
        tf = count / len(query)
        count_of_docs_contains_lemma = get_count_of_docs_contains_lemma(lemma)
        if count_of_docs_contains_lemma == 0:
            continue
        idf = np.log10(COUNT_OF_WEBPAGES / count_of_docs_contains_lemma)
        tf_idf = tf * idf
        query_lemma_tfidf[lemma] = tf_idf
    return query_lemma_tfidf


def get_vector():
    result_vector = [0 for _ in range(len(all_lemmas))]
    for lemma, tf_idf in query_tf_idf.items():
        if lemma in all_lemmas:
            result_vector[all_lemmas.index(lemma)] = tf_idf
    result_vector = np.array(result_vector)
    return result_vector


def get_cosine_similarities():
    result_cosine_similarities = []
    norm_query_vector = np.linalg.norm(query_vector)
    for vector in vectors:
        dot_product = np.dot(query_vector, vector)
        norm_vector = np.linalg.norm(vector)

        if norm_query_vector == 0 or norm_vector == 0:
            return 0

        result_cosine_similarities.append(dot_product / (norm_query_vector * norm_vector))
    return result_cosine_similarities


def add_to_result_urls(index, line):
    if cosine_similarities[index] > 0:
        split_line = line.split()
        url = split_line[1]
        result_urls.append(url)


def iterate_in_index_txt():
    with open('index.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        index = 0
        while line:
            add_to_result_urls(index, line)
            line = file.readline()
            index += 1


def get_cos_similaries_indices_dictionary():
    result_cosine_similarities_indices_dictionary = {}
    with open('index.txt', 'r', encoding='utf-8') as file:
        line = file.readline()
        index = 0
        while line:
            result_cosine_similarities_indices_dictionary[line.split()[1]] = cosine_similarities[index]
            line = file.readline()
            index += 1
    return result_cosine_similarities_indices_dictionary


if __name__ == '__main__':
    result_urls = []
    all_lemmas = get_lemmas()
    vectors = get_vectors()
    query = input()
    query = prepare_query(query)
    query_tf_idf = get_query_tf_idf()
    query_vector = get_vector()
    cosine_similarities = get_cosine_similarities()
    if cosine_similarities == 0:
        print("Ничего не найдено")
    else:
        cosine_similarities_indices_dictionary = get_cos_similaries_indices_dictionary()
        cosine_similarities_indices_dictionary = sorted(cosine_similarities_indices_dictionary.items(),
                                                        key=lambda item: item[1], reverse=True)
        cosine_similarities_indices_dictionary = cosine_similarities_indices_dictionary[:10]
    print(cosine_similarities_indices_dictionary)
