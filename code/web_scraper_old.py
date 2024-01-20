from bs4 import BeautifulSoup
import requests
import sys
import io
import argparse
import os
import threading
import time
from typing import Literal

#   HTTP CONFIGURATION

PROXY_URL = 'https://proxy.scrapeops.io/v1/'
#API_KEY = '7e801fe4-49da-4ddb-9043-913bf7218c27'
API_KEY = '5b747c45-d035-48c8-abda-e1047835e5dc'

#   SRC FILE CONFIGURATION

FILE_PATH = './resources/products.csv'
DELIMITER = ','
HEADER = 'name,price,approximation,market_ID'
#   MARKET CONFIGURATION

MARKET_CATEGORIES = ('vianoce', 'ovocie-a-zelenina', 'mliecne-vyrobky-a-vajcia', 'pecivo', 'maso-ryby-a-lahodky',
                     'trvanlive-potraviny', 'specialna-a-zdrava-vyziva', 'mrazene-potraviny', 'napoje', 'alkohol',
                     'starostlivost-o-domacnost', 'zdravie-a-krasa', 'starostlivost-o-dieta', 'chovatelske-potreby',
                     'domov-a-zabava')
MARKET_ID=0


#   SCRIPT ARGUMENTS

parser = argparse.ArgumentParser(
                    prog='Shopping product parser',
                    description="""The parser establishes connection with a hypermarket\'s online leaflet page
                                and scrapes all provided products or the filtered ones based on a product name or category.""",
                    epilog='Text at the bottom of help')

parser.add_argument('-p', '--product')
parser.add_argument('-c', '--category', choices=['napoje', 'pecivo'])
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-f', '--file')
parser.add_argument('-m', '--market', type=int)
parser.add_argument('-o', '--overwrite', action='store_true')

args = parser.parse_args()

if sum([bool(args.product), bool(args.category), bool(args.all)]) != 1:
    parser.error("Precisely one of -p/--product or -c/--category must be provided.")


if(args.market):
    MARKET_ID = args.market

args.file if args.file else FILE_PATH


# Function to get the soup object
def get_soup(url, params):
    response = requests.get(url, params=params)
    # Encoding the response to utf-8 to handle special characters
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

if args.file:

    match os.path.splitext(args.file)[1]:
        case '.tsv':
            DELIMITER = '\t'
        case '.csv':
            pass
        case _:
            raise TypeError("Invalid or unsupported file extension!")

def scrape_data(name: str, file, lock: threading.Lock = threading.Lock, data_type: Literal['product', 'category'] = 'product'):
    url = ''
    page_i = 1
    print(f'{name}')
    print(f'{data_type}')

    while True:
        print(f"Currently processed page: {page_i}")

        if data_type == 'product':
            url = f'https://potravinydomov.itesco.sk/groceries/sk-SK/search?query={name}&page={str(page_i)}&count=48'
        elif data_type == 'category':
            url = f"https://potravinydomov.itesco.sk/groceries/sk-SK/shop/{name}/all?page={str(page_i)}&count=48"


        params = {
            'api_key': API_KEY,
            'url': url, 
        }
        

        # Getting the soup object
        soup = get_soup(PROXY_URL, params)

        if requests.get(PROXY_URL, params=params).status_code != 200:
            print(requests.get(PROXY_URL, params=params).status_code)
            print(f"Request failed for page {page_i}. Exiting the loop.")
            break

        try:
            product_grid = soup.find('ul', class_="product-list grid").find_all('li')

        except AttributeError:
            print(f"Error parsing page {page_i}. Exiting the loop.")
            break

        # Printing the soup object
        
        if product_grid == None:
            print(f"No product grid found on page {page_i}. Exiting the loop.")
            break
        
        with lock:
            for index, item in enumerate(product_grid):
                print(f"Currently processed product: {index + 1}")

                try:
                    csv_record: str = item.find('span', class_='styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text').get_text().replace(',', '')
                except (AttributeError):
                    print("Processed product has no product name text! Skipping...")
                    continue
            
                csv_record += DELIMITER
                
                try:
                    csv_record += item.find('p', class_='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text').get_text().replace(',', '.')
                except (AttributeError):
                    print("Processed product has no price text! Skipping...")
                    continue

                
                csv_record += DELIMITER
                csv_record += str(MARKET_ID)
                csv_record += '\n'

                file.write(csv_record)
        page_i += 1
    
    print(f"Succesfully scraped {page_i - 1} pages!")

if(args.overwrite):
    with open(args.file if args.file else FILE_PATH, mode='w', encoding='utf-8') as file:
        file.write("name,price,market_ID")


file = open(args.file if args.file else FILE_PATH, mode='a', encoding='utf-8')
lock = threading.Lock()


# with open(args.file if args.file else FILE_PATH, mode='a', encoding='utf-8') as file: 
if(args.all):

    for category in MARKET_CATEGORIES:

        thread = threading.Thread(target=scrape_data, args=(category, file, lock, 'category'))
        thread.start()
        time.sleep(3)
        #scrape_data(name=category, file=file, type='category')
elif args.category:
    scrape_data(name=args.category, file=file, data_type='category')
elif args.product:
    scrape_data(name=args.product, file=file, data_type='product')


while threading.active_count() > 1:
    time.sleep(1)
    print("Main thread waiting...")

print("Script finished successfully!")