

def replace_none_with_empty_str(some_dict):
    return { k: ("" if v is None else v) for k, v in some_dict.items() }