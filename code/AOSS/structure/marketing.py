import sys, os, time
import polars as pl
from typing import List
import multiprocessing as mpr, multiprocessing.connection as mpr_conn
from dataclasses import dataclass
import signal

#Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)


from config_paths import *
from AOSS.structure.shopping import MarketHub
from AOSS.components.processing import ProductCategorizer
from AOSS.components.processing import process_product

def custom_signal_handler(signum, frame):
    print(f"Received custom signal {signum}. Performing custom action.")


def terminate():
    exit(0)

def signal_handler(signum, frame):

    if signum == 2:
        print("Terminating marketing process...")
        terminate()


@dataclass
class ScrapeRequest():
    ID: int
    market_ID: int
    categories: List[str]



requests: List[ScrapeRequest] = []
request_ID = 1
product_df = None

def get_request_ID():
    global request_ID
    old_ID = request_ID
    request_ID += 1
    return old_ID

def __check_training_set(hub: MarketHub):
    training_market = hub.training_market()
    market_categories = training_market.categories()
    
    empty_categories = []

    # firstly we analyze whether there are any products for each category for the training market
    # if there are not, script creates a new request
    for category in market_categories:
        if len( product_df.filter( (product_df['market_ID'] == training_market.ID() ) &
                                 (product_df['query_string'] == category) )) == 0:
            
            print(f"Detected no products for training market {training_market.name()}. Category: {category}")
            empty_categories.append(category)
    
    # now we create a request if necessary
    if len(empty_categories) > 0:

        requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=training_market.ID(), categories=empty_categories))
        

        
def __check_product_sets(hub: MarketHub):
    markets = hub.markets()
    training_market = hub.training_market()
    empty_categories: List[str] = []

    for market in markets:
        if market.ID() == training_market.ID(): continue
        
        empty_categories.clear()
        market_categories = market.categories()

        for category in market_categories:
            if len( product_df.filter( (product_df['market_ID'] == market.ID() ) &
                                (product_df['query_string'] == category) )) == 0:
        
                print(f"Detected no products for market {market.name()}. Category: {category}")
                empty_categories.append(category)
        
        if len(empty_categories) > 0:            
            requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), categories=empty_categories.copy()))


def __send_scrape_request(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr.Queue, request: ScrapeRequest):
        
    while True:
        if not hub_to_scraper.full():
            hub_to_scraper.put(obj=request, block=False)
            break
        else:
            print("Unable to send scraping request!. Retrying...")
            __check_main(main_to_all=main_to_all)
            time.sleep(1)

    
    

def __check_main(main_to_all: mpr_conn.PipeConnection, timeout: int = 1):

    try:
        if main_to_all.poll(timeout=timeout) and main_to_all.recv() == "-quit":
            terminate()
    except KeyboardInterrupt:
        terminate()

        

def start_market_hub(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr.Queue,
                     scraper_to_hub: mpr.Queue):



    with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

        global product_df

        product_df = pl.read_csv(hub.product_file())

        for market in hub.markets():
            market.buffer(size=10000)

        training_market = hub.training_market()

        __check_main(main_to_all=main_to_all)
        __check_training_set(hub=hub)
        __check_product_sets(hub=hub)

        # here we start sending necessary scraping requets
        while len(requests) > 0:
            processed_request = requests.pop(0)
            __send_scrape_request(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper,
                                    request=processed_request)

            # in this loop, we wait until the request was finished successfully
            while True:
                
                if not scraper_to_hub.empty():

                    try:
                        scraped_data = scraper_to_hub.get(block=False)
                    except Exception:
                        pass

                    if isinstance(scraped_data, list):
                        print("Received scraped data! Processing...")
                        
                        for product_data in scraped_data:

                            product, market_ID = product_data
                            process_product(product=product)
                            
                            if market_ID == training_market.ID():
                                category = ProductCategorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'],
                                                        header=CATEGORY_MAP_FILE['header'])
                                
                                try:
                                    training_market.register_product(product=product, norm_category=category)
                                    print(f"Registered successfully: {{{product.name}}}")
                                except ValueError:
                                    print(f"Product {{{product.name}}} already registered!")
                            else:
                                categorizer = ProductCategorizer(market_hub=hub)
                                assert(hub.can_categorize())

                                if hub.can_categorize():
                                    
                                    start = time.time()
                                    category = categorizer.categorize(product=product)
                                    end = time.time()

                                    print(f"time:{end - start}")

                                    try:
                                        hub.market(ID=market_ID).register_product(product=product, norm_category=category)
                                        print(f"Product {product.name} registered successfully!")
                                    except ValueError:
                                        print(f"Product {product.name} already registered!")
                                

                    elif isinstance(scraped_data, int):

                        if processed_request.ID == scraped_data:
                            print(f"Request {processed_request.ID} fulfilled!")
                            hub.market(ID=processed_request.market_ID).save_products()
                            hub.load_products()
                            break
                    else:
                        print("Unsupported response type!")
                
                time.sleep(1.5)

        

            
            



                                
                                


def start(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr.Queue, 
          scraper_to_hub: mpr.Queue):
    
    os.chdir(parent_directory)
    signal.signal(signal.SIGINT, signal_handler)
    start_market_hub(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, scraper_to_hub=scraper_to_hub)




if __name__ == "__main__":
    print("Start this script as a subprocess by running start() function.")
    
 