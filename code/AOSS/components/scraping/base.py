
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from collections import OrderedDict
import time
import threading
from typing import List

import os, sys

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)

from AOSS.structure.shopping import Market, Product

from AOSS.other.utils import ThreadPool
from AOSS.structure.shopping import Market

# ------ ProductScraper - Class Declaration&Definition ------ #

class ProductScraper:

    #  --- HTML STRUCTURE --- #

    __URL = 'https://wolt.com/sk/svk/bratislava/venue/'
    __PRICE_APPROX_SIGN = '~'
    __CURRENCY_SIGN = '€'

    def __init__(self,  market: Market, driver_path: str = None):
        
        self.__market = market
        self.__category: str = None
        
        self.__URL += self.__market.store_name() + '/items/'

        # Here we configure webdriver - we set Chrome options to run in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        # If a custom webdriver was specified, we specify new service, otherwise we select the default one
        if(driver_path):
            self.__driver = webdriver.Chrome(service=Service(driver_path), options=options)
        else:
            self.__driver = webdriver.Chrome(options=options)        

    def market(self):
        return self.__market

    def category(self, name: str = None, wait: int = 1.5):
        """
            This method serves both as a getter and setter and returns the currently processed product category.

            When category is changed, driver requests new url and then program waits for content to load.
        """


        if name:

            for category in self.__market.categories():
                if category == name:
                    break
            else:
                raise ValueError("Provided market doesn't contain such a category!")

            self.__category = name
            self.__driver.get(url=self.__URL + name)
            time.sleep(wait)

            if name not in self.__driver.current_url:
                raise ValueError(f"Failed to navigate to the requested category: {name}")
        else:
            return self.__category 



    def scrape_products(self, height_pos: int = 0, wait: int = 2, console_log: bool = False, products: List[tuple[str, str, str]] = None):
        
        __return = False

        if products is None:
            __return = True
            products: List[tuple[str, str, str]] = []

        # we scroll to the specified position and wait for page to lazy load products
        self.__driver.execute_script(f"window.scrollTo(0, {height_pos});")
        time.sleep(wait)

        product_items = self.__driver.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

        # Now we can interact with the located sub-elements
        for item in product_items:

            # We extract text from the desired html elements - product name and price
            name: str = item.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text#.text.replace(self.__f_delimiter,
                                                                                                                                #  self.__delim_subst)
            price: str = item.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text#.text.replace(self.__f_delimiter, 
                                                                                                                     #            self.__delim_subst)

            if console_log:
                print(f"Scraped successfully: {{name: {name}, price: {price}}}")

            products.append((name, price, self.__category, ))


        if __return:
            return products


    def scrape_subcategory(self, target_label: str):

        catalog = self.__driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
        categories = catalog.find_elements(By.CSS_SELECTOR, ':scope > *')
        
        target_ctg = None
        
        for category in categories:
            label = category.find_element(By.CLASS_NAME, 'sc-7f1dcb48-6')
            if label.text == target_label:
                target_ctg = category
                break
        else:
            raise ValueError("Category with the specified label not found!")
        
        assert(target_ctg is not None)


        _products = OrderedDict()
        
        if target_ctg:
            while True:
                # Find all products in the target category
                products = target_ctg.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

                if len(products) == 0:
                    print("NO MORE PRODUCTS!")
                    break
                
                len_prev = len(_products)

                for product in products:
                    name = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text
                    price = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text

                    _products[name] = price

                    print(name)
                
                if len(_products) == len_prev:
                    print("DUPLICATE PRODUCTS!")
                    break

                # Scroll to the next set of products
                self.__driver.execute_script("arguments[0].scrollIntoView();", products[-1])
                time.sleep(2)
        else:
            print("Target category not found.")

    def scrape_category(self, products: List[tuple[str, str, str]] = None, wait: int = 2, console_log: bool = False):
        __return = False

        if products is None:
            products: List[tuple[str, str, str]] = []
            __return = True
        

        catalog = self.__driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
        cur_pos = self.__driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")

        if catalog:
            while True:
                # Find all products in the target category
                product_items = catalog.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

                if len(product_items) == 0:
                    print("NO MORE PRODUCTS!")
                    break
                

                for product in product_items:
                    name = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text
                    price = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text
                    
                    if console_log:
                        print(f"Scraped successfully: {{name: {name}, price: {price}}}")

                    products.append((name, price, self.__category))

              
                # Scroll to the next set of products
                self.__driver.execute_script("arguments[0].scrollIntoView();", product_items[-1])
                new_pos = self.__driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")
                
                if new_pos == cur_pos:
                    print("Finishing!")
                    break

                cur_pos = new_pos
                time.sleep(wait)
        else:
            print("Target category not found.")
        
        if __return:
            return products




    def scrape_and_quit(self, console_log: bool = False, products: List[tuple[str, str, str]] = None):
        
        _return = False
        if products is None:
            products: List[tuple[str, str, str]] = []
            _return = True
        

        self.scrape_category(products=products, console_log=console_log)
        self.quit()

        if _return:
            return products


    def quit(self):
        self.__driver.quit()




class ParallelProductScraper:
    def __init__(self, market: Market, driver_path: str = None, session_limit: int = 4):
        
        self.__market = market
        self.__driver_path = driver_path
        self.__session_limit = session_limit

        self.__buffer: List[tuple[str, str, str]] = []
        self.__buffer_lock = threading.Lock()
        self.__is_scraping_signal = threading.Event()




    def __scrape_category(self, category: str, console_log: bool = False):
        print("Executing...")
        scraper = ProductScraper(market=self.__market, driver_path=self.__driver_path)
        scraper.category(name=category)
        
        products = scraper.scrape_and_quit(console_log=console_log)

        with self.__buffer_lock:
            self.__buffer.extend(products)
    
    def market(self):
        return self.__market
    
    def consume_buffer(self):
        buffer_cpy: List[tuple[str, str, str]] = []


        with self.__buffer_lock:
            buffer_cpy = self.__buffer.copy()
            self.__buffer.clear()
        
        return buffer_cpy
    
    def buffer_size(self):
        with self.__buffer_lock:
            return len(self.__buffer)
    
    def is_scraping(self):
        return self.__is_scraping_signal.is_set()
    


    def __launch_threads(self, categories: tuple[str] = None, console_log: bool = False):
        
        self.__is_scraping_signal.set()

        with ThreadPool(self.__session_limit) as thread_pool:
            
            if categories is not None and categories:
                for category in categories:
                    thread_pool.schedule_task(task=self.__scrape_category,  category=category, console_log=console_log)
                    time.sleep(2)
            else:
                for category in self.__market.categories():
                    thread_pool.schedule_task(task=self.__scrape_category,  category=category, console_log=console_log)
                    time.sleep(2)
        
            thread_pool.wait_until_complete()
        
        self.__is_scraping_signal.clear()


    def scrape_all(self, categories: tuple[str] = None, console_log: bool = False): 

        thread = threading.Thread(target=self.__launch_threads, args=(categories, console_log))
        thread.start()
        time.sleep(1.5)

            
if __name__ == "__main__":
    print("Nothing to execute...")
