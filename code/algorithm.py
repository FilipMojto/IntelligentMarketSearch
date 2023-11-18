

def match_strings(str_1 : str, str_2 : str) -> float:
    len_1 = len(str_1)
    len_2 = len(str_2)

    min_len = min(len_1, len_2)
    fragment = 1/max(len_1, len_2)

    #min_len = min(len_1, len_2)
    i = 0
    match = 0

    for i in range(0, min_len):
        if str_1[i] == str_2[i]:
            match += fragment

    return round(match, 2)