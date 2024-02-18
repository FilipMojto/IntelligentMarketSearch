__ALL__ = ['Application']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"


import tkinter
from tkinter import TclError
import os, sys
import signal, multiprocessing as mpr, multiprocessing.connection as mpr_conn
import threading as thrd
import time


# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)

from config_paths import *
from AOSS.gui.main_shopping_view import MainShoppingView
from AOSS.gui.loading_screen import LoadingScreen
from AOSS.structure.marketing import GUI_START_SIGNAL

def terminate():
    print("Terminating GUI process...")
    os._exit(0)

def signal_handler(signum, frame):

    if signum == signal.SIGINT:
        terminate()

class Application(tkinter.Tk):

    def __init__(self, *args, lock: mpr.Lock = None, **kw) -> None:
        super(Application, self).__init__(*args, **kw)
        #self.__app = tkinter.Tk()

        self.title("AOSS Application 1.2.0")
        self.geometry("1000x580")
        self.minsize(700, 500)
        
        self.__main_shoppping_view = MainShoppingView(self, _product_file_lock=lock,  bg='black')
        self.__main_shoppping_view.grid(row=0, column=0, sticky="NSEW", padx=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        

        #self.mainloop()








def start(main_to_all: mpr.Queue = None, hub_to_gui: mpr.Queue = None, product_file_lock: mpr.Lock = None):
    """
        This function starts a GUI process for AOSS app.

        Parameters:

            a) main_to_all - a Queue instance which is used by the main process to broadcast its signals
                            to all subprocesses

            b) hub_to_gui - a Queue instance which is used by the Marketing Process to communicate with
                            Gui Process
    """




    app: Application = None

    def __start_app(lock: mpr.Lock = None):
        nonlocal app
        app = Application(lock)
        app.mainloop()

    if main_to_all is None:
        __start_app()
        terminate()
    


    def check_main(window: tkinter.Tk, repeat_after: int = -1):

        nonlocal main_to_all

        if not main_to_all.empty() and main_to_all.get(block=False) == "-end":
            terminate()

        if repeat_after >= 0:
            window.after(repeat_after, check_main, window)

    loading_screen_after_ids = []

    def check_progress_reports(main_to_all: mpr_conn.PipeConnection, hub_to_gui: mpr.Queue):
        
        nonlocal loading_screen
        nonlocal loading_screen_after_ids
        check_main(window=loading_screen, repeat_after=-1)

        try:
            if not hub_to_gui.empty():
                progress = hub_to_gui.get(block=False)
                assert(0<=progress<=100)

                loading_screen.progress_bar['value'] = progress
                loading_screen.update_idletasks()

                if progress == 100:                    
                    loading_screen.quit()
                    return
    
            # Schedule the next after() call and save the after ID
            loading_screen_after_ids.append(loading_screen.after(1500, check_progress_reports, main_to_all, hub_to_gui))

        # loading_screen_after_ids = [id for id in loading_screen_after_ids if loading_screen.after(id, None) is not None]
            #time.sleep(1.5)
        except KeyboardInterrupt:
            terminate()
   
    
    # starting the loadscreen
    loading_screen = LoadingScreen()
    loading_screen.after(1500, check_progress_reports, main_to_all, hub_to_gui)
    loading_screen.mainloop()

    # here we remove any scheduled functions
    for id in loading_screen_after_ids:
        loading_screen.after_cancel(id=id)

    time.sleep(3)
    
    loading_screen.destroy()



    print("starting gui...")
    #global app
    app = Application(lock=product_file_lock)
    app.after(1500, check_main, app, 1500)

    try:
        app.mainloop()
    except KeyboardInterrupt:
        terminate()


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        terminate()

    signal.signal(signal.SIGINT, signal_handler)


