import os
import time
import sys

from src.corpora.corpora_parser import read_corpora_editais, generate_train_file, generate_test_file
from flair.datasets import ColumnCorpus
from flair.embeddings import WordEmbeddings, StackedEmbeddings
from flair.embeddings import FlairEmbeddings, TransformerWordEmbeddings, ELMoEmbeddings
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.optim import SGDW
from src.utils.utils import validate_params

if __name__ == '__main__':
    params = validate_params(sys.argv)

    # Preparing common environment
    n_epochs = params['n_epochs']
    corpus_name = 'editais'
    corpora_path = 'data/corpora/editais/regiao'

    columns = {
        0: 'token',
        1: 'ner'
    }

    word2vec_skip_file = 'data/Embeddings/pt/skip_s300.gensim'
    word2vec_cbow_file = 'data/Embeddings/pt/cbow_s300.gensim'

    glove_file = 'data/Embeddings/pt/glove_s300.gensim'

    flair_forward_file = 'data/Embeddings/pt/flairBBP_forward-pt.pt'
    flair_backward_file = 'data/Embeddings/pt/flairBBP_backward-pt.pt'

    bert_base_embedding_path = 'neuralmind/bert-base-portuguese-cased'
    bert_large_embedding_path = 'neuralmind/bert-large-portuguese-cased'

    # Initizaling default values
    is_use_glove = False
    is_use_w2v_skip = False
    is_use_w2v_cbow = False
    is_use_flair = False
    is_use_elmo = False
    is_use_bert_base = False
    is_use_bert_large = False
    is_use_crf = True
    data_folder = None

    # Initializing specific values based on model_name
    model_name = params['model_name'].lower()

    if model_name == 'bert_base':
        is_use_bert_base = True
    elif model_name == 'bert_large':
        is_use_bert_large = True
    elif model_name == 'glove':
        is_use_glove = True
    elif model_name == 'glove_bert_base':
        is_use_glove = True
        is_use_bert_base = True
    elif model_name == 'glove_bert_large':
        is_use_glove = True
        is_use_bert_large = True
    elif model_name == 'w2vskip':
        is_use_w2v_skip = True
    elif model_name == 'w2vskip_bert_base':
        is_use_w2v_skip = True
        is_use_bert_base = True
    elif model_name == 'w2vskip_bert_large':
        is_use_w2v_skip = True
        is_use_bert_large = True
    else:
        print("\nInvalid option for 'model_name'. Please, type 'python run_flair_experiments_editais.py -h' for help.")
        exit(1)

    print(f"\n\n==> Running: '{params['model_name']}'...\n\n")
    time.sleep(10)

    if is_use_bert_base or is_use_bert_large:
        batch_size = 16
    else:
        batch_size = 32

    model_name = ''

    if is_use_flair:
        model_dir = 'data/models/flair'
        model_name += 'flair'
    elif is_use_bert_base:
        model_dir = 'data/models/bert_base'
        model_name += 'bert_base'
    elif is_use_bert_large:
        model_dir = 'data/models/bert_large'
        model_name += 'bert_large'
    elif is_use_elmo:
        model_dir = 'data/models/elmo'
        model_name += 'elmo'
    else:
        model_dir = 'data/models/bilstm'
        model_name += 'bilstm'

    if is_use_w2v_skip:
        model_dir += '_w2v_skip'
        model_name += '_w2v_skip'
    elif is_use_w2v_cbow:
        model_dir += '_w2v_cbow'
        model_name += '_w2v_cbow'
    elif is_use_glove:
        model_dir += '_glove'
        model_name += '_glove'

    if is_use_crf:
        model_dir += '_crf'
        model_name += '_crf'
        print('\nRunning using CRF')

    print(f'\nModel Name: {model_name}')

    corpora = read_corpora_editais(corpora_path)

    print('\nNum Corpora:', len(corpora))

    corpora_names = list(corpora.keys())

    for test_id in range(len(corpora_names)):

        print(f'\n\nEvaluation: {corpora_names[test_id]}\n')

        model_dir_corpus = os.path.join(model_dir, corpus_name, corpora_names[test_id])

        os.makedirs(model_dir_corpus, exist_ok=True)

        val_id = (test_id+1) % len(corpora_names)

        train_idx = [j for j in range(len(corpora_names)) if j != test_id and j != val_id]

        test_file = f'{corpora_names[test_id]}.conll'
        val_file = f'{corpora_names[val_id]}.conll'
        train_file = f"corpus_{'_'.join([corpora_names[j].replace('corpus_', '') for j in train_idx])}.conll"

        train_file_path = os.path.join(corpora_path, train_file)

        generate_train_file(corpora, corpora_names, train_idx, train_file_path)

        corpus = ColumnCorpus(corpora_path, columns, train_file=train_file, test_file=test_file,
                              dev_file=val_file)

        print('\n  Train len: ', len(list(corpus.train)))
        print('  Dev len: ', len(list(corpus.dev)))
        print('  Test len: ', len(list(corpus.test)))

        print('\n  Train: ', corpus.train[1].to_tagged_string('label'))
        print('  Dev: ', corpus.dev[1].to_tagged_string('label'))
        print('  Test: ', corpus.test[1].to_tagged_string('label'))

        tag_type = 'ner'

        tag_dictionary = corpus.make_label_dictionary(label_type=tag_type)

        print('\nTags: ', tag_dictionary.idx2item)

        # Loading Traditional Embeddings

        if is_use_w2v_skip:
            print('\nRunning using Word2vec Skip')
            traditional_embedding = WordEmbeddings(word2vec_skip_file)
        elif is_use_w2v_cbow:
            print('\nRunning using Word2vec CBOW')
            traditional_embedding = WordEmbeddings(word2vec_cbow_file)
        elif is_use_glove:
            print('\nRunning using Glove')
            traditional_embedding = WordEmbeddings(glove_file)
        else:
            print('\nNot using Traditional embedding')
            traditional_embedding = None

        # Loading Contextual Embeddings

        embedding_types = []

        if traditional_embedding is not None:
            embedding_types.append(traditional_embedding)

        if is_use_flair:
            print('\nRunning using Flair')
            flair_embedding_forward = FlairEmbeddings(flair_forward_file)
            flair_embedding_backward = FlairEmbeddings(flair_backward_file)
            embedding_types.append(flair_embedding_forward)
            embedding_types.append(flair_embedding_backward)

        if is_use_bert_base or is_use_bert_large:
            if is_use_bert_base:
                print('\nRunning using BERT Base')
                bert_path = bert_base_embedding_path
            else:
                print('\nRunning using BERT Large')
                bert_path = bert_large_embedding_path
            bert_embedding = TransformerWordEmbeddings(bert_path, fine_tune=False, layers='-1,-2,-3,-4',
                                                       allow_long_sentences=True)
            bert_embedding.max_subtokens_sequence_length = 512
            embedding_types.append(bert_embedding)

        if is_use_elmo:
            print('\nRunning using Elmo')
            elmo_embedding = ELMoEmbeddings('pt', embedding_mode='all')
            embedding_types.append(elmo_embedding)

        embeddings = StackedEmbeddings(embeddings=embedding_types)

        tagger = SequenceTagger(hidden_size=256, embeddings=embeddings, tag_dictionary=tag_dictionary,
                                tag_type=tag_type, use_crf=is_use_crf)

        trainer = ModelTrainer(tagger, corpus)

        project_name = f'ner_pt_{corpora_names[test_id]}'

        trainer.train(model_dir_corpus, optimizer=SGDW, learning_rate=0.1, mini_batch_size=batch_size,
                      max_epochs=n_epochs)

        test_results_file = os.path.join(model_dir_corpus, 'test.tsv')

        new_test_file = os.path.join(model_dir_corpus, corpus_name + '_conlleval_test.tsv')

        test_results = generate_test_file(test_results_file, new_test_file)

        os.remove(train_file_path)
