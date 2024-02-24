__ALL__ = ['Application']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"


import tkinter
from tkinter import TclError
import os, sys
import signal, multiprocessing as mpr, multiprocessing.connection as mpr_conn
import threading
import threading as thrd
import time


# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)

from config_paths import *
from AOSS.gui.main_view import MainView
from AOSS.gui.loading_screen import LoadingScreen
from AOSS.structure.marketing import GUI_START_SIGNAL, GUI_UPDATE_SIGNAL
from AOSS.structure.shopping import MarketHub

def terminate():
    print("Terminating GUI process...")
    os._exit(0)

def signal_handler(signum, frame):

    if signum == signal.SIGINT:
        terminate()

class Application(tkinter.Tk):

    def on_key_press(self, event, main_view: MainView):

        key_pressed = event.keysym

        if key_pressed == "Delete":
            main_view.market_explorer_frame.delete_product()

            
    def __init__(self, *args, lock: mpr.Lock = None, **kw) -> None:
        super(Application, self).__init__(*args, **kw)
        #self.__app = tkinter.Tk()

        self.market_hub = MarketHub(src_file=MARKET_HUB_FILE['path'])
        self.market_hub.load_markets()

        if lock:
            with lock:
                self.market_hub.load_products()

        self.title("AOSS Application 1.2.0")
        #app = Tk()
    #app.geometry("1295x520")
        self.geometry("1295x520")
        #self.minsize(700, 500)
        
        self.main_view = MainView(self, root=self, market_hub=self.market_hub,  bg='black')
        self.main_view.grid(row=0, column=0, sticky="NSEW", padx=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.bind("<Key>", lambda event, main_view=self.main_view: self.on_key_press(event, main_view))
        

        #self.mainloop()








def start(main_to_all: mpr.Queue = None, hub_to_gui: mpr.Queue = None, gui_to_hub: mpr.Queue = None, 
          product_file_lock: mpr.Lock = None):
    
    UPDATE_FINISH_SIGNAL = 1

    """
        This function starts a GUI process for AOSS app.

        Parameters:

            a) main_to_all - a Queue instance which is used by the main process to broadcast its signals
                            to all subprocesses

            b) hub_to_gui - a Queue instance which is used by the Marketing Process to communicate with
                            Gui Process
    """




    app: Application = None
    update_thread: threading.Thread = None
    progress_signal_mappings = {
        GUI_START_SIGNAL/6: "analyzing training market...",
        GUI_START_SIGNAL/3: "analyzing the rest of markets...",


    }


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

        
                if progress == GUI_START_SIGNAL:
                    loading_screen.info_text.config(text="finishing...")
                    loading_screen.after(500, loading_screen.quit)
                    return
                
                elif progress == (GUI_START_SIGNAL/6):
                    loading_screen.info_text.config(text="analyzing training market...", font=('Arial', 11))
                elif progress == (GUI_START_SIGNAL/3):
                    loading_screen.info_text.config(text="analyzing markets...", font=('Arial', 11))
                # elif progress == (GUI_START_SIGNAL/3):
                #     loading_screen.info_text.config(text="analyzing markets...", font=('Arial', 11))
                elif 0<=progress<100:
                    loading_screen.info_text.config(text="scraping missing products...", font=('Arial', 11))
                
                
    
            # Schedule the next after() call and save the after ID
            loading_screen_after_ids.append(loading_screen.after(1500, check_progress_reports, main_to_all, hub_to_gui))

        # loading_screen_after_ids = [id for id in loading_screen_after_ids if loading_screen.after(id, None) is not None]
            #time.sleep(1.5)
        except KeyboardInterrupt:
            terminate()

    def update(app: Application, gui_to_hub: mpr.Queue, lock: mpr.Lock):
        
        start = time.time()

        with lock:
            end = time.time()
            print(f"time: {end - start}")
            app.market_hub.load_dataset()
        
        while gui_to_hub.full():

            print("Hub's queue full! Retrying...")
            time.sleep(1)
        
        gui_to_hub.put(obj=UPDATE_FINISH_SIGNAL)
        


        

        

    
    def check_update_signal(app: Application, lock: mpr.Lock, hub_to_gui: mpr.Queue, gui_to_hub: mpr.Queue, repeat_after: int):
        print("CHECKING!!")
        nonlocal update_thread

        if not hub_to_gui.empty() and hub_to_gui.get(block=False) == GUI_UPDATE_SIGNAL:

            if update_thread and update_thread.is_alive():
                update_thread.join()
                #time.sleep(0.3)
            

            print("NOW")
            update_thread = threading.Thread(target=update, args=(app, gui_to_hub, lock))
            update_thread.start()



        app.after(repeat_after, check_update_signal, app, lock, hub_to_gui, gui_to_hub, repeat_after)



   
    
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
    time.sleep(1)
    app.after(1500, check_update_signal, app, product_file_lock, hub_to_gui, gui_to_hub, 1500)

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


