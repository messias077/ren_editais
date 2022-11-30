def validate_params(params):
    params_dict = {}
    expected_params = ['n_epochs', 'embeddings', '--help', '-h']
    traditional = ['glove', 'w2v_skip', 'w2v_cbow']
    contextualized = ['flair', 'elmo', 'bert_base', 'bert_large']

    embedding_names = """
            Traditional (embedding1):
               glove        => Glove Embedding
               w2v_skip     => Word2Vec + Skip-gram
               w2v_cbow     => Word2Vec + CBow

            Contextualized (embedding2):
               flair        => Flair Embeddings
               elmo         => Elmo Embedding
               bert_base    => BERT Base version            
               bert_large   => BERT Large version            
    """

    # Get parameters values
    for p in params[1:]:
        name_value = p.split("=")

        if len(name_value) == 2:
            if name_value[0] not in expected_params:
                print(f"\n'{name_value[0]}': Invalid parameter!")
                exit(1)

            if name_value[0] == 'embeddings':
                count_traditional = 0
                count_contextualized = 0
                list_embeddings = name_value[1].split(",")

                if len(list_embeddings) <= 2:
                    for e in list_embeddings:
                        e_lower = e.lower()
                        if e_lower in traditional:
                            count_traditional += 1
                        elif e_lower in contextualized:
                            count_contextualized += 1
                        else:
                            print(f"\n'{e}': Invalid embedding name!")
                            exit(1)

                    if count_traditional > 1 or count_contextualized > 1:
                        print("\nInvalid combination. Please choose to combine maximum: 0 or 1 traditional + 0 or 1 "
                              "contextualized.")
                        exit(1)
                else:
                    print("\nInvalid combination. Please choose to combine maximum: 0 or 1 traditional + 0 or 1 "
                          "contextualized.")
                    exit(1)

            params_dict[name_value[0]] = name_value[1]
        elif len(name_value) == 1:
            if name_value[0] == '--help' or name_value[0] == '-h':
                print(f"\nUsage: python run_flair_experiments_editais.py n_epochs=<num epochs> embeddings=<embedding1,"
                      f"embedding2>"
                      f"\nWhere: n_epochs   => Number of epochs to run the experiment."
                      f"\n       embeddings => Embeddings to combine. Maximum: 0 or 1 traditional + 0 or 1 "
                      f"contextualized."
                      f"\n\n       Embedding options: \n{embedding_names}")
                exit(0)
            else:
                print(f"\n'{name_value[0]}': Invalid parameter or without value!")
                exit(1)
        else:
            print(f"\n'{p}': Invalid parameter!")
            exit(1)

    # Validate mandatory params
    if 'n_epochs' in params_dict:
        try:
            params_dict['n_epochs'] = int(params_dict['n_epochs'])
        except ValueError:
            print(f"\nInvalid parameter type for 'n_epochs'. Please, type an integer.")
            exit(1)
    else:
        print(f"\nMissing param: 'n_epochs'.")
        exit(1)

    if 'embeddings' not in params_dict:
        print(f"\nMissing param: 'embeddings'.")
        exit(1)

    return params_dict
