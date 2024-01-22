from marketing import Market, Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from collections import OrderedDict
import time
import threading
from typing import List, Dict
from utils import ThreadPool



# ------ ProductScraper - Class Declaration&Definition ------ #

class ProductScraper:

    #  --- HTML STRUCTURE --- #

    __URL = 'https://wolt.com/sk/svk/bratislava/venue/'
    __PRICE_APPROX_SIGN = '~'
    __CURRENCY_SIGN = '€'

    def __init__(self,  market: Market, driver_path: str = None, substition: Dict[str, str] = {",": "."}, clear_data: bool = False, session_limit: int = 4):
        
        self.__market = market
        self.__session_limit = session_limit
        self.__substitution = substition
        
        self.__URL += market.store_name() + '/items/'
        self.__MARKET_LOCK = threading.Lock()

        # Here we configure webdriver
        # Set Chrome options to run in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')

        if(driver_path):
            self.__driver = webdriver.Chrome(service=Service(driver_path), options=options)
        else:
            self.__driver = webdriver.Chrome(options=options)

            
    def __scrape_products(self, height_pos: int, sleep_: int = 3, _print: bool = False, products: List[Product] = None) -> None:
        self.__driver.execute_script(f"window.scrollTo(0, {height_pos});")
        time.sleep(sleep_)

        product_entries = self.__driver.find_elements(By.CSS_SELECTOR, '.sc-a8239ffe-4.gOfKkf')

        # Now we can interact with the located sub-elements
        for index, entry in enumerate(product_entries):

            # We extract text from the desired html elements - product name and price
            name: str = entry.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text#.text.replace(self.__f_delimiter,
                                                                                                                                #  self.__delim_subst)
            price: str = entry.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text#.text.replace(self.__f_delimiter, 
                                                                                                                     #            self.__delim_subst)
            
            # We process data by replacing string parts with desired ones 
            for key, value in self.__substitution.items():
                name = name.replace(key, value)
                price = price.replace(key, value)

            
            approximation = 0

            # Here we check whether the price is just an approximate value
            if(price[0] == self.__PRICE_APPROX_SIGN):
                price = price[1:]
                approximation = 1
            
            # We remove the potential price approximation sign from the price text
            price = price.split(self.__CURRENCY_SIGN)[0].strip()
            
            new_product = Product(name=name, price=float(price), approximation=approximation)

            if _print:
                print("Scraped successfully:", end=" ")
                new_product.__str__()

            if products is not None:
                products.append(new_product)


    def scrape_category(self, category: str, scrolldown: int = 2000, register: bool = False, _print: bool = False, signal: threading.Event = None,
                        products: List[Product] = None) -> None:

        if category not in self.__market.categories():
            raise ValueError("Specified category not found!")
        
        
        self.__driver.get(url=self.__URL + category)

        cur_height_pos = 0
        total_height = self.__driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        
        _products = OrderedDict()

        while cur_height_pos < total_height:

            product_data: List[Product] = []        

            self.__scrape_products(height_pos=cur_height_pos,  sleep_=1.5, _print=_print, products=product_data)
            cur_height_pos += scrolldown
            
            for product in product_data:
                _products[product.name()] = product


        if signal:
            print("Setting signal...")
            signal.set()

        if register:
            
            for product in _products.values():
                product.category(category=category)

                with self.__MARKET_LOCK:
                    try:
                        self.__market.for_registration(product=product)
                        #self.__market.register_products(product=product)
                    except ValueError:
                        if _print:
                            print("Product already registered: " + str(product.ID()) + ',' + ' ' + product.name())

                        
        
        if products is not None:
            products.extend(list(_products.values()))


    def scrape_and_quit(self, category: str, scrolldown: int = 2000, register: bool = False, print_: bool = False, products: List[Product] = None):
        self.scrape_category(category=category, scrolldown=scrolldown, register=register, _print=print_, products=products)
        self.quit()



    def scrape_all(self, register: bool = False, _print: bool = False, products: List[Product] = None) -> None: 
        threads: List[threading.Thread] = []
        products: List[Product] = []

        with ThreadPool(self.__session_limit) as thread_pool:

            for category in self.__market.categories():
                

                scraper = ProductScraper(market=self.__market)
                thread_pool.schedule_task(task=scraper.scrape_and_quit, category=category, scrolldown=2000, register=register, print_=_print,
                                          products=products)
            
     
            thread_pool.wait_until_complete()
        

    def quit(self):
        self.__driver.quit()

    # Function to get the total scroll height using JavaScript
    #def get_total_scroll_height(self, _driver):
     #   return _driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")



# ------ GlobalProductScraper - Class Declaration&Definition ------ #
    

# class GlobalProductScraper:
#     def __init__(self, market: Market, session_limit: int = 4) -> None:
#         self.__market = market
#         self.__session_limit = session_limit
    
#     def drop_session_if_dead(self, sessions: List[ProductScraper], signal_handler: SignalHandler):
#         print("IM here!")
#         session_index = signal_handler.pop_first_complete()

#         if(session_index > -1):
#             print(f"Session: {session_index} was completed! Quitting...")
#             sessions[session_index].quit()
#             sessions.pop(session_index)
        


#     def scrape_all(self, scrolldown: int = 2000, register: bool = False, print_: bool = False):
#         scrapers: List[ProductScraper] = []

#         with ThreadPool(self.__session_limit) as thread_pool: 
#             markets = self.__market.markets()

#             market_stop_signals: List[threading.Event] = []
#             signal_handler = SignalHandler()
        

#             for market in markets:
#                 scraper = ProductScraper(market=market)
#                 scrapers.append(scraper)

#                 for category in market.categories():
#                     signal = threading.Event()

#                     thread_pool.schedule_task(task=scraper.scrape_category, category=category, scrolldown=scrolldown, register=register, print_=print_, signal=signal)
#                     market_stop_signals.append(signal)

#                 signal_handler.add_group(group=market_stop_signals)
                
#                 #scraper.quit()

#             print("WAITING...")
#             thread_pool.wait_until_complete(task=self.drop_session_if_dead, sessions=scrapers, signal_handler=signal_handler)
        
#         for scraper in scrapers:
#             scraper.quit()


#     def scrape_category(self, category: str, scrolldown: int = 2000, register: bool = False, print_: bool = False):
#         with ThreadPool(self.__session_limit) as thread_pool: 
#             markets = self.__market.markets()

#             for market in markets:
#                 scraper = ProductScraper(market=market)

#                 # for category in market.categories():
#                 thread_pool.schedule_task(task=scraper.scrape_category, category=category, scrolldown=scrolldown, register=register, print_=print_)
                
#                 scraper.quit()
            
#             thread_pool.wait_until_complete()


if __name__ == "__main__":
    print("Nothing to execute...")
