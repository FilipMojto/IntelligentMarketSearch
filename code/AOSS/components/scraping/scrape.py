import time
from typing import List
import os, sys
import multiprocessing as mpr, multiprocessing.connection as mpr_conn, signal
import msvcrt
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
from AOSS.structure.shopping import MarketHub
from AOSS.components.scraping.base import ParallelProductScraper
from AOSS.structure.marketing import ScrapeRequest


scrapers: List[ParallelProductScraper] = []
active_scraper: ParallelProductScraper = None

requests: List[ScrapeRequest] = []
processed_request: ScrapeRequest = None

def terminate():
    print("Terminating scraping process...")
    exit(0)

def signal_handler(signum, frame):
    
    if signum == 2:
        terminate()

def __check_main(main_to_all: mpr_conn.PipeConnection):
    """
        This function checks for any incoming request from the main process.
    """

    if main_to_all.poll(timeout=1.5) and main_to_all.recv() == "-end":
        terminate()



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

    
    #    pass

    # if hub_to_scraper.poll(timeout=1.5):
    #     msg = hub_to_scraper.recv()

    #     if isinstance(msg, ScrapeRequest):
    #         global requests
    #         requests.append(msg)
    #     else:
    #         print("Unexpected object type from hub-to-scraper connection!")

def process_requests(main_to_all: mpr_conn.PipeConnection, scraper_to_hub: mpr.Queue):

    global active_scraper, processed_request

    # first case in which no scraping process in currently in progress
    if active_scraper is None and processed_request is None:

    
        while len(requests) > 0:
            request = requests.pop(0)
            scraper_found = False

            # we search scrapers to find the one which suits the request
            for scraper in scrapers:

                if scraper.market().ID() == request.market_ID:
                    scraper.scrape_all(categories=request.categories, console_log=True)
                    active_scraper = scraper
                    processed_request = request
                    scraper_found = True
                    break
            
            # case in which an invalid request was received, program simply dumps such requests
            else:
                print("Received a request with unknown market ID! Dumping...")

            __check_main(main_to_all=main_to_all)

            # while there are still requests available and scraper was not found program
            # continues the loop
            if scraper_found:
                break
                
        __check_main(main_to_all=main_to_all)

    # the other possible case where there is or was an active scraper recently
    elif active_scraper is not None and processed_request is not None:

        # if scrape buffer has reached its limit or scraper stopped scraping
        if active_scraper.buffer_size() > 100 or not active_scraper.is_scraping():
            data = active_scraper.consume_buffer()
       
            # this way scraper process repeats its attempt to send data until they are
            # received successfully
            while True:
                if not scraper_to_hub.full():
                    scraper_to_hub.put(obj=data, block=False)
                    #scraper_to_hub.send(data)
                    __check_main(main_to_all=main_to_all)
                    break
                else:
                    print("Unable to send scraped data! Retrying...")
                    time.sleep(1.5)

            # if scraper has scraped all data process attempts to send the processed request's
            # ID as a signal that all data requested were scraped successfully
            if not active_scraper.is_scraping():
                
                while True:
                    if not scraper_to_hub.full():
                        scraper_to_hub.put(processed_request.ID, block=False)
                        __check_main(main_to_all=main_to_all)
                        break
                    else:
                        print("Pipe not ready for writing. Retrying...")
                        time.sleep(1.5)

                active_scraper = None
                processed_request = None

        __check_main(main_to_all=main_to_all)



def start(main_to_all: mpr_conn.PipeConnection, scraper_to_hub: mpr.Queue,
          hub_to_scraper: mpr.Queue):
    
    signal.signal(signal.SIGINT, signal_handler)
    os.chdir(parent_directory)
    scrapers.clear()
    
    __check_main(main_to_all=main_to_all)

    # here we initialize a scraper for each market availale in the market hub
    with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

        for market in hub.markets():
            scrapers.append(ParallelProductScraper(market=market, session_limit=5))

    # now we can check for incoming requests and process them afterwards
    # the process also checks for incoming signal from the main process
    # the process listens for incoming requests from the market hub process until
    # end request from main process is received
        
    while True:

        __check_market_hub(hub_to_scraper=hub_to_scraper)
        process_requests(main_to_all=main_to_all, scraper_to_hub=scraper_to_hub)
        __check_main(main_to_all=main_to_all)

        time.sleep(1)
                


if __name__ == "__main__":
    print("Start this script as a subprocess and provide some connections.")

    #signal.signal(signal.SIGINT, signal_handler)