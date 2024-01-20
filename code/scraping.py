from marketing import Market
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import argparse
from selenium.webdriver.chrome.service import Service
from enum import Enum
from collections import OrderedDict
import threading
from typing import List

class ProductScraper:

    __URL = 'https://wolt.com/sk/svk/bratislava/venue/'
    __PRICE_APPROX_SIGN = '~'
    __CURRENCY_SIGN = '€'

    def scrape_products(self, driver: webdriver.Chrome, height_pos: int, sleep_: int = 3) -> List[str]:
        driver.execute_script(f"window.scrollTo(0, {height_pos});")
        time.sleep(sleep_)

        products = driver.find_elements(By.CSS_SELECTOR, '.sc-a8239ffe-4.gOfKkf')
        dataset = []

        # Now you can interact with the located sub-elements
        for index, sub_element in enumerate(products):
            name: str = sub_element.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text.replace(self.__f_delimiter,
                                                                                                                                  self.__delim_subst)
            price: str = sub_element.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text.replace(self.__f_delimiter, 
                                                                                                                                 self.__delim_subst)

            approximation = '0'

            if(price[0] == self.__PRICE_APPROX_SIGN):
                price = price[1:]
                approximation = '1'

            price = price.split(self.__CURRENCY_SIGN)[0].strip()

            print(name)
            
            # Check if the name is not already in the dataset before adding
           # if name not in dataset:
            #global PRODUCT_ID
            #with PRODUCT_ID_LOCK:
            
            dataset.append(name + self.__f_delimiter + price + self.__f_delimiter + approximation + self.__f_delimiter + str(self.__market.ID()))

            #dataset[name] = str(self.__market.register_product()) + self.__f_delimiter + price + self.__f_delimiter + approximation 
            #+ self.__f_delimiter + str(self.__market.ID())
                #PRODUCT_ID += 1

        return dataset

    def scrape_category(self, category: str):
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

    def scrape_all(self): pass

    # Function to get the total scroll height using JavaScript
    def get_total_scroll_height(self, _driver):
        return _driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

    def __init__(self, market: Market, output_file: str, f_delimiter: str = ',', delim_subst: str = '.', clear_data: bool = False):
        self.__market = market
        self.__output_file = output_file
        self.__f_delimiter = f_delimiter
        self.__delim_subst = delim_subst
        
        self.__URL += market.store_name()

        with open(file=self.__output_file, mode='a') : pass

        if clear_data:
            with open(file=self.__output_file, mode='w') : pass
