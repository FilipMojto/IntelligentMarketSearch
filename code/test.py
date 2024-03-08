from AOSS.structure.shopping import MarketHub
from AOSS.components.scraping.base import ProductScraper
from AOSS.components.processing import process_scraped_products

import config_paths as cfg

def main():
    # with MarketHub(src_file=cfg.MARKET_HUB_FILE['path']) as hub:
    #     hub.remove_local_products()


    #     # scraper = ProductScraper(hub.market(identifier=1))
    #     # products = scraper.scrape_all(console_log=True)

    #     # products[]


    #     pass
        #products = process_scraped_products(products=products)







if __name__ == "__main__":
    main()