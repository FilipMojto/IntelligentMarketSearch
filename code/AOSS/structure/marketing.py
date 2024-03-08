import sys, os, time
from typing import List
import multiprocessing as mpr, multiprocessing.connection as mpr_conn
from dataclasses import dataclass
import signal
import math
from queue import Empty
import threading
from datetime import datetime

#Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)


from config_paths import *
from AOSS.structure.shopping import MarketHub, Market, ProductCategory
from AOSS.components.processing import ProductCategorizer
from AOSS.components.processing import process_product
from AOSS.other.exceptions import IllegalProductState

from AOSS.components.IPC.IPC import ProgressReportPoints as PRP
from AOSS.components.IPC.IPC import PROGRESS_REPORTS as PR

@dataclass
class ScrapeRequest:
    ID: int
    market_ID: int
    categories: List[int]


requests: List[ScrapeRequest] = []
request_ID = 1
product_df = None


UPDATE_PRODUCTS_SIGNAL = 1
PROGRESS_BAR_SIGNAL = 2
UPDATE_INTERVAL_SIGNAL = 3
UPDATE_STOP_SIGNAL = -1

UPDATE_LIMIT = 0.75
MAX_UPDATE_DELAY = 30




def get_request_ID():
    global request_ID
    old_ID = request_ID
    request_ID += 1
    return old_ID



market_hub_lock = threading.Lock()


                                
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

    for ID, name in categories.items():
        if len( product_df.filter( (product_df['market_ID'] == market.ID() ) &
                                (product_df['query_string_ID'] == ID) )) == 0:
            
            print(f"Detected no products for market {market.name()}. Category: {name}")
            empty_categories.append(ID)
        
    # now we create a request if needed
    if empty_categories:
        requests.append(ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), categories=empty_categories))





