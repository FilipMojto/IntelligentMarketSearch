from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
from selenium.webdriver.chrome.service import Service
from enum import Enum
from collections import OrderedDict
import threading
from code.AOSS.utils import ThreadPool


class Category(Enum):
    FRUIT_VEGETABLE = 1
    BAKERY_PRODUCTS = 2
    MEAT_FISH = 3
    SMOKED_MEAT = 4
    DAIRY_PRODUCTS = 5
    EGGS_YEAST = 6
    READY_MEALS = 7
    DURABLES = 8
    SWEETS = 9
    SALTY_SNACKS = 10
    NON_ALCOHOLIC_DRINKS = 11
    BEER_CIDER = 12
    
    


categories = {
    Category.FRUIT_VEGETABLE: 'ovocie-zelenina-103',
    Category.BAKERY_PRODUCTS: 'pecivo-111',

}

URL = 'https://wolt.com/sk/svk/bratislava/venue/billa-segnerova/items/'
APPROXIMATION_SIGN = '~'
CURRENCY_SIGN = '€'

INPUT_FILE = './resources/markets.csv'
INPUT_FILE_CHUNK_SIZE = 200

OUTPUT_FILE = './output.csv'
OUTPUT_FILE_LOCK = threading.Lock()
HEADER = 'product_ID,name,price,approximation,market_ID'
FILE_DELIMITER = ','
DELIM_REPLACEMENT = '.'
MARKET_ID = 1

def load_product_ID() -> int:
    with open(file=INPUT_FILE, mode='r') as file:

        data = file.read(INPUT_FILE_CHUNK_SIZE)
        lines = data.split('\n')

        for line in lines:
            record = line.split(FILE_DELIMITER)

            if record[0] == str(MARKET_ID):
                return int(record[2])
    
    raise ValueError("No record found for the provided market ID!")

PRODUCT_ID = load_product_ID()
PRODUCT_ID_LOCK = threading.Lock()


def save_product_ID():
    global PRODUCT_ID
    with PRODUCT_ID_LOCK:
        data = ""

        with open(file=INPUT_FILE, mode='r') as file:
            data = file.read(INPUT_FILE_CHUNK_SIZE)
        
        lines = data.split('\n')
        data = ""

        for line in lines:
            record = line.split(FILE_DELIMITER)

            if record[0] == str(MARKET_ID):
                data += record[0] + FILE_DELIMITER + record[1] + FILE_DELIMITER + str(PRODUCT_ID) + '\n'
            else:
                data += line + '\n'
        
        with open(file=INPUT_FILE, mode='w', encoding='utf-8') as file:
            file.write(data)
     
def save_to_output_file(data):
    with OUTPUT_FILE_LOCK:
        with open(file=OUTPUT_FILE, mode='a', encoding='utf-8') as _file:
            _file.write(data)

parser = argparse.ArgumentParser()
parser.add_argument('-dp', '--driver_path', required=False)
parser.add_argument('-c', '--clear_data', required=False, action='store_true')
args = parser.parse_args()

if args.clear_data:
    with open(file=OUTPUT_FILE, mode='a') : pass
    with open(file=OUTPUT_FILE, mode='w') : pass

# Function to get the total scroll height using JavaScript
def get_total_scroll_height(_driver):
    return _driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

def scrape_data(driver, height_pos: int = 0, dataset: OrderedDict = OrderedDict(), sleep_=3):
    driver.execute_script(f"window.scrollTo(0, {height_pos});")
    time.sleep(sleep_)

    products = driver.find_elements(By.CSS_SELECTOR, '.sc-a8239ffe-4.gOfKkf')

    # Now you can interact with the located sub-elements
    for index, sub_element in enumerate(products):
        name: str = sub_element.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text.replace(FILE_DELIMITER, DELIM_REPLACEMENT)
        price: str = sub_element.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text.replace(FILE_DELIMITER, DELIM_REPLACEMENT)

        approximation = '0'

        if(price[0] == APPROXIMATION_SIGN):
            price = price[1:]
            approximation = '1'

        price = price.split(CURRENCY_SIGN)[0].strip()

        print(name)
        
        # Check if the name is not already in the dataset before adding
        if name not in dataset:
            global PRODUCT_ID
            with PRODUCT_ID_LOCK:
                
                dataset[name] = str(PRODUCT_ID) + FILE_DELIMITER + price + FILE_DELIMITER + approximation + FILE_DELIMITER + str(MARKET_ID)
                PRODUCT_ID += 1

    return dataset

def update_category(category: Category, to_file: bool = False, scrolldown: int = 2000):
    url = URL + categories[category]

    # Set Chrome options to run in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    if(args.driver_path):
        driver = webdriver.Chrome(service=Service(args.driver_path), options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.get(url=url)



    cur_height_pos = 0
    total_height = get_total_scroll_height(_driver=driver)

    products = OrderedDict()

    while cur_height_pos < total_height:
        products = scrape_data(driver=driver, height_pos=cur_height_pos, dataset=products, sleep_=1.5)
        cur_height_pos += scrolldown

    if to_file:
        with open(file=OUTPUT_FILE, mode='a', encoding='utf-8') as _file:
            for name, data in products.items():

                elements = data.split(FILE_DELIMITER)
                save_to_output_file(elements[0] + FILE_DELIMITER + name + FILE_DELIMITER + elements[1] + FILE_DELIMITER + elements[2] + FILE_DELIMITER + elements[3] + '\n')
                #_file.write(elements[0] + FILE_DELIMITER + name + FILE_DELIMITER + elements[1] + FILE_DELIMITER + elements[2] + FILE_DELIMITER + elements[3] + '\n')

    driver.quit()
    return products



threads = []

for category in categories:

    with ThreadPool()

    thread = threading.Thread(target=update_category, args=(category, True, 1500))
    thread.start()
    threads.append(thread)

#update_category(category=Category.FRUIT_VEGETABLE, to_file=True, scrolldown=1500)
    
for thread in threads:
    thread.join()

save_product_ID()