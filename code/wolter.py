import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ProcessPoolExecutor
from typing import Literal
import multiprocessing, threading
import signal
import sys

#link = 'https://wolt.com/sk/svk/bratislava/venue/tesco-kamenne-namestie/items/ovocie-a-zelenina-5#cerstva-zelenina-71'

#link = 'https://wolt.com/sk/svk/bratislava/venue/billa-segnerova/items/udeniny-lahodky-128#sunky'


categories = ['ovocie-zelenina-103', 'pecivo-111', 'maso-ryby-117', 'udeniny-lahodky-128', 'mliecne-vyrobky-144']
#categories = ['ovocie-zelenina-103']

fruit_vegetable = ('ovocie-97', 'zelenina-99', 'bylinky-100', 'orechy-semienka-susene-ovocie-101', 'cerstve-stavy-smoothie-102')

bakery = ('chlieb-104', 'slane-pecivo-105', 'sladke-pecivo-106',
          'tortilly-pita-chleby-107', 'ostatne-pecivo-108',
          'racio-knackebrot-109', 'torty-a-zakusky-110')

meat = ('kuracie-112', 'bravcove-114', 'hovadzie-115',
        'ryby-293')

smoked_goody = ('sunky-118', 'salamy-119', 'slaniny-120', 'parky-121',
                'klobasy-122', 'spekacky-123', 'salaty-124',
                'lahodky-125', 'pastety-126', 'mast-a-oskvarky-127')

diaries = ('maslo-tuky-margariny-129', 'syry-130', 'tavene-syry-131',
           'mlieko-132', 'jogurtove-mliecne-napoje-133',
           'mliecne-dezerty-134', 'ochutene-jogurty-136',
           'biele-jogurty-135', 'tvarohy-137', 'bryndza-cottage-138',
           'natierky-pomazanky-139', 'smotany-slahacky-140',
            'majonezy-tatarske-omacky-dressingy-141', 'kondenzovane-mlieko-142',
            'ladova-kava-143')

MARKET_ID = 1

FILE_HEADER = 'name,price,approximation,market_ID'
DELIMITER = ','
OUTPUT_FILE_PATH = './resources/products.csv'

exit_event = threading.Event()

def get_soup(link: str, sleep_: float = 5):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(link)
        # Wait for some time to let the initial content load
        time.sleep(sleep_)
        
        # Get the fully rendered HTML content
        page_source = driver.page_source
        return BeautifulSoup(page_source, 'html.parser')
    finally:
        driver.quit()

def scrape_data(category: Literal['ovocie-zelenina-103', 'pecivo-111', 'maso-ryby-117', 'udeniny-lahodky-128', 'mliecne-vyrobky-144']):

    subcategories = []

    match category:
        case 'ovocie-zelenina-103':
            subcategories = fruit_vegetable
        case 'pecivo-111':
            subcategories = bakery
        case 'maso-ryby-117':
            subcategories = meat
        case 'udeniny-lahodky-128':
            subcategories = smoked_goody
        case 'mliecne-vyrobky-144':
            subcategories = diaries    

    processed_categories = []

    if exit_event.is_set():
        exit(1)

    for category_ in subcategories:
        link = f'https://wolt.com/sk/svk/bratislava/venue/billa-segnerova/items/{category}#{category_}'
        soup = get_soup(link=link)

        if soup == None:
            raise ValueError("No HTML downloaded!")

        sections = soup.find('div', class_="sc-5d58460c-0 jXrjhY").find_all('div', recursive=False)

        for section in sections:

            print("\nANOTHER SECTION!\n")
            subsections = section.find('div', class_="sc-b27603a9-0 gVLwyA").find_all('div', recursive=False)

            for index, subsection in enumerate(subsections):
                print("\nANOTHER SUBSECTION!\n")
                products = subsection.find_all('div', recursive=False)

                for index, product in enumerate(products):
                    
                    print(index + 1)

                    csv_record = product.find('h3', class_='sc-34527c92-8 dPHPvR').get_text().replace(',', '')
                    
                    if index == 0:
                        present = False

                        for el in processed_categories:
                            if el == csv_record:
                                present = True
                                print("PRESENT!")
                                print(csv_record)
                                print(el)
                                break

                            if exit_event.is_set():
                                exit(1)

                        else:
                            print("NOT PRESENT!  Adding...")
                            print(csv_record)
                            processed_categories.append(csv_record)
                        
                        if present:
                            break

                    csv_record += DELIMITER
                    price = product.find('div', class_='sc-24d58607-0 fnYmyi sc-34527c92-7 jJWXsy').get_text().replace(',', '.').split('€')
                    approximation = 0

                    if price[0][0] == '~':
                        approximation = 1
                        price[0] = price[0][1:]

                    #if len(price) > 1 and price[1] != '':
                    csv_record += price[0] + '€'
                    #else:
                     #   csv_record += price[0] + '€'

                    csv_record += DELIMITER
                    csv_record += str(approximation)

                    csv_record += DELIMITER
                    
                    
                    #csv_record += DELIMITER
                    csv_record += str(MARKET_ID)
                    csv_record += '\n'

                    with open(file=OUTPUT_FILE_PATH, mode='a', encoding='utf-8') as file:
                        file.write(csv_record)

                    

                    print(csv_record)

                    if exit_event.is_set():
                        exit(1)
                
                if exit_event.is_set():
                    exit(1)

            if exit_event.is_set():
                exit(1)

def signal_handler(sig, frame):
    print("\nReceived signal:", sig)
    print("Cleaning up and exiting...")
    # Additional cleanup code can be added here
    sys.exit(0)

def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)

        with open(file=OUTPUT_FILE_PATH, mode='w') as file:
            file.write(FILE_HEADER + '\n')

        threads = []

        for category in categories:
            print(category)
            thread = threading.Thread(target=scrape_data, args=(category,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        exit_event.set()

        for thread in threads:
            thread.join()


    print("Program terminated successfully!")

if __name__ == '__main__':
    main()        