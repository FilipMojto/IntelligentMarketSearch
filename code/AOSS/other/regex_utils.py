
import re
from unidecode import unidecode

def is_word(text):
    text = unidecode(text)

    # Define a regex pattern for a word
    pattern = r'^[a-zA-Z]+$'#$'

    # Return True if it's a word, otherwise False
    return bool(re.match(pattern, text))



def extract_words(text: str) -> list[str]:

    splits = text.split(sep=' ')
    words = []

    for split in splits:

        if is_word(split):
            words.append(split)
    
    return words