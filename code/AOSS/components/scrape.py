
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
#from collections import OrderedDict
import time
from datetime import datetime
#import threading
from typing import List, Literal

import os, sys
import requests

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

#from AOSS.other.utils import ThreadPool
from AOSS.structure.shopping import Market
#from AOSS.other.exceptions import InvalidHTMLFormat

# ------ ProductScraper - Class Declaration&Definition ------ #

# class ProductScraper:

#     #  --- HTML STRUCTURE --- #

#     __URL = 'https://wolt.com/sk/svk/bratislava/venue/'
#     __PRICE_APPROX_SIGN = '~'
#     __CURRENCY_SIGN = '€'

#     def __init__(self,  market: Market, driver_path: str = None):
        
#         self.__market = market
#         self.__category: str = None
        
#         self.__URL += self.__market.store_name() + '/items/'

#         # Here we configure webdriver - we set Chrome options to run in headless mode
#         options = webdriver.ChromeOptions()
#         options.add_argument('--headless')

#         # If a custom webdriver was specified, we specify new service, otherwise we select the default one
#         if(driver_path):
#             self.__driver = webdriver.Chrome(service=Service(driver_path), options=options)
#         else:
#             self.__driver = webdriver.Chrome(options=options)        

#     def market(self):
#         return self.__market

#     def category(self, name: str = None, wait: int = 1.5):
#         """
#             This method serves both as a getter and setter and returns the currently processed product category.

#             When category is changed, driver requests new url and then program waits for content to load.
#         """


#         if name:

#             for category in self.__market.categories():
#                 if category == name:
#                     break
#             else:
#                 raise ValueError("Provided market doesn't contain such a category!")

#             self.__category = name
#             self.__driver.get(url=self.__URL + name)
#             time.sleep(wait)

#             if name not in self.__driver.current_url:
#                 raise ValueError(f"Failed to navigate to the requested category: {name}")
#         else:
#             return self.__category 



#     def scrape_products(self, height_pos: int = 0, wait: int = 2, console_log: bool = False, products: List[tuple[str, str, str, int]] = None):
        
#         __return = False

#         if products is None:
#             __return = True
#             products: List[tuple[str, str, str, int]] = []

#         # we scroll to the specified position and wait for page to lazy load products
#         self.__driver.execute_script(f"window.scrollTo(0, {height_pos});")
#         time.sleep(wait)

#         product_items = self.__driver.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

#         # Now we can interact with the located sub-elements
#         for item in product_items:

#             # We extract text from the desired html elements - product name and price
#             name: str = item.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text#.text.replace(self.__f_delimiter,
#                                                                                                                                 #  self.__delim_subst)
#             price: str = item.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text#.text.replace(self.__f_delimiter, 
#                                                                                                                      #            self.__delim_subst)

#             if console_log:
#                 print(f"Scraped successfully: {{name: {name}, price: {price}}}")

#             products.append((name, price, self.__category, self.__market.ID()))


#         if __return:
#             return products


#     def scrape_subcategory(self, target_label: str):

#         catalog = self.__driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
#         categories = catalog.find_elements(By.CSS_SELECTOR, ':scope > *')
        
#         target_ctg = None
        
#         for category in categories:
#             label = category.find_element(By.CLASS_NAME, 'sc-7f1dcb48-6')
#             if label.text == target_label:
#                 target_ctg = category
#                 break
#         else:
#             raise ValueError("Category with the specified label not found!")
        
#         assert(target_ctg is not None)


#         _products = OrderedDict()
        
#         while True:
#             # Find all products in the target category
#             products = target_ctg.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

#             if len(products) == 0:
#                 print("NO MORE PRODUCTS!")
#                 break
            
#             len_prev = len(_products)

#             for product in products:
#                 name = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text
#                 price = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text

#                 _products[name] = price

#                 print(name)
            
#             if len(_products) == len_prev:
#                 print("DUPLICATE PRODUCTS!")
#                 break

#             # Scroll to the next set of products
#             self.__driver.execute_script("arguments[0].scrollIntoView();", products[-1])
#             time.sleep(2)


#     def scrape_category(self, products: List[tuple[str, str, str, int]] = None, wait: int = 2, console_log: bool = False):
#         __return = False

#         if products is None:
#             products: List[tuple[str, str, str, int]] = []
#             __return = True
        

#         catalog = self.__driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
#         cur_pos = self.__driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")

#         if catalog:
#             while True:
#                 # Find all products in the target category
#                 product_items = catalog.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

#                 if len(product_items) == 0:
#                     break
                

#                 for product in product_items:
#                     name = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text
#                     price = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text
                    
#                     if console_log:
#                         print(f"Scraped successfully: {{name: {name}, price: {price}}}")

#                     products.append((name, price, self.__category, self.__market.ID()))

              
#                 # Scroll to the next set of products
#                 self.__driver.execute_script("arguments[0].scrollIntoView();", product_items[-1])
#                 new_pos = self.__driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")
                
