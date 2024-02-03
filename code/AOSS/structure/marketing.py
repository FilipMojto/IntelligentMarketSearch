
import signal
import sys, os, time
import polars as pl
from typing import List
import multiprocessing as mpr, multiprocessing.connection as mpr_conn
from dataclasses import dataclass

#Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)

#print(__file__)# Move up two directories to reach the parent directory (AOSS)
#parent_directory = os.path.abspath(os.path.join(script_directory,))

#sys.path.append(parent_directory)
#os.chdir(parent_directory)


from config_paths import *
from AOSS.structure.shopping import MarketHub
from AOSS.components.scraping.base import ParallelProductScraper
from AOSS.other.utils import PathManager

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
        

        #requests.append(f"--scrape {training_market.ID()} " + " ".join(empty_categories) + str(get_request_ID()))

    # now the rest of the markets

def __scrape_training_set(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr_conn.PipeConnection, scraper_to_hub: mpr_conn.PipeConnection):
    assert(len(requests) > 0)

    hub_to_scraper.send(obj=requests[0])

    while(True):
        __check_main(main_to_all=main_to_all)

        if scraper_to_hub.poll(timeout=1.5):
            resp = scraper_to_hub.recv()

            if resp == 0:
                return 0
        
        time.sleep(1.5)

        
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
            
            requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), categories=empty_categories))

            #requests.append(f"--scrape {market.ID()} " + " ".join(empty_categories) + str(get_request_ID()))

def __scrape_product_sets(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr_conn.PipeConnection, scraper_to_hub: mpr_conn.PipeConnection):
    __check_main(main_to_all=main_to_all)

    for request in requests:
        hub_to_scraper.send(obj=request)
        __check_main(main_to_all=main_to_all)
        time.sleep(1)
    
    while len(requests) > 0:

        if scraper_to_hub.poll(timeout=1.5):
            resp_ID = scraper_to_hub.recv()

            for request in requests:
                if request.ID == resp_ID:
                    print(f"Request {request.ID} fulfilled!")
                    requests.remove(request)
                    break
        
        __check_main(main_to_all=main_to_all)
        time.sleep(1.5)


    
def __check_main(main_to_all: mpr_conn.PipeConnection):

    try:
        if main_to_all.poll(timeout=1) and main_to_all.recv() == "-quit":
            terminate()
    except KeyboardInterrupt:
        terminate()

        

def start_market_hub(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr_conn.PipeConnection,
                     scraper_to_hub: mpr_conn.PipeConnection):

    with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:
        global product_df
        product_df = pl.read_csv(hub.product_file())
        print(product_df.describe())

        __check_main(main_to_all=main_to_all)
        __check_training_set(hub=hub)


        if len(requests) > 0:
            __scrape_training_set(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, scraper_to_hub=scraper_to_hub)
            requests.pop(0)

        assert(len(requests) == 0)

        
        __check_main(main_to_all)
        __check_product_sets(hub=hub)
        
        if len(requests) > 0:
            __scrape_product_sets(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, scraper_to_hub=scraper_to_hub)

        # for request in request:
        #     data = hub_to_scraper.send(obj=request)

        #     __check_main()
        #     time.sleep(0.5)

        # while True:
        #     __check_main()

        #     if scraper_to_hub.poll(timeout=1.5):
        #         response = scraper_to_hub.recv()

        #         if response is not None:
        #             response_ID = int(response)

        #             for request in requests:
        #                 if requests

        #     time.sleep(1.5)
  
        

def start(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr_conn.PipeConnection, 
          scraper_to_hub: mpr_conn.PipeConnection):
    os.chdir(parent_directory)
    # print(f"Par: {parent_directory}")
    # print(f"Cur: {os.getcwd()}")
    start_market_hub(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, scraper_to_hub=scraper_to_hub)




if __name__ == "__main__":
    start()

    signal.signal(signal.SIGINT, signal_handler)