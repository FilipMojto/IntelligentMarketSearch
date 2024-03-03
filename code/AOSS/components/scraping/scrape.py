import time
from typing import List
import os, sys
import multiprocessing as mpr, multiprocessing.connection as mpr_conn, signal
import msvcrt

import threading
from queue import Empty

#Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..', '..'))
sys.path.append(parent_directory)

#print(__file__)# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..', '..'))

sys.path.append(parent_directory)
os.chdir(parent_directory)


from config_paths import *
from AOSS.structure.marketing import ScrapeRequest
from AOSS.structure.shopping import MarketHub, Product
from AOSS.components.scraping.base import ProductScraper



scrapers: List[ProductScraper] = []
scraper_lock = threading.Lock()
active_scraper: ProductScraper = None
is_scraping = threading.Event()

requests: List[ScrapeRequest] = []
products: List[tuple[Product, int]] = []
product_lock = threading.Lock()
processed_request: ScrapeRequest = None

def terminate():
    print("Terminating scraping process...")

    # for scraper in scrapers:
    #     scraper.quit()

    exit(0)

def signal_handler(signum, frame):
    
    if signum == 2:
        terminate()

def check_main(main_to_all, timeout: float = 1.5):
    """
        This function checks for any incoming request from the main process.
    """

    if main_to_all.value:
         terminate()
        
    time.sleep(timeout)
    
    # try:
    #     if main_to_all.get(timeout=timeout) == "-end":
    #         terminate()
    # except Empty:
    #     pass
    #if not main_to_all.empty() and main_to_all.get(block=False) == "-end":
     #   terminate()


    #if main_to_all.poll(timeout=timeout) and main_to_all.recv() == "-end":
     #   terminate()



def __check_market_hub(hub_to_scraper: mpr.Queue):
    """
        This function checks for any incoming request from the market hub process.

        If a passed object's type is ScrapeRequest we process save the request to the
        request buffer.
    """

    if not hub_to_scraper.empty():
        msg = hub_to_scraper.get(block=False)

        if isinstance(msg, ScrapeRequest):
            global requests
            requests.append(msg)
        else:
            print("Unexpected object type from hub-to-scraper connection!")


def __scrape_products(scraper: ProductScraper, request: ScrapeRequest):

    """
        Used solely by script, more specifically by a scraping thread. It scrapes all data from a specific scraper.
        Before it starts execution it must get lock of active_scraper global variable.
    """
    is_scraping.set()

    products_ = scraper.scrape_categories(identifiers=request.categories, mode='ID')

    with product_lock:
        global products
        products.extend(products_)
    
    is_scraping.clear()
    
    # with scraper_lock:
    #     active_scraper = None





def process_requests(main_to_all: mpr.Queue, scraper_to_hub: mpr.Queue):

    global active_scraper, processed_request, products

    if not is_scraping.is_set():

        while len(requests) > 0:
            request = requests.pop(0)
            scraper_found = False

            # we search scrapers to find the one which suits the request
            for scraper in scrapers:

                if scraper.market().ID() == request.market_ID:
                

                    scrape_thread = threading.Thread(target=__scrape_products, args=(scraper, request))
                    scrape_thread.start()
                    processed_request = request

                    break
            
            # case in which an invalid request was received, program simply dumps such requests
            else:
                print("Received a request with unknown market ID! Dumping...")

            check_main(main_to_all=main_to_all)

            # while there are still requests available and scraper was not found program
            # continues the loop
            if scraper_found:
                break
                
        check_main(main_to_all=main_to_all)
   
    with product_lock:
       # can_send = (products)

        finished = False

        while products:
            finished = True
            
            #length = len(products)

            #while i <  length:

            while True:
                if not scraper_to_hub.full():
                    scraper_to_hub.put(obj=products[:5000], block=False)
                    break
                else:
                    print("Pipe not ready for writing. Retrying...")
                    check_main(main_to_all=main_to_all, timeout=0.05)
                
            products = products[5000:]

            #products = products[5000:]
        
        if finished:
            while True:
                if not scraper_to_hub.full():
                    scraper_to_hub.put(processed_request.ID, block=False)
                    break
                else:
                    print("Pipe not ready for writing. Retrying...")
                    check_main(main_to_all=main_to_all, timeout=0.05)






#     if is_scraping.is_set() and not requests:
        
#         while True:
#             if not scraper_to_hub.full():
#                 scraper_to_hub.put(processed_request.ID, block=False)
#                 __check_main(main_to_all=main_to_all)
#                 break
#             else:
#                 print("Pipe not ready for writing. Retrying...")
#                 time.sleep(1.5)

#         active_scraper = None
#         processed_request = None

# __check_main(main_to_all=main_to_all)


# def __check_products(scraper_to_hub: mpr.Queue):
#     global products

#     with product_lock:
#         if products:
#             if not scraper_to_hub.full():
#                 for product in products:
#                     scraper_to_hub.put(obj=product, block=False)
                
#                 products.clear()
#             else:
#                 print("Pipe not ready for writing. Retrying...")
#                 time.sleep(1.5)




def start(main_to_all: mpr.Queue, scraper_to_hub: mpr.Queue,
          hub_to_scraper: mpr.Queue):
    
    signal.signal(signal.SIGINT, signal_handler)
    os.chdir(parent_directory)
    scrapers.clear()
    


    check_main(main_to_all=main_to_all)

    # here we initialize a scraper for each market availale in the market hub
    with MarketHub(src_file=MARKET_HUB_FILE['path']) as hub:

        for market in hub.markets():
            scrapers.append(ProductScraper(market=market))

        # now we can check for incoming requests and process them afterwards
        # the process also checks for incoming signal from the main process
        # the process listens for incoming requests from the market hub process until
        # end request from main process is received
        is_scraping.clear()

        while True:

            __check_market_hub(hub_to_scraper=hub_to_scraper)
            process_requests(main_to_all=main_to_all, scraper_to_hub=scraper_to_hub)
            check_main(main_to_all=main_to_all)

            time.sleep(1)
    
    



if __name__ == "__main__":
    print("Start this script as a subprocess and provide some connections.")

    #signal.signal(signal.SIGINT, signal_handler)