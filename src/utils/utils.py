def validate_params(params):
    params_dict = {}
    expected_params = ['n_epochs', 'model_name', '--help', '-h']
    model_names = """
            BERT_base            => Run only with BERT Base.
            BERT_large           => Run only with BERT Large.
            Glove                => Run only with Glove.
            Glove_BERT_base      => Run with Glove + BERT Base.
            Glove_BERT_large     => Run with Glove + BERT Large.
            W2VSkip              => Run only with Word2Vec-Skipgram.
            W2VSkip_BERT_base    => Run with Word2Vec-Skipgram + BERT Base.
            W2VSkip_BERT_large   => Run with Word2Vec-Skipgram + BERT Large.
    """

    # Get parameters values
    for p in params[1:]:
        name_value = p.split("=")

        if len(name_value) == 2:
            if name_value[0] not in expected_params:
                print(f"\n'{name_value[0]}': Invalid parameter!")
                exit(1)

            params_dict[name_value[0]] = name_value[1]
        elif len(name_value) == 1:
            if name_value[0] == '--help' or name_value[0] == '-h':
                print(f"\nUsage: python run_flair_experiments_editais.py n_epochs=<num epochs> model_name=<model name>"
                      f"\nWhere: n_epochs -> Number of epochs to run the experiment."
                      f"\n       model_name: \n{model_names}")
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

    if 'model_name' not in params_dict:
        print(f"\nMissing param: 'model_name'.")
        exit(1)

    return params_dict
