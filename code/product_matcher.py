

import rapidfuzz.fuzz as fuzz
import argparse

from marketing import Product


SRC_FILE_PATH = './resources/products.csv'
OUTPUT_FILE_PATH = './resources/product_match.csv'
BEST_MATCHES_FILE_PATH = './resources/best_matches.csv'

DELIMITER = ','
BEST_MATCHES_SIZE_LIMIT = 10

parser = argparse.ArgumentParser(
                    prog='Shopping product parser',
                    description="""The parser establishes connection with a hypermarket\'s online leaflet page
                                and scapes all related products according to the input product name.""",
                    epilog='Text at the bottom of help')

parser.add_argument('product')
parser.add_argument('-a', '--append', action='store_true')

args = parser.parse_args()


if not args.append:
    open(file=OUTPUT_FILE_PATH, mode='w')



best_matches = []

def put_if_match_better(product: Product, match: float) -> bool:

    if len(best_matches) < BEST_MATCHES_SIZE_LIMIT:
        best_matches.append((product, match))

    min_match = -1
    min_match_i = -1

    for index, match_ in enumerate(best_matches):

        if(min_match_i == -1 or match_[1] < min_match):
            min_match_i = index
            min_match = match_[1]


    if(min_match_i != -1 and match > min_match):
        best_matches[min_match_i] = (product, match)
        return True
    
    return False

with open(file=SRC_FILE_PATH, mode='r', encoding='utf-8') as file:
    
    line = file.readline()
    print(line)


    index = 0
    while(line):
    
        record = line.split(sep=DELIMITER)
        print(record)
        product = Product(ID=index, name=record[0], price=float(record[1].split(' ')[0]))


        with open(file=OUTPUT_FILE_PATH, mode='a', encoding='utf-8') as file2:
            file2.write(f'{index},{fuzz.partial_ratio(args.product, record[0])},{fuzz.token_set_ratio(args.product, record[0])} \n')

        put_if_match_better(product=product, match=fuzz.partial_ratio(args.product, record[0]))

        index += 1
        line = file.readline()


open(file=BEST_MATCHES_FILE_PATH, mode='w')
with open(file=BEST_MATCHES_FILE_PATH, mode='a', encoding='utf-8') as file:

    for match in best_matches:
        file.write(f'{match[0].get_ID()}, {match[1]}\n')











