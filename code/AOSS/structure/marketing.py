import sys, os, time
import polars as pl
from typing import List
import multiprocessing as mpr, multiprocessing.connection as mpr_conn
from dataclasses import dataclass
import signal
from datetime import datetime
import math

import concurrent.futures

#Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)


from config_paths import *
from AOSS.structure.shopping import MarketHub, Market, ProductCategory
from AOSS.components.processing import ProductCategorizer
from AOSS.components.processing import process_product
from AOSS.other.exceptions import IllegaProductState

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
    categories: List[int]



requests: List[ScrapeRequest] = []
request_ID = 1
product_df = None

GUI_START_SIGNAL = 100

def get_request_ID():
    global request_ID
    old_ID = request_ID
    request_ID += 1
    return old_ID

# def __check_training_set(hub: MarketHub):
#     training_market = hub.training_market()
#     market_categories = training_market.categories()
    
#     empty_categories = []

#     # firstly we analyze whether there are any products for each category for the training market
#     # if there are not, script creates a new request
#     for category in market_categories:
#         if len( product_df.filter( (product_df['market_ID'] == training_market.ID() ) &
#                                  (product_df['query_string'] == category) )) == 0:
            
#             print(f"Detected no products for training market {training_market.name()}. Category: {category}")
#             empty_categories.append(category)
    
#     # now we create a request if necessary
#     if len(empty_categories) > 0:

#         requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=training_market.ID(), categories=empty_categories))
        

        
# def __check_product_sets(hub: MarketHub):
#     markets = hub.markets()
#     training_market = hub.training_market()
#     empty_categories: List[str] = []

#     for market in markets:
#         if market.ID() == training_market.ID(): continue
        
#         empty_categories.clear()
#         market_categories = market.categories()

#         for category in market_categories:
#             if len( product_df.filter( (product_df['market_ID'] == market.ID() ) &
#                                 (product_df['query_string'] == category) )) == 0:
        
#                 print(f"Detected no products for market {market.name()}. Category: {category}")
#                 empty_categories.append(category)
        
#         if len(empty_categories) > 0:            
#             requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), categories=empty_categories.copy()))


def send_or_wait(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr.Queue, request: ScrapeRequest):
    """
        Attempts to send a ScrapeRequest instance via hub-to-scraper Queue. If the request was not sent
        because the queue is full it waits some time before trying again. Basically this function loops
        until the message is sent successfully or it receives termination signal from the main process.
    """

    while True:
        if not hub_to_scraper.full():
            hub_to_scraper.put(obj=request, block=False)
            break
        else:
            print("Unable to send scraping request!. Retrying...")
            check_main(main_to_all=main_to_all)
            time.sleep(1)

    
    

def check_main(main_to_all: mpr.Queue, timeout: int = 1):
    """
        Checks for some predefined signals which might be sent by the main process, like termination signal.

        If termination signal was received, process terminates by executing termination function.
    """


    try:
        if not main_to_all.empty() and main_to_all.get(block=False) == "-quit":
            terminate()

        # sig = main_to_all.get(block=False, timeout=timeout)
        # if sig == "-quit":
        #     terminate()

        #if main_to_all.poll(timeout=timeout) and main_to_all.recv() == "-quit":
           # terminate()
    except KeyboardInterrupt:
        terminate()

    

import threading

market_hub_lock = threading.Lock()


def categorize_product(market_hub: MarketHub, market_ID: int, product):
    categorizer = None

    with market_hub_lock:
        categorizer = ProductCategorizer(market_hub=market_hub)

    start = time.time()
    category =  categorizer.categorize(product=product)
    end = time.time()

    print(f"Time: {end - start}")

    try:
        market_hub.market(identifier=market_ID).register_product(product=product, norm_category=category)
        print(f"Product {product.name} registered successfully!")
    except IllegaProductState:
        print(f"Product {product.name} already registered!")


# def start_market_hub(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr.Queue,
#                      scraper_to_hub: mpr.Queue, hub_to_gui: mpr.Queue):



#     with MarketHub(src_file=MARKET_HUB_FILE['path']) as hub:

#         global product_df
#         product_df = pl.read_csv(hub.product_file())

#         for market in hub.markets():
#             market.buffer(size=10000)

#         training_market = hub.training_market()

#         __check_main(main_to_all=main_to_all)

        
#         market_categories = training_market.categories()
        
