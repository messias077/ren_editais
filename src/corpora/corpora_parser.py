import os


def read_corpus_file(corpus_file, split_char='\t', idx=1):
    with open(corpus_file, encoding='utf-8') as file:
        lines = file.readlines()
    data = []
    words = []
    tags = []
    for line in lines:
        line = line.replace('\n', '')
        if line != '':
            if split_char in line:
                fragments = line.split(split_char)
                words.append(fragments[0])
                tags.append(fragments[idx])
        else:
            if len(words) > 1:
                data.append((words, tags))
            words = []
            tags = []

    return data


def read_corpora_editais(corpora_path):
    corpora_names = os.listdir(corpora_path)
    corpora_data = {}
    for corpus_name in corpora_names:
        if "corpus_" not in corpus_name:  # avoid loop in file creation
            corpus_path = os.path.join(corpora_path, corpus_name)
            corpus_data = read_corpus_file(corpus_path, split_char=' ', idx=1)
            corpora_data[corpus_name.replace('.conll', '')] = corpus_data
    return corpora_data


def generate_train_file(corpora, corpora_names, train_idx, train_file):
    train_data = []
    for id_ in train_idx:
        data = corpora[corpora_names[id_]]
        train_data.extend(data)
    data_conll = ''
    for data in train_data:
        sent_data = '\n'.join('{} {}'.format(token, tag) for token, tag in zip(data[0], data[1]))
        sent_data += '\n\n'
        data_conll += sent_data
    data_conll = data_conll[:-2]
    with open(train_file, 'w', encoding='utf-8') as file:
        file.write(data_conll)


def generate_test_file(test_results_file, new_test_file):
    with open(new_test_file, 'w+', encoding='utf8') as new_file:
        with open(test_results_file, 'r', encoding='utf8') as file:
            for line in file:
                if line != '\n':
                    line = line.strip()
                    spliter = line.split(' ')
                    token = spliter[0]
                    tag_1 = spliter[1]
                    tag_2 = spliter[2]
                    new_file.write(str(token) + ' ' + str(tag_1) +
                                   ' ' + str(tag_2) + '\n')
                else:
                    new_file.write(line)
