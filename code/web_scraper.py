from bs4 import BeautifulSoup
import requests
import sys
import io
import argparse
import os

FILE_PATH = './output.csv'
DELIMITER = ','


parser = argparse.ArgumentParser(
                    prog='Shopping product parser',
                    description="""The parser establishes connection with a hypermarket\'s online leaflet page
                                and scapes all related products according to the input product name.""",
                    epilog='Text at the bottom of help')

parser.add_argument('-p', '--product')
parser.add_argument('-f', '--file')

args = parser.parse_args()

# Set the default encoding of stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Function to get the soup object
def get_soup(url, params):
    response = requests.get(url, params=params)
    # Encoding the response to utf-8 to handle special characters
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'html.parser')

page_i = 1

if args.file:

    match os.path.splitext(args.file)[1]:
        case '.tsv':
            DELIMITER = '\t'
        case '.csv':
            pass
        case _:
            raise TypeError("Invalid or unsupported file extension!")


with open(args.file if args.file else FILE_PATH, 'w', encoding='utf-8') as file: 
    file.write('nazov,cena\n')

    while True:
        # Your URL and parameters
        url = 'https://proxy.scrapeops.io/v1/'
        params = {
            'api_key': '7e801fe4-49da-4ddb-9043-913bf7218c27',
            'url': f'https://potravinydomov.itesco.sk/groceries/sk-SK/search?query={args.product}&page={str(page_i)}&count=48', 
        }

        # Getting the soup object
        soup = get_soup(url, params)

        try:
            product_items = soup.find('ul', class_="product-list grid").find_all('li')
        except AttributeError:
            break

        # Printing the soup object
        
        if product_items == None:
            break
        
        for item in product_items:
        
            csv_record: str = item.find('span', class_='styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text').get_text().replace(',', '')
            csv_record += ','
            
            csv_record += item.find('p', class_='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text').get_text().replace(',', '.')
            csv_record += '\n'

            file.write(csv_record)
        page_i += 1