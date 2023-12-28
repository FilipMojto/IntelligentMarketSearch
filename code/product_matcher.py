

import rapidfuzz.fuzz as fuzz
import argparse

from marketing import Product


DEF_FILE_PATH = './code/requirements/products.csv'

parser = argparse.ArgumentParser(
                    prog='Shopping product parser',
                    description="""The parser establishes connection with a hypermarket\'s online leaflet page
                                and scapes all related products according to the input product name.""",
                    epilog='Text at the bottom of help')

# parser.add_argument('product')
# parser.add_argument('-f', '--file')

str_1 = "rajciny"
str_2 = "paradajky"

print(fuzz.partial_ratio(str_1, str_2))
print(fuzz.token_set_ratio(str_1, str_2))






args = parser.parse_args()






