
import multiprocessing as mpr
import multiprocessing.connection as mpr_conn

import config_paths as cfg
from AOSS.structure.shopping import MarketHub
from AOSS.components.processing import ProductCategorizer

def start(main_to_categorizer: mpr.Queue):

    with MarketHub(src_file=cfg.MARKET_HUB_FILE) as hub:
        categorizer = ProductCategorizer(market_hub=hub)

    

        while True:

            if not main_to_categorizer.empty():
                request = main_to_categorizer.get(block=False)

                if isinstance(request, str):
                    categorizer.categorize(product=request)
                
                else:
                    print("Unknown request type for categorization!")
