from gensim.models import KeyedVectors


if __name__ == '__main__':
    embeddings = {
        'skip_s300': {
            'embeddings_txt_file': 'data/Embeddings/pt/skip_s300.txt',
            'embeddings_bin_file': 'data/Embeddings/pt/skip_s300.gensim'
        },
        'glove_s300': {
            'embeddings_txt_file': 'data/Embeddings/pt/glove_s300.txt',
            'embeddings_bin_file': 'data/Embeddings/pt/glove_s300.gensim'
        }
    }

    seq = 1
    qty_embeddings = len(embeddings)

    print('\n=> Converting TXT Embedding(s) to binary...\n')

    for emb in embeddings.keys():
        embeddings_txt_file = embeddings[emb]['embeddings_txt_file']
        embeddings_bin_file = embeddings[emb]['embeddings_bin_file']
        print(f"Embedding {seq}/{qty_embeddings}:")
        print(f"   Converting '{emb}' of txt file '{embeddings_txt_file}' to bin file '{embeddings_bin_file}'... ")

        try:
            emb_vectors = KeyedVectors.load_word2vec_format(embeddings_txt_file, binary=False)
        except FileNotFoundError:
            print(f"   Warning: File '{embeddings_txt_file}' not found! Skipping it...\n")
            seq += 1
            continue

        emb_vectors.save(embeddings_bin_file)
        print('   Process Completed!\n')
        seq += 1
