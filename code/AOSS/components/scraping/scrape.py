import time
from typing import List
import os, sys
import multiprocessing.connection as mpr_conn, signal

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


requests = []
scrapers: List[ParallelProductScraper] = []


def terminate():
    print("Terminating scraping process...")
    exit(0)

def signal_handler(signum, frame):
    
    if signum == 2:
        terminate()

def start(main_to_all: mpr_conn.PipeConnection, hub_to_scraper: mpr_conn.PipeConnection,
          scraper_to_hub: mpr_conn.PipeConnection):

    os.chdir(parent_directory)
    scrapers.clear()

    with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

        for market in hub.markets():
            scrapers.append(ParallelProductScraper(market=market, session_limit=5))

    data : str = ""

    while True:
        all_finished = True
        
        for scraper in scrapers:
            if scraper.is_scraping():
                all_finished = False
                break
        
        if all_finished and len(requests) > 0:

            for _ in range(len(requests)):
                request = requests.pop(0)
                # args = request.split(' ')
                
                # if len(args) < 2:
                #     print("Invalid request format!")
                #     continue
                
                market = hub.market(ID=int(request.market_ID))
                success = False

                # if args[0] == '--scrape':
                #     print(f"Im supposed to scrape from market: {market.name()}.")

                for scraper in scrapers:
                    if scraper.market().ID() == market.ID():
                        scraper.scrape_all(categories=request.categories)
                        success = False
                        break
                
                if success: break

        for scraper in scrapers:
            if not scraper.is_scraping() and scraper.buffer_size() > 200:
                data = scraper.consume_buffer()

                with open(file="../resources/temp.csv", mode='a', encoding='utf-8') as file:

                    for product in data:
                        file.write(data[0] + ',' + data[1] + ',' + data[2])
         
        


        try:
            if main_to_all.poll(timeout=0.01):
                data = main_to_all.recv()
        except KeyboardInterrupt:
            terminate()

        if data is not None:

            if data == "-quit":
                print("Qutting scraping proces...")
                sys.exit(0)
        
        hub_request: str = None

        if hub_to_scraper.poll(timeout=0.1):
            hub_request = hub_to_scraper.recv()

        if hub_request is not None:
            requests.append(hub_request)
        
        time.sleep(1.5)

                


if __name__ == "__main__":
    print("Start this script as a subprocess and provide some connections.")

    signal.signal(signal.SIGINT, signal_handler)