import multiprocessing as mp
import time
from typing import List, Dict


import config_paths as cfg
import AOSS.components.script as scrip
from AOSS.structure.shopping import MarketHub, ProductCategory
from AOSS.components.processing import ProductCategorizer

#output_file = "./test.csv"

def main():
    with MarketHub(src_file=cfg.MARKET_HUB_FILE['path']) as hub:

        categorizer = ProductCategorizer(market_hub=hub)
        categorizer.recategorize()

    # Create a multiprocessing Queue for communication
#     main_to_subprocess = mp.Queue()

#     count = 4

#     all_to_main = mp.Queue(maxsize=5)
#     processes: List[tuple[mp.Process, str]] = []

#     hub = MarketHub(src_file=cfg.MARKET_HUB_FILE['path'])
#     hub.load_markets()
#     hub.load_products()


#     product_df = hub.product_df()


#     for row in product_df.iter_rows(named=True):
   
#         if len(processes) < count:
#             categorizer = mp.Process(target=scrip.launch_subprocess, args=(all_to_main, row['normalized_name']))

#             categorizer.start()
#             processes.append((categorizer, row['normalized_name']))
             
#             if len(processes) != count:
#                 time.sleep(2)
#             continue

#         while True:
#             if not all_to_main.empty():
#                 response: tuple[int, ProductCategory] = all_to_main.get(block=False)

#                 if isinstance(response, tuple):
#                     pid, category = response
#                     found = False
#                     # let's find a subprocess which finished
#                     for process, product in processes:
#                         if process.pid == pid:
#                             with open(file=output_file, mode='a', encoding='utf-8', newline='') as output_f:
#                                 output_f.write(product + ': ' + category.name + '\n')

#                             process.join()
#                             processes.remove((process, product))
#                             found = True
#                             break
#                     else:
#                         print("Provided process ID not found!")
                    
#                     if found: break

#                 else:
#                     print("Unknown response type!")
            
#             # else:
#             #     time.sleep(1.5)
                


        





#     # Launch the subprocess
#     #subprocess_process = mp.Process(target=scrip.launch_subprocess, args=(main_to_subprocess,))
    
    
#     #subprocess_process.start()
#     #print(f"subprocess: {subprocess_process.pid}")

#     # Send data to the subprocess through the Queue
#     #main_to_subprocess.put("Hello from the main process!")

    



#     # Wait for the subprocess to finish
#  #   subprocess_process.join()

#     print("Main process finished.")


if __name__ == "__main__":
    main()