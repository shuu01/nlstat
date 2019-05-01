# python natural language statistics

Gather statistics from python projects

## usage

    import dclnt

    top_size = 10
    path = '/path'

    verbs_stat = dclnt.get_top_verbs_in_path(path, top_size)
    funcs_stat = dclnt.get_top_function_names_in_path(path, top_size)
    all_verbs = dclnt.get_all_words_in_path(path)