#         empty_categories = []



#         # firstly we analyze whether there are any products for each category for the training market
#         # if there are not, script creates a new request
#         for category in market_categories:
#             if len( product_df.filter( (product_df['market_ID'] == training_market.ID() ) &
#                                     (product_df['query_string'] == category) )) == 0:
                
#                 print(f"Detected no products for training market {training_market.name()}. Category: {category}")
#                 empty_categories.append(category)
        
#         # now we create a request if necessary
#         if len(empty_categories) > 0:

#             requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=training_market.ID(), categories=empty_categories))




#         #__check_training_set(hub=hub)
#         __check_product_sets(hub=hub)

#         # here we start sending necessary scraping requets
#         while len(requests) > 0:
#             processed_request = requests.pop(0)
#             __send_scrape_request(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper,
#                                     request=processed_request)

#             # in this loop, we wait until the request was finished successfully
#             while True:
                
#                 if not scraper_to_hub.empty():

#                     try:
#                         scraped_data = scraper_to_hub.get(block=False)
#                     except Exception:
#                         pass

#                     if isinstance(scraped_data, list):
#                         print("Received scraped data! Processing...")
                        
#                         with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
#                             futures = []

#                             for product_data in scraped_data:

#                                 product, market_ID = product_data
#                                 process_product(product=product)
                                
#                                 if market_ID == training_market.ID():
#                                     category = ProductCategorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'],
#                                                             header=CATEGORY_MAP_FILE['header'])
                                    
#                                     try:
#                                         training_market.register_product(product=product, norm_category=category)
#                                         print(f"Registered successfully: {{{product.name}}}")
#                                     except IllegalProductStructureError:
#                                         print(f"Product {{{product.name}}} already registered!")
#                                 else:
#                                     #categorizer = ProductCategorizer(market_hub=hub)
#                                     assert(hub.can_categorize())

#                                     if hub.can_categorize():
                                        
#                                         # start = time.time()
                                
#                                         future = executor.submit(categorize_product, hub, market_ID, product)
#                                         futures.append(future)
#                                         # category = categorizer.categorize(product=product)
#                                         # end = time.time()

#                                         # print(f"time:{end - start}")

#                                         # try:
#                                         #     hub.market(ID=market_ID).register_product(product=product, norm_category=category)
#                                         #     print(f"Product {product.name} registered successfully!")
#                                         # except IllegalProductStructureError:
#                                         #     print(f"Product {product.name} already registered!")
                            
#                             concurrent.futures.wait(futures)

#                     elif isinstance(scraped_data, int):

#                         if processed_request.ID == scraped_data:
#                             print(f"Request {processed_request.ID} fulfilled!")
#                             hub.market(ID=processed_request.market_ID).save_products()
#                             hub.update()
#                             hub.load_products()
#                             break
#                     else:
#                         print("Unsupported response type!")
                
#                 time.sleep(1.5)

#         if not hub_to_gui.full():
#             hub_to_gui.put(obj=GUI_START_SIGNAL, block=False)
#         else:
#             print("Unable to send scraping request!. Retrying...")
#             __check_main(main_to_all=main_to_all)
#             #time.sleep(1)

        
def notify_gui(hub_to_gui: mpr.Queue, main_to_all: mpr.Queue, progress: int):
    assert(0<=progress<=GUI_START_SIGNAL)

    while hub_to_gui.full():
        print("Gui process queue full! Retrying...")
        check_main(main_to_all=main_to_all)
    
    hub_to_gui.put(progress, block=False)





            
            



                                
def analyze_market(market: Market):
    """
        Analyzes provided market by searching registered products for each category. If category contains
        no such products it inserts it into the SrapeRequest's empty categories buffer.

        Global product dataframe is used to filter our analyzed market and its categories.

        New ScrapeRequest instance is only added to the global request buffer should at least one empty category
        was found.
    """

    categories = market.categories()
    empty_categories = []

    for name, ID in categories.items():
        if len( product_df.filter( (product_df['market_ID'] == market.ID() ) &
                                (product_df['query_string_ID'] == ID) )) == 0:
            
            print(f"Detected no products for market {market.name()}. Category: {name}")
            empty_categories.append(ID)
        
    # now we create a request if needed
    if empty_categories:
        requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), categories=empty_categories))


