import time

from AOSS.structure.shopping import MarketHub
from AOSS.components.scraping.base import ParallelProductScraper

from config_paths import *

with MarketHub(src_file=MARKET_HUB_FILE['path'], header=MARKET_HUB_FILE['header']) as hub:

    market = hub.market(ID=1)

    scraper = ParallelProductScraper(market=market, session_limit=5)

    scraper.scrape_all(console_log=True, categories=('ovocie-zelenina-103',
                                                     'pecivo-111',
                                                     'maso-ryby-117',
                                                     'udeniny-lahodky-128'))

    while scraper.is_scraping():

        time.sleep(2)

    print("exiting the main thread...")

    
