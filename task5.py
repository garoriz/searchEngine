import os
import re

import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords


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
        result_vector = [0 for i in range(len(lemmas))]
        with open(os.path.join("tf_idf", "lemmas", "lemmas" + str(index) + ".txt"), 'r',
                  encoding='utf-8') as lemma_file:
            line = lemma_file.readline()
            while line:
                split_line = line.split()
                result_vector[lemmas.index(split_line[0])] = split_line[2]
                line = lemma_file.readline()
        result_vectors.append(result_vector)
        index = index + 1
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


if __name__ == '__main__':
    lemmas = get_lemmas()
    vectors = get_vectors()
    query = prepare_query(input())
    print(query)