def start(main_to_all: mpr.Queue, hub_to_scraper: mpr.Queue, scraper_to_hub: mpr.Queue, hub_to_gui: mpr.Queue,
          gui_to_hub: mpr.Queue, product_file_lock: mpr.Lock):
    
    update_interval = 0

    def terminate():
        nonlocal hub
        hub.save_markets()
        hub.update()
        exit(0)
        

    def signal_handler(signum, frame):

        if signum == 2:
            # Since proess might be in the middle of update or something like that, 
            # some exceptions might be uncaught
            try:
                print("Terminating marketing process...")
                terminate()
            except Exception:
                pass
            #sys.exit(0)
    

    def check_main(main_to_all, timeout: int = 1):
        """
            Checks for some predefined signals which might be sent by the main process, like termination signal.

            If termination signal was received, process terminates by executing termination function.
        """

        
        if main_to_all.value:
            terminate()
        
        time.sleep(timeout)
   


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


    def process_request_data(request: ScrapeRequest):
        nonlocal scraper_to_hub, gui_to_hub, main_to_all, update_interval

        while True:
            # here we wait until we receive and answer
            while scraper_to_hub.empty():
                check_main(main_to_all=main_to_all)

            response = scraper_to_hub.get(block=False)

            # case in which we should receive updated product data
            if isinstance(response, list):
                print("Received scraped data! Processing...")
                
                for product, market_ID in response:
                    check_main(main_to_all=main_to_all, timeout=0.1)
                    update_interval = check_update_interval_signals(gui_to_hub=gui_to_hub,
                                                                    interval=update_interval)
                    
                    while update_interval == -1:
        
                        check_main(main_to_all=main_to_all)
                        update_interval = check_update_interval_signals(gui_to_hub=gui_to_hub, interval=update_interval)

                    process_product(product=product)

                    if market_ID == request.market_ID:
                        market = hub.market(identifier=market_ID)
                        try:
                            market.update_product(product=product)

                            print(f"Updated successfully: {product.name}")
                            try:
                                # we remove this product as it has been updated and is still at disposal
                                category_products.remove(product.name)
                            except ValueError:
                                pass


                        # we received a new data which are not yet registered
                        except IllegalProductState:
                            
                            if market.ID() == training_market.ID():
                                category = categorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'])
                            else:
                                category = categorizer.categorize(product=product)

                            process_product(product=product)
                            try:
                                
                                market.register_product(product=product, norm_category=category)
                                print(f"Registered successfully: {{{product.name}}}")
                            except IllegalProductState:
                                print(f"Product {{{product.name}}} already registered!")

                    else:
                        print("Received response contains invalid market ID!")
            
            
            # case in which we should receive the ScrapeProcessTerminationSignal
            elif isinstance(response, int):
                
                # here all updated data have to be saved to the product file and market hub
                # has to be refreshed
                if request.ID == response:
                    market = hub.market(identifier=request.market_ID)
                    #if market.

                    if category_products:
                        market.remove_products(identifiers=category_products)
                    

                    print(f"Request {request.ID} fulfilled!")

                    while hub_to_gui.full():
                        print("GUI's queue is full! Retrying...")
                        check_main(main_to_all=main_to_all)
                    
                    hub_to_gui.put(obj=(UPDATE_PRODUCTS_SIGNAL,), block=False)

                    while gui_to_hub.empty() or gui_to_hub.get(block=False)[0] != UPDATE_PRODUCTS_SIGNAL:
                        time.sleep(1)


                    with product_file_lock:
                        market.save_products()
                        hub.update()
                        hub.load_products()

                    break
                else:
                    print("Received invalid Scrape Process Termination Signal!")
            else:
                print("Unsupported response type!")
            
            check_main(main_to_all=main_to_all)

        
        time.sleep(update_interval)


    def send_progress_signal(hub_to_gui: mpr.Queue, main_to_all: mpr.Queue, progress: int):
        assert(0<=progress<=100)

        while hub_to_gui.full():
            print("Gui process queue full! Retrying...")
            check_main(main_to_all=main_to_all)
        
        hub_to_gui.put(obj=(PROGRESS_BAR_SIGNAL, progress), block=False)
    



    def check_update_interval_signals(gui_to_hub: mpr.Queue, interval: int, timeout: int = 1):

        try:
            signal = gui_to_hub.get(timeout=timeout)

            if signal[0] == UPDATE_INTERVAL_SIGNAL:
                return int(signal[1])
            
        except Empty:
            pass

        return interval


    
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

    # analyzing training market
    send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=PRP.TRAINING_MARKET_ANALYSIS)

    training_market = hub.training_market()
    analyze_market(market=training_market)
    
    send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=PRP.MARKETS_ANALYSIS)


    for market in markets:
        if market.ID() == training_market.ID(): continue
        analyze_market(market=market)

    send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=PRP.SCRAPING_MISSING_DATA)

    
    if requests:
        progress = PRP.SCRAPING_MISSING_DATA
        progress_rate = math.floor((PRP.UPDATING_DATA - PRP.SCRAPING_MISSING_DATA)
                                   /len(requests))

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
                    
          
                    for product_data in scraped_data:
                        check_main(main_to_all=main_to_all, timeout=0.001)

                        product, market_ID = product_data
                        market = hub.market(identifier=market_ID)

                        process_product(product=product)
                        category = ProductCategory.NEURČENÁ
                        if market_ID == training_market.ID():
                            category = ProductCategorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'])
                        
                        try:
                            market.register_product(product=product, norm_category=category)
                            print(f"Registered successfully: {{{product.name}}}")
                        except IllegalProductState:
                            print(f"Product {{{product.name}}} already registered!")
                            
              

                elif isinstance(scraped_data, int):

                    if processed_request.ID == scraped_data:
                        print(f"Request {processed_request.ID} fulfilled!")

                        with product_file_lock:
                            hub.market(identifier=processed_request.market_ID).save_products()
                        
                        hub.update()

                        with product_file_lock:
                            hub.load_products()
                        send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=progress + progress_rate)
                        progress += progress_rate
                        break
                else:
                    print("Unsupported response type!")
            
            time.sleep(1.5)


    send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=PRP.UPDATING_DATA)

    sorted_df = product_df.sort('updated_at')

    # firsly we check whether certain fraction of products are out-of-date
    update_limit_row = sorted_df.row(int((len(product_df)/100) * UPDATE_LIMIT))
    
    # we convert the string into a timestamp    
    timestamp = datetime.strptime(update_limit_row[PRODUCT_FILE['columns']['updated_at']['index']], "%Y-%m-%d %H:%M:%S")
    current_date = datetime.now()

    # now we get the update delay
    update_delay = current_date - timestamp

    if (update_delay.total_seconds())/60 > MAX_UPDATE_DELAY:
        print("Detected a lot of out-of-date data! Updating...")
        hub.remove_local_products()
        return start(main_to_all, hub_to_scraper, scraper_to_hub, hub_to_gui,
          gui_to_hub, product_file_lock)

        # for market in markets:
        #     request = ScrapeRequest(ID=get_request_ID(), market_ID=market.ID(), 
        #                             categories=None)
            
        #     send_or_wait(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, request=request)
        #     process_request_data(request=request)

    send_progress_signal(hub_to_gui=hub_to_gui, main_to_all=main_to_all, progress=PRP.FINISHING_POINT)

    # now gui can start, since all necessary data are present   
    # while hub_to_gui.full():
    #     print("Unable to send scraping request!. Retrying...")
    #     check_main(main_to_all=main_to_all)

    #hub_to_gui.put(obj=GUI_START_SIGNAL, block=False)
    

    hub.update()

    print("Starting update process...")
    processed_categories: List[str] = []
    
    categorizer = ProductCategorizer(market_hub=hub)

    while True:
        # we update product_df to get latest version of dataframe
        product_df = hub.product_df()

        # sorting the product dataframe by the updated_at attribute
        # we find the earliest updated record in dataframe
    

        print(f"The difference between {current_date} and {timestamp} is: {update_delay.total_seconds()/60}")


        earliest_updated = sorted_df.filter(sorted_df['query_string_ID'].is_in(processed_categories).not_()).head(1)
        
        #print(earliest_updated)
        



        market = earliest_updated['market_ID']
        processed_categories.append(earliest_updated['query_string_ID'][0])
        
        # here we store products belonging to the same category as the earliest updated product
        # products which will remain here after update process is finished are removed from the
        # market
        category_products = product_df.filter(product_df['query_string_ID'] == earliest_updated['query_string_ID'])['name'].to_list()
        

        print(f"Updating category {earliest_updated['query_string_ID'][0]} of market {earliest_updated['market_ID'][0]}.")
    

        # now we create a ScrapeRequest isntance and send it to the scraper process
        processed_request = ScrapeRequest(ID=get_request_ID(), market_ID=earliest_updated['market_ID'][0], categories=[earliest_updated['query_string_ID'][0]])
        
        with product_file_lock:
            hub.market(identifier=processed_request.market_ID).load_products()
        
        send_or_wait(main_to_all=main_to_all, hub_to_scraper=hub_to_scraper, request=processed_request)

        #update_interval = 0

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
                    check_main(main_to_all=main_to_all, timeout=0.1)
                    update_interval = check_update_interval_signals(gui_to_hub=gui_to_hub,
                                                                    interval=update_interval)
                    
                    while update_interval == -1:
        
                        check_main(main_to_all=main_to_all)
                        update_interval = check_update_interval_signals(gui_to_hub=gui_to_hub, interval=update_interval)

                    process_product(product=product)

                    if market_ID == processed_request.market_ID:
                        market = hub.market(identifier=market_ID)
                        try:
                            market.update_product(product=product)

                            print(f"Updated successfully: {product.name}")
                            try:
                                # we remove this product as it has been updated and is still at disposal
                                category_products.remove(product.name)
                            except ValueError:
                                pass


                        # we received a new data which are not yet registered
                        except IllegalProductState:
                            
                            if market.ID() == training_market.ID():
                                category = categorizer.categorize_by_mapping(product=product, mappings_file=CATEGORY_MAP_FILE['path'])
                            else:
                                category = categorizer.categorize(product=product)

                            process_product(product=product)
                            try:
                                
                                market.register_product(product=product, norm_category=category)
                                print(f"Registered successfully: {{{product.name}}}")
                            except IllegalProductState:
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
                        market.remove_products(identifiers=category_products)
                    

                    print(f"Request {processed_request.ID} fulfilled!")
                    #market.save_products()

                    while hub_to_gui.full():
                        print("GUI's queue is full! Retrying...")
                        check_main(main_to_all=main_to_all)
                    
                    hub_to_gui.put(obj=(UPDATE_PRODUCTS_SIGNAL,), block=False)

                    while gui_to_hub.empty() or gui_to_hub.get(block=False)[0] != UPDATE_PRODUCTS_SIGNAL:
                        time.sleep(1)


                    with product_file_lock:
                        market.save_products()
                        hub.update()
                        hub.load_products()
                    break
                else:
                    print("Received invalid Scrape Process Termination Signal!")
            else:
                print("Unsupported response type!")
            
            check_main(main_to_all=main_to_all)


           # print(first_row)


        time.sleep(update_interval)


if __name__ == "__main__":

    print("Start this script as a subprocess by running start() function.")
    
 