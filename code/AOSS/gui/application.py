__ALL__ = ['Application']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "2.2.0"


import tkinter
import os, sys
import multiprocessing as mpr


# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)


from config_paths import *
from main_view import MainView
from AOSS.structure.shopping import MarketHub



class Application(tkinter.Tk):



    # def on_key_press(self, event, main_view: MainView):

    #     key_pressed = event.keysym

    #     if key_pressed == "Delete":
    #         main_view.market_explorer_window.delete_product()

            
    def __init__(self, *args, lock: mpr.Lock = None, gui_to_hub: mpr.Queue = None, **kw) -> None:
        super(Application, self).__init__(*args, **kw)
        

        self.market_hub = MarketHub(src_file=MARKET_HUB_FILE['path'])
        self.market_hub.load_markets()

        if lock:
            with lock:
                self.market_hub.load_products()
        else:
            self.market_hub.load_products()

        self.title("AOSS Application " + __VERSION__)
        self.geometry("1070x570")

        
        self.main_view = MainView(self, root=self, app_version=__VERSION__, market_hub=self.market_hub, gui_to_hub=gui_to_hub, bg='lightblue')
        self.main_view.pack(side='left', fill='both', expand=True, padx=10)

        # self.bind("<Key>", lambda event, main_view=self.main_view: self.on_key_press(event, main_view))
        
        self.bind("<Key>", lambda event, main_view=self.main_view: main_view.on_key_press(event, main_view))







# def start(main_to_all: mpr.Queue = None, gui_to_main: mpr.Queue = None, hub_to_gui: mpr.Queue = None, gui_to_hub: mpr.Queue = None, 
#           product_file_lock: mpr.Lock = None):
    
#     #UPDATE_FINISH_SIGNAL = 1

#     """
#         This function starts a GUI process for AOSS app.

#         Parameters:

#             a) main_to_all - a Queue instance which is used by the main process to broadcast its signals
#                             to all subprocesses

#             b) hub_to_gui - a Queue instance which is used by the Marketing Process to communicate with
#                             Gui Process
#     """




#     app: Application = None
#     update_thread: threading.Thread = None


#     def __start_app(lock: mpr.Lock = None):
#         nonlocal app
#         app = Application(lock)
#         app.mainloop()

#     if main_to_all is None:
#         __start_app()
#         terminate()
    


#     def check_main(window: tkinter.Tk = None, repeat_after: int = -1):

#         nonlocal main_to_all
        
#         if main_to_all.value:
#             terminate()
        

#         # if not main_to_all.empty() and main_to_all.get(block=False) == "-end":
#         #     terminate()

#         if repeat_after >= 0:
#             window.after(repeat_after, check_main, window)

#     loading_screen_after_ids = []

#     def check_progress_report(main_to_all: mpr_conn.PipeConnection, hub_to_gui: mpr.Queue):
        
#         nonlocal loading_screen
#         nonlocal loading_screen_after_ids
#         check_main(window=loading_screen, repeat_after=-1)

#         try:
#             if not hub_to_gui.empty():
#                 signal = hub_to_gui.get(block=False)
                
#                 if signal[0] == PROGRESS_BAR_SIGNAL:

#                     assert(0<=signal[1]<=100)

#                     loading_screen.progress_bar['value'] = signal[1]
#                     loading_screen.update_idletasks()

            
#                     if signal[1] == PRP.FINISHING_POINT:
#                         loading_screen.info_text.config(text="finishing...")
#                         loading_screen.after(500, loading_screen.quit)
#                         return
                    
#                     elif signal[1] == PRP.TRAINING_MARKET_ANALYSIS:
#                         loading_screen.info_text.config(text=PR[PRP.TRAINING_MARKET_ANALYSIS])
#                     elif signal[1] == PRP.MARKETS_ANALYSIS:
#                         loading_screen.info_text.config(text=PR[PRP.MARKETS_ANALYSIS])
#                     elif PRP.MARKETS_ANALYSIS<=signal[1]<PRP.UPDATING_DATA:
#                         loading_screen.info_text.config(text=PR[PRP.SCRAPING_MISSING_DATA])
#                     elif signal[1] == PRP.UPDATING_DATA:
#                         loading_screen.info_text.config(text=PR[PRP.SCRAPING_MISSING_DATA])

                
    
#             # Schedule the next after() call and save the after ID
#             loading_screen_after_ids.append(loading_screen.after(1500, check_progress_report, main_to_all, hub_to_gui))

#         # loading_screen_after_ids = [id for id in loading_screen_after_ids if loading_screen.after(id, None) is not None]
#             #time.sleep(1.5)
#         except KeyboardInterrupt:
#             terminate()

#     def update(app: Application, gui_to_hub: mpr.Queue, lock: mpr.Lock):
        
#         start = time.time()

#         with lock:
#             end = time.time()
#             print(f"time: {end - start}")
#             app.market_hub.load_dataset()
        
#         while gui_to_hub.full():

#             print("Hub's queue full! Retrying...")
#             time.sleep(1)
        
#         gui_to_hub.put(obj=(UPDATE_PRODUCTS_SIGNAL, 1))
        


        

        

    
#     def check_update_signal(app: Application, lock: mpr.Lock, hub_to_gui: mpr.Queue, gui_to_hub: mpr.Queue, repeat_after: int):
#         nonlocal update_thread

#         if not hub_to_gui.empty() and hub_to_gui.get(block=False)[0] == UPDATE_PRODUCTS_SIGNAL:

#             if update_thread and update_thread.is_alive():
#                 update_thread.join()

            
#             update_thread = threading.Thread(target=update, args=(app, gui_to_hub, lock))
#             update_thread.start()



#         app.after(repeat_after, check_update_signal, app, lock, hub_to_gui, gui_to_hub, repeat_after)


#     def set_update_interval(sec: int):
#         nonlocal gui_to_hub

#         gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, sec))

   
    
#     # starting the loadscreen
#     loading_screen = LoadingScreen()
#     loading_screen.after(1500, check_progress_report, main_to_all, hub_to_gui)
#     loading_screen.mainloop()

#     # here we remove any scheduled functions
#     for id in loading_screen_after_ids:
#         loading_screen.after_cancel(id=id)

#     time.sleep(3)
    
#     loading_screen.destroy()



#     print("starting gui...")
#     #global app
#     app = Application(lock=product_file_lock, gui_to_hub=gui_to_hub)
#     app.after(1500, check_main, app, 1500)
#     time.sleep(1)
#     app.after(1500, check_update_signal, app, product_file_lock, hub_to_gui, gui_to_hub, 1500)

#     try:
#         app.mainloop()
#     except KeyboardInterrupt:
#         pass

#     gui_to_main.put(obj=GUI_TERMINATION_SIGNAL)

#     while True:
#         check_main()
#         time.sleep(1)

    
#     #terminate(gui_to_main=gui_to_main)


# if __name__ == "__main__":
#     try:
#         start()
#     except KeyboardInterrupt:
#         terminate()

#     signal.signal(signal.SIGINT, signal_handler)


if __name__ == '__main__':

    # signal.signal(signal.SIGINT, signal_handler)
    app = Application()
    app.mainloop()