#                 if new_pos == cur_pos:
#                     break

#                 cur_pos = new_pos
#                 time.sleep(wait)
#         else:
#             raise InvalidHTMLFormat(message="Product catalogue element not found!")
        
#         if __return:
#             return products




#     def scrape_and_quit(self, console_log: bool = False, products: List[tuple[str, str, str, int]] = None):
        
#         _return = False
#         if products is None:
#             products: List[tuple[str, str, str, int]] = []
#             _return = True
        

#         self.scrape_category(products=products, console_log=console_log)
#         self.quit()

#         if _return:
#             return products


#     def quit(self):
#         self.__driver.quit()




# class ParallelProductScraper:
    
#     def __init__(self, market: Market, driver_path: str = None, session_limit: int = 4):
        
#         self.__market = market
#         self.__driver_path = driver_path
        
#         self.__session_limit = session_limit
#         self.__scrapers: List[ProductScraper] = []
#         self.__scraper_lock = threading.Lock()

        

#         self.__buffer: List[tuple[str, str, str, int]] = []
#         self.__buffer_lock = threading.Lock()
#         self.__is_scraping_signal = threading.Event()




#     def __scrape_category(self, category: str, console_log: bool = False):
#         scraper: ProductScraper = None

#         with self.__scraper_lock:
#             scraper = self.__scrapers.pop()

#         scraper.category(name=category)
#         products = scraper.scrape_category(console_log=console_log)

#         with self.__buffer_lock:
#             self.__buffer.extend(products)
        
#         with self.__scraper_lock:
#             self.__scrapers.append(scraper)
    
#     def market(self):
#         return self.__market
    
#     def consume_buffer(self):
#         buffer_cpy: List[tuple[str, str, str, int]] = []


#         with self.__buffer_lock:
#             buffer_cpy = self.__buffer.copy()
#             self.__buffer.clear()
        
#         return buffer_cpy
    
#     def buffer_size(self):
#         with self.__buffer_lock:
#             return len(self.__buffer)
    
#     def is_scraping(self):
#         return self.__is_scraping_signal.is_set()
    


#     def __launch_threads(self, categories: tuple[str] = None, console_log: bool = False):
        
#         self.__is_scraping_signal.set()


#         with ThreadPool(self.__session_limit) as thread_pool:
            
#             if categories is not None and categories:
#                 for category in categories:
#                     thread_pool.schedule_task(task=self.__scrape_category,  category=category, console_log=console_log)
#                     time.sleep(2)
#             else:
#                 for category in self.__market.categories():
#                     thread_pool.schedule_task(task=self.__scrape_category,  category=category, console_log=console_log)
#                     time.sleep(2)
        
#             thread_pool.wait_until_complete()
        
#         self.__is_scraping_signal.clear()


#     def scrape_all(self, categories: tuple[str] = None, console_log: bool = False): 
#         if not self.__scrapers:
#             for _ in range(self.__session_limit):
#                 self.__scrapers.append(ProductScraper(market=self.__market))



#         thread = threading.Thread(target=self.__launch_threads, args=(categories, console_log))
#         thread.start()
#         time.sleep(1.5)

#     def quit(self):
#         for scraper in self.__scrapers:
#             scraper.quit()







