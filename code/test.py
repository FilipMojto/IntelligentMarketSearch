from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from typing import OrderedDict
import AOSS.structure.shopping as shp
import AOSS.components.product_scraping as scrp
from config_paths import *
from AOSS.components.product_processing import *
from AOSS.structure.shopping import MarketHub, Market
import polars as pl

from datetime import datetime

current_timestamp = time.time()
formatted_timestamp = datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
print("Formatted Timestamp:", formatted_timestamp)


def scrape_market(market: Market):

    scraper = scrp.ParallelProductScraper(market=market, session_limit=5)

    scraper.scrape_all(console_log=True)

    while(not scraper.is_finished()):
        time.sleep(5)

        if scraper.buffer_size() >= 500:
            product_data = scraper.consume_buffer()

            products = process_scraped_products(products=product_data)

            for product in products:
                categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'],
                                   header=QUERY_STRING_FILE['header'])
                
                try:
                    market.for_registration(product=product)
                    print(f"Market {market} registered successfully!")
                except ValueError:
                    print(f"Market: {market} already in the dataset!")

    market.register_products()

with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

    market = hub.markets()[2]

    market.buffer(size=500)

    scrape_market(market)

    # scraper = scrp.ParallelProductScraper(market=market, session_limit=5)

    # scraper.scrape_all(console_log=True)

    # while(not scraper.is_finished()):
    #     time.sleep(5)

    #     if scraper.buffer_size() >= 500:
    #         product_data = scraper.consume_buffer()

    #         products = process_scraped_products(products=product_data)

    #         for product in products:
    #             categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'],
    #                                header=QUERY_STRING_FILE['header'])
                
    #             market.for_registration(product=product)
    
    # market.register_products()




#product = Product(name="NIKECO", price=1.54, approximation=0, category="hotove-jedla-159")

#categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'], header=QUERY_STRING_FILE['header'])

# from datetime import datetime

# current_timestamp = time.time()
# formatted_timestamp = datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d %H:%M:%S')
# print("Formatted Timestamp:", formatted_timestamp)

#print(dataset)


# def process(products, market: Market):

#     products = process_scraped_products(products=products, category=market.categories()[0])
    
#     for product in products:
#         product = categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'], header=CATEGORY_FILE['header'])

#     for product in products:
#         try:
#             market.for_registration(product)
#         except ValueError:
#             print(f"Product: {product.__str__()} already registered!")

# with MarketHub(src_file="./resources/data/market_hub.csv", header=True) as hub:
    
#     markets = hub.markets()
    
#     market = markets[2]
#     market.buffer(size=500)
    
#     scraper = scrp.ParallelProductScraper(market=market, session_limit=5)

#     scraper.scrape_all(console_log=True)

#     while not scraper.is_finished():

#         time.sleep(5)

#         if scraper.buffer_size() >= 500:
#             product_data = scraper.consume_buffer()


#             products = process_scraped_products(products=product_data)

#             for product in products:
#                 categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'], header=QUERY_STRING_FILE['header'])
                
#                 try:
#                     market.for_registration(product=product)
#                     print(f"Product {product} registered successfully!")
#                 except ValueError:
#                     print(f"Product {product} already registered!")
#     market.register_products()

    # for category in market.categories():

    #     scraper.category(name=category)
    #     product_data = scraper.scrape_category(console_log=True)
    #     products = process_scraped_products(product_data, category=category)
        
    #     for product in products:
    #         categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'], header=QUERY_STRING_FILE['header'])
            
    #         try:
    #             market.for_registration(product=product)
    #             print(f"Product {product} registered successfully!")
    #         except ValueError:
    #             print(f"Product {product} already registered!")
    
    #     market.register_products()
    # for category in market.categories():
    #     scraper.category(name=category)

    #     products = scraper.scrape_category(console_log=True)
        
    #     products = process_scraped_products(products=products, category=category)
        
    #     for product in products:
    #         product = categorize_product(product=product, categories_file=QUERY_STRING_FILE['path'],
    #                                      header=QUERY_STRING_FILE['header'])
            
    #         try:
    #             market.for_registration(product=product)
    #             print(f"Product {product} registered successfully!")
    #         except ValueError:
    #             print(f"Product {product} already registered!")
            
    # market.register_products()

exit(0)


# options = webdriver.ChromeOptions()
# # options.add_argument('--headless')

# driver = webdriver.Chrome(options=options)
# driver.get("https://wolt.com/sk/svk/bratislava/venue/billa-segnerova/items/ovocie-zelenina-103")

# # Wait for some time to make sure the page is loaded
# time.sleep(5)

# def find_target_category(target_label: str):
#     catalog = driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
#     categories = catalog.find_elements(By.CSS_SELECTOR, ':scope > *')
    
#     target_ctg = None
    
#     for category in categories:
#         label = category.find_element(By.CLASS_NAME, 'sc-7f1dcb48-6')
#         if label.text == target_label:
#             target_ctg = category
#             break
#     else:
#         raise ValueError("Category with the specified label not found!")
    
#     assert(target_ctg is not None)

# catalog = driver.find_element(By.CSS_SELECTOR, '[data-test-id="productCatalog.productCategoryScreen"]')
# _products = OrderedDict()

# if catalog:

#     cur_pos = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")

#     while True:
#         # Find all products in the target category
#         products = catalog.find_elements(By.CSS_SELECTOR, '[data-test-id="ItemCard"]')

#         # if len(products) == 0:
#         #     print("NO MORE PRODUCTS!")
#         #     break
        
#         len_prev = len(_products)

#         for product in products:
#             name = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCard.Title"]').text
#             price = product.find_element(By.CSS_SELECTOR, '[data-test-id="ImageCentricProductCardPrice"]').text

#             _products[name] = price

#             print(name)
        
#         # if len(_products) == len_prev:
#         #     print("DUPLICATE PRODUCTS!")
#         #     break

#         # Scroll to the next set of products
#         driver.execute_script("arguments[0].scrollIntoView();", products[-1])
#         new_pos = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;")

#         if cur_pos == new_pos:
#             print("Stopping!")
#             break

#         cur_pos = new_pos

#         time.sleep(2)
# else:
#     print("Target category not found.")




# #Close the WebDriver
# driver.quit()