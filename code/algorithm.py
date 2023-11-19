

# This function calculate the match score between two strings. The result
# is between 0 for absolutely no similarity to 1 for perfect similarity.
# def match_strings(str_1: str, str_2: str, case_sensitive: bool = False) -> float:
#     if not isinstance(str_1, str) or not isinstance(str_2, str):
#         raise TypeError("Invalid type for matching! Strings are requested.")
    
#     if not case_sensitive:
#         str_1 : str = str_1.lower()
#         str_2 : str = str_2.lower()



#     len_1 : int = len(str_1)
#     len_2 : int = len(str_2)

#     weight : int = 1/max(len_1, len_2)
#     match = sum(c1 == c2 for c1, c2 in zip(str_1, str_2))

#     return round(match * weight, 2)