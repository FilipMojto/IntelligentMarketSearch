from bs4 import BeautifulSoup
import requests
import sys
import io
import argparse
import os

FILE_PATH = './output.csv'
DELIMITER = ','
print("here")

parser = argparse.ArgumentParser(
                    prog='Shopping product parser',
                    description="""The parser establishes connection with a hypermarket\'s online leaflet page
                                and scrapes all provided products or the filtered ones based on a product name or category.""",
                    epilog='Text at the bottom of help')

parser.add_argument('-p', '--product')
parser.add_argument('-c', '--category', choices=['napoje', 'pecivo'])
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-f', '--file')

args = parser.parse_args()
print("here")
if sum([bool(args.product), bool(args.category), bool(args.all)]) != 1:
    parser.error("Precisely one of -p/--product or -c/--category must be provided.")
print("here")



# Set the default encoding of stdout to UTF-8
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("here")
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

print("here")
with open(args.file if args.file else FILE_PATH, 'w', encoding='utf-8') as file: 
    file.write('nazov,cena\n')
    url_2 = ''

    while True:
        print(f"Currently processed page: {page_i}")
        if(args.product):
            url_2 = f'https://potravinydomov.itesco.sk/groceries/sk-SK/search?query={args.product}&page={str(page_i)}&count=48'
        elif(args.category):
            url_2 = f"https://potravinydomov.itesco.sk/groceries/sk-SK/shop/{args.category}/all?page={str(page_i)}&count=48"
    
        url = 'https://proxy.scrapeops.io/v1/'
        params = {
            'api_key': '7e801fe4-49da-4ddb-9043-913bf7218c27',
            'url': url_2, 
        }

        # Getting the soup object
        soup = get_soup(url, params)
        
        if requests.get(url, params=params).status_code != 200:
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
        


        for index, item in enumerate(product_grid):
            print(f"Currently processed product: {index + 1}")

            try:
                csv_record: str = item.find('span', class_='styled__Text-sc-1i711qa-1 xZAYu ddsweb-link__text').get_text().replace(',', '')
            except (AttributeError):
                print("Processed product has no product name text! Skipping...")
                continue
        
            csv_record += ','
            
            try:
                csv_record += item.find('p', class_='styled__StyledHeading-sc-119w3hf-2 jWPEtj styled__Text-sc-8qlq5b-1 lnaeiZ beans-price__text').get_text().replace(',', '.')
            except (AttributeError):
                print("Processed product has no price text! Skipping...")
                continue

        
            csv_record += '\n'

            file.write(csv_record)
        page_i += 1
    
    print(f"Succesfully scraped {page_i - 1} pages!")