
import sys, os
import signal
import threading
import multiprocessing as mpr, multiprocessing.connection as mpr_conn
from typing import List
import queue
from dataclasses import dataclass

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)


# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..'))
sys.path.append(parent_directory)

MAIN_TERMINATION_SIGNAL = "-end"
# GUI_TERMINATION_SIGNAL = 1





from config_paths import *

from AOSS.processes.IPC import GUI_TERMINATION_SIGNAL
from AOSS.processes.DPMP import start as dpmp_start
from AOSS.processes.DSPP import start as dspp_start
from AOSS.processes.GUIP import start as gui_start

main_to_all = mpr.Queue(maxsize=5)
gui_to_main = mpr.Queue(maxsize=5)
hub_to_scraper = mpr.Queue(maxsize=5)
scraper_to_hub = mpr.Queue(maxsize=5)
hub_to_qui = mpr.Queue(maxsize=5)
gui_to_hub = mpr.Queue(maxsize=5)
product_file_lock = mpr.Lock()


processes: List[mpr.Process] = []

def terminate(signal):
    signal.value = 1
    #main_to_all.put(MAIN_TERMINATION_SIGNAL)
    #main_to_all.send("-quit")

    for process in processes:
        process.join()

    processes.clear()
    exit(0)

#def send_termination_signals():
    
    
    # for process in processes:
    #     process.join()

    # processes.clear()
    # print("All processes terminated.")


def signal_handler(signum, frame):


    if signum == 2:
        print("Ctrl + C received. Terminating subprocesses.")
        terminate()





def check_gui(signal, timeout: float = 1.5):

    try:
        if gui_to_main.get(block=False, timeout=timeout) == GUI_TERMINATION_SIGNAL:
        
            terminate(signal=signal)
        
    except queue.Empty:
        pass

def launch_subprocesses():

    manager = mpr.Manager()
    shared_termination_signal = manager.Value('i', 0)
    
        
    

    # main_to_all = mpr.Pipe()
    # hub_to_scraper = mpr.Queue(maxsize=5)
    # scraper_to_hub = mpr.Queue(maxsize=5)
    
    #hub_to_scraper, scraper_to_hub = mpr.Pipe()
    
    
    market_hub = mpr.Process(target=dpmp_start, args=(shared_termination_signal, hub_to_scraper, scraper_to_hub, hub_to_qui,
                                                     gui_to_hub, product_file_lock))
    
    market_hub.start()
    processes.append(market_hub)

    scraper = mpr.Process(target=dspp_start, args=(shared_termination_signal, scraper_to_hub, hub_to_scraper))
    scraper.start()
    processes.append(scraper)
    

    gui = mpr.Process(target=gui_start, args=(shared_termination_signal, gui_to_main, hub_to_qui, gui_to_hub, product_file_lock))
    gui.start()
    processes.append(gui)

    while True:
        check_gui(signal=shared_termination_signal)


    # try:
    #     for process in processes:
    #         process.join()
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt received. Terminating processes...")
        #terminate()
        # # Send termination signal to each process
        # for process in processes:
        #     main_to_all[0].send("-quit")

        # # Wait for each process to terminate
        # for process in processes:
        #     process.join()

        # print("All processes terminated.")

    #terminate()
    #print("Main process terminated!")



if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    launch_subprocesses()

    