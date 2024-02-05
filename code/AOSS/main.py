
import sys, os
import signal
import multiprocessing as mpr, multiprocessing.connection as mpr_conn


# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
sys.path.append(parent_directory)


from config_paths import *
from AOSS.components.processing import *

import AOSS.structure.marketing as mrk
import AOSS.components.scraping.scrape as scrp
import AOSS.gui.application as app


processes: List[mpr.Process] = []
main_to_all: mpr_conn.PipeConnection = mpr.Pipe()

def terminate():
    for process in processes:
        main_to_all.send("-end")

    for process in processes:
        process.join()

    processes.clear()    


def signal_handler(signum, frame):

    if signum == 2:

        print("Ctrl + C received. Terminating subprocesses.")
        terminate()
        exit(0)



def launch_subprocesses():
    
    

    main_to_all = mpr.Pipe()
    hub_to_scraper = mpr.Queue(maxsize=5)
    scraper_to_hub = mpr.Queue(maxsize=5)
    
    #hub_to_scraper, scraper_to_hub = mpr.Pipe()
    
    
    market_hub = mpr.Process(target=mrk.start, args=(main_to_all[0], hub_to_scraper, scraper_to_hub))
    
    market_hub.start()
    processes.append(market_hub)

    scraper = mpr.Process(target=scrp.start, args=(main_to_all[0], scraper_to_hub, hub_to_scraper))
    scraper.start()
    processes.append(scraper)

    gui = mpr.Process(target=app.start, args=(main_to_all[0],))
    gui.start()
    processes.append(gui)


    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Terminating processes...")

        # Send termination signal to each process
        for process in processes:
            main_to_all[0].send("-quit")

        # Wait for each process to terminate
        for process in processes:
            process.join()

        print("All processes terminated.")


    print("Main process terminated!")



if __name__ == '__main__':

    launch_subprocesses()    

    signal.signal(signal.SIGINT, signal_handler)