def analyze_product(row):
    print(row[PRODUCT_FILE['columns']['updated_at']['index']])



def start(main_to_all: mpr.Queue, hub_to_scraper: mpr.Queue, 
          scraper_to_hub: mpr.Queue, hub_to_gui: mpr.Queue,
          product_file_lock: mpr.Lock):
          
    
    os.chdir(parent_directory)
    signal.signal(signal.SIGINT, signal_handler)
    #start_market_hub(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, scraper_to_hub=scraper_to_hub, hub_to_gui=hub_to_qui)

    hub = MarketHub(src_file=MARKET_HUB_FILE['path'])   
    hub.load_markets()

    with product_file_lock:
        hub.load_products()

    #with MarketHub(src_file=MARKET_HUB_FILE['path']) as hub:
    hub.update()
    markets = hub.markets()
    
    for market in markets:
        market.buffer(size=10000)

    global product_df
    product_df = hub.product_df() # pl.read_csv(hub.product_file())

    check_main(main_to_all=main_to_all)

    training_market = hub.training_market()
    analyze_market(market=training_market)
    
    notify_gui(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=GUI_START_SIGNAL/4)


    for market in markets:
        if market.ID() == training_market.ID(): continue
        analyze_market(market=market)
    
    notify_gui(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=GUI_START_SIGNAL/2)

    progress = GUI_START_SIGNAL/2
    
    if requests:
        progress_rate = math.floor(progress/len(requests))

    # here we start sending  scraping requets
    while requests:
        processed_request = requests.pop(0)
        send_or_wait(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, request=processed_request)

        # in this loop, we wait until the request was finished successfully
        while True:
            if not scraper_to_hub.empty():

                try:
                    scraped_data = scraper_to_hub.get(block=False)
                except Exception:
                    pass

                if isinstance(scraped_data, list):
                    print("Received scraped data! Processing...")
                    
                    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                        futures = []

                        for product_data in scraped_data:

                            product, market_ID = product_data
                            market = hub.market(identifier=market_ID)

                            process_product(product=product)
                            category = ProductCategory.NEURČENÁ
                            if market_ID == training_market.ID():
                                category = ProductCategorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'])
                            
                            try:
                                market.register_product(product=product, norm_category=category)
                                print(f"Registered successfully: {{{product.name}}}")
                            except IllegaProductState:
                                print(f"Product {{{product.name}}} already registered!")
                            
                            # try:
                            #     training_market.register_product(product=product, norm_category=category)
                            #     print(f"Registered successfully: {{{product.name}}}")
                            # except IllegaProductState:
                            #     print(f"Product {{{product.name}}} already registered!")


                    
                                #future = executor.submit(categorize_product, hub, market_ID, product)
                                #futures.append(future)
            
                        
                        #concurrent.futures.wait(futures)

                elif isinstance(scraped_data, int):

                    if processed_request.ID == scraped_data:
                        print(f"Request {processed_request.ID} fulfilled!")

                        with product_file_lock:
                            hub.market(identifier=processed_request.market_ID).save_products()
                        
                        hub.update()

                        with product_file_lock:
                            hub.load_products()
                        notify_gui(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=progress + progress_rate)
                        progress += progress_rate
                        break
                else:
                    print("Unsupported response type!")
            
            time.sleep(1.5)


    notify_gui(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=GUI_START_SIGNAL)

    # now gui can start, since all necessary data are present   
    while hub_to_gui.full():
        print("Unable to send scraping request!. Retrying...")
        check_main(main_to_all=main_to_all)

    #hub_to_gui.put(obj=GUI_START_SIGNAL, block=False)
    




    print("Starting update process...")
    processed_categories: List[int] = []
    
    categorizer = ProductCategorizer(market_hub=hub)

    while True:
        # we update product_df to get latest version of dataframe
        product_df = hub.product_df()

        # we find the earliest updated record in dataframe
        # Get the first row
        sorted_df = product_df.sort('updated_at')
        first_row = sorted_df.filter(sorted_df['query_string_ID'].is_in(processed_categories).not_()).head(1)
        market = first_row['market_ID']
        processed_categories.append(first_row['query_string_ID'][0])

        category_products = product_df.filter(product_df['query_string_ID'] == first_row['query_string_ID'])['name'].to_list()
        
        #first_row = sorted_df.row(by_predicate=lambda x : x['query_string'] not in processed_categories)




        # for row in sorted_df.iter_rows(named=True):
        #     if row['query_string'] not in processed_categories:
        #         #here I need to store the reference to this row
        #         processed_categories.append(row['query_string'])
        #         sorted_df.row()



        #first_row = sorted_df.head(1)

        # Print the content of the first row
        print(f"Updating category {first_row['query_string_ID'][0]} of market {first_row['market_ID'][0]}.")
    

        # now we create a ScrapeRequest isntance and send it to the scraper process
        processed_request = ScrapeRequest(ID=get_request_ID(), market_ID=first_row['market_ID'][0], categories=[first_row['query_string_ID'][0]])
        
        with product_file_lock:
            hub.market(identifier=processed_request.market_ID).load_products()
        
        send_or_wait(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, request=processed_request)

        # here we wait until the request is fulfilled
        while True:
            # here we wait until we receive and answer
            while scraper_to_hub.empty():
                check_main(main_to_all=main_to_all)

            response = scraper_to_hub.get(block=False)

            # case in which we should receive updated product data
            if isinstance(response, list):
                print("Received scraped data! Processing...")
                
                for product, market_ID in response:
                    process_product(product=product)

                    if market_ID == processed_request.market_ID:
                        market = hub.market(identifier=market_ID)
                        try:
                            market.update_product(product=product)

                            try:
                                category_products.remove(product.name)
                            except ValueError:
                                pass


                        # we received a new data which are not yet registered
                        except IllegaProductState:
                            
                            if market.ID() == training_market.ID():
                                category = categorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'])
                            else:
                                category = categorizer.categorize(product=product)

                            process_product(product=product)
                            try:
                                
                                market.register_product(product=product, norm_category=category)
                                print(f"Registered successfully: {{{product.name}}}")
                            except IllegaProductState:
                                print(f"Product {{{product.name}}} already registered!")

                    else:
                        print("Received response contains invalid market ID!")
            
            # case in which we should receive the ScrapeProcessTerminationSignal
            elif isinstance(response, int):
                
                # here all updated data have to be saved to the product file and market hub
                # has to be refreshed
                if processed_request.ID == response:
                    market = hub.market(identifier=processed_request.market_ID)
                    #if market.

                    if category_products:
                        market.remove_products(products=category_products)
                    

                    print(f"Request {processed_request.ID} fulfilled!")
                    #market.save_products()

                    with product_file_lock:
                        market.save_products()
                        hub.load_products()
                    break
                else:
                    print("Received invalid Scrape Process Termination Signal!")
            else:
                print("Unsupported response type!")
            
            check_main(main_to_all=main_to_all)


           # print(first_row)


        # for row in product_df.iter_rows():



        #     category = row[PRODUCT_FILE['columns']['query_string']['index']]
        #     market_ID = row[PRODUCT_FILE['columns']['market_ID']['index']]

        #     if len(requests) < limit and category not in updated:
        #         request = ScrapeRequest(ID=get_request_ID(), market_ID=market_ID, categories=[category])
        #         send_or_wait(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, request=request)
        #         requests.append(requests)
            
        #     while scraper_to_hub.empty():
        #         check_main(main_to_all=main_to_all)

        #     response = scraper_to_hub.get()

        #     if isinstance(response, list):
        #         print("Received scraped data. Processing...")

        #         for product, market_ID in response:
        #             market = hub.market(ID=market_ID)
        #             market.update_product(product=product)
            
        #     elif isinstance(response, int):
        #         print(f"Request {processed_request.ID} fulfilled!")




                







        # for market in markets:
        #     df = product_df.filter(product_df['market_ID'] == market.ID())

        #     for row in df.iter_rows():

        #         _datetime = datetime.strptime(row[PRODUCT_FILE['columns']['updated_at']['index']],
        #                                     "%Y-%m-%d %H:%M:%S")
                
        #         _timedelta = datetime.today() - _datetime

        #         if len(categories_to_update) < limit:
        #             categories_to_update.insert( (row[PRODUCT_FILE['columns']['query_string']['index']],
        #                                            _timedelta.total_seconds()) )
        #         else:


            
        #     categories_to_update.clear()
            
            




      #  result_df = product_df.map_rows(function=lambda row : analyze_product(row=row), return_dtype=None)



    




if __name__ == "__main__":

    print("Start this script as a subprocess by running start() function.")
    
 