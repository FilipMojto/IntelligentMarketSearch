import multiprocessing as mp



def launch_subprocess(all_to_main: mp.Queue, product: str):
    try:
        
        # Import necessary modules and functions in the subprocess
        import time, os

        import config_paths as cfg
        from AOSS.structure.marketing import MarketHub
        from AOSS.components.processing import ProductCategorizer


        hub = MarketHub(src_file=cfg.MARKET_HUB_FILE['path'])
        hub.load_markets()
        hub.load_products()

        categorizer = ProductCategorizer(market_hub=hub)
        category = categorizer.categorize(product=product)

        while all_to_main.full():
            print("Failed to send a reponse! Queue is full.")
            time.sleep(1.5)


        all_to_main.put(obj=(os.getpid(), category), block=False)
          

        


        print("END!")

        # # Implement the subprocess logic
        # while True:
        #     message = main_to_subprocess.get()
        #     print(f"Subprocess received: {message}")
        #     time.sleep(2)

    except Exception as e:
        print(f"Exception in subprocess: {e}")