class ProductScraper:
    """
        This class serves for effective web-scraping of Product metadata. These data are later converted into
        Product objects.

        The implementation scrapes data from web API of https://wolt.com/ publicly available at:

            https://restaurant-api.wolt.com/v4/venues/slug/

        The content is scraped in HTML format by using a python library requests.

        Attributes:

            a) market - a Market instance from which Scraper object scrapes data

            b) url - an instance-specific url string which is formed based on provided Market object

        Some global constants:

            a) BASE_URL

            b) MARKET_MENU_URL

            c) MARKET_CATEGORY_URL

        All of above compose an url of the scraped web page. Best not to modify this.


        SeeAlso:

            shopping, requests
    """

    _BASE_URL = f'https://restaurant-api.wolt.com/v4/venues/slug/'
    _MARKET_MENU_URL = "/menu"
    _MARKET_CATEGORY_URL = "/categories/slug/"

    def __init__(self, market: Market) -> None:
        """
            Creates an instance dependent on the provided Market instance.
        """

        self.__market = market
        self.__categories = market.categories()
        self.__url = ProductScraper._BASE_URL + self.__market.store_name() + ProductScraper._MARKET_MENU_URL

    def market(self):
        """
            Returns a Market instance which is used for scraping Product metadata.
        """
        return self.__market



    def scrape_categories(self, identifiers: tuple[int, ...], mode: Literal['ID', 'index'] = 'ID', products: List[tuple[Product, int]] = None,
                          console_log: bool = False):
        
        """
            This function allows filtering the scraped to only certain categories provided by the market.

            Returns
            ---
            A list of tuples in which each tuple maps the scraped product to its market.
        """

        # if isinstance(categories[0], str) and any(category not in self.__market.categories() for category in categories):
        #     raise ValueError("Provided category is not supported by the market!")
        
        _return = False

        if products is None:
            products = []
            _return = True

        market_categories: List[str] = []

        for identifier in identifiers:

            category_name = None
            category_ID = None

            if mode == 'ID':
                try:
                    for id in identifiers:
                        market_categories.append(self.__categories[identifier])
                except KeyError:
                    raise ValueError("Provided category ID not supported by this market!")
            elif mode == 'index':

                for index, value in enumerate(self.__categories.values()):
                    if index in identifiers:
                        market_categories.append(value)


            #     #try:
            #     for name, ID in self.__categories.items():

            #         if identifier == ID:
            #             market_categories[name] = ID
            #             break
            #     else:                    
            #         raise ValueError("Provided category ID not supported by this market!")

            #         #categories_str[self.__categories[category]] =  category
            #         # categories_str.append(self.__categories[category])
            #         # category_ID = category
            #     # except KeyError:
            #     #     raise ValueError("Provided category not supported by this market!")
            # elif mode == 'index':

            #     # searching for a category by an index
            #     for index, (ID, name) in enumerate(self.__categories.items()):
            #         if index == identifier:
            #             market_categories[ID] = name
            #             #categories_str.append(name)

            #             #category_name = name
            #             #category_ID = ID
            #             break
            #     else:
            #         raise IndexError("Provided category index is invalid!")
                    

            #     #category_name = self.__market.categories()[category]
            # else:
            #     raise TypeError("Unsupported type of category! Must be either string or integer!")


        #url = self.__url + ProductScraper._MARKET_CATEGORY_URL + category_name
        response = requests.get(self.__url)

        if response.status_code == 200:
            data = response.json()

            for item in data['items']:
                
                category_ID = item.get('category')
                category_name = None

                for identifier in data['categories']:
                    if identifier['id'] == category_ID:
                        category_name = identifier['slug']
                        break
                
                if not category_name in market_categories:
                    if console_log:
                        print(f"Category {category_name} filtered out!")
                    continue
                
                category_ID = None
                for key, value in self.__categories.items():
                    if value == category_name:
                        category_ID = key
                        break
                
                quantity_left=item.get('quantity_left')

                if quantity_left is None:
                    quantity_left = 0
                


                new_product = Product(
                    name=item.get('name', 'unknown'),
                    price=int(item.get('baseprice', -1)) / 100,
                    approximation=0,
                    quantity_left=quantity_left,
                    category_ID=category_ID,
                    created_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

                products.append( (new_product, self.__market.ID()) )
                
                if console_log:
                    print(f"Scraped successfully: {new_product}")

        else:
            raise ConnectionRefusedError(f"Received invalid status code: {response.status_code}")
        
        if _return:
            return products

    # def get_categories(self):
    #     url = self.__url
    #     response = requests.get(url)

    #     if response.status_code == 200:
    #         data = response.json()

    #         for category in data['categories']:
                
    #             print(category.get('slug'))



    def scrape_all(self, products: List[Product] = None, console_log: bool = False):
        
        _return = False

        if products is None:
            _return = True
            products = []
        

       # url = self.__url + ProductScraper._MARKET_CATEGORY_URL + category_name
        response = requests.get(self.__url)

        if response.status_code == 200:
            data = response.json()

            for item in data['items']:
                category_ID = item.get('category')
                category_name = None

                for category in data['categories']:
                    if category['id'] == category_ID:
                        category_name = category['slug']
                        break
                
                if not category_name in self.__categories.values():
                    if console_log:
                        print(f"Category {category_name} not supported by current market! Skipping...")
                    continue

                category_ID = None
                for key, value in self.__categories.items():
                    if value == category_name:
                        category_ID = key
                        break

                quantity_left=item.get('quantity_left')

                if quantity_left is None:
                    quantity_left = 0

                new_product = Product(
                    name=item.get('name', 'unknown'),
                    price=int(item.get('baseprice', -1)) / 100,
                    approximation=0,
                    quantity_left=quantity_left,
                    category_ID=category_ID,
                    created_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    updated_at=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))

                products.append( (new_product, self.__market.ID()) )
                
                if console_log:
                    print(f"Scraped successfully: {new_product}")

        else:
            raise ConnectionRefusedError(f"Received invalid status code: {response.status_code}")

        if _return:
            return products
        
        #return self.scrape_categories(categories=self.__market.categories(), console_log=console_log)
        # products: List[tuple[Product, int]] = []

        # self.scrape_categories(categories=self.__market.categories(), products=products, console_log=console_log)

        # # for category in categories:
        # #     self.scrape_categories(categories=(category,), products=products, console_log=console_log)

        # return products
        #return Scraper.__scrape_products(url=self.__url)


    

if __name__ == "__main__":
    print("Nothing to execute...")
