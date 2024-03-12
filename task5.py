import os


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
    while index <= 156:
        with open(os.path.join("tf_idf", "lemmas", "lemmas" + str(index) + ".txt"), 'r',
                  encoding='utf-8') as lemma_file:
            pass


if __name__ == '__main__':
    lemmas = get_lemmas()
    vectors = get_vectors()
