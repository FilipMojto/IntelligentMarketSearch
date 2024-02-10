__ALL__ = ['Application']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"


import tkinter
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
from AOSS.structure.marketing import GUI_START_SIGNAL

def terminate():
    print("Terminating GUI process...")
    os._exit(0)

def signal_handler(signum, frame):

    if signum == signal.SIGINT:
        terminate()

class Application(tkinter.Tk):

    def __init__(self, *args, **kw) -> None:
        super(Application, self).__init__(*args, **kw)
        #self.__app = tkinter.Tk()

        self.title("AOSS Application 1.2.0")
        self.geometry("1000x580")
        self.minsize(700, 500)
        
        self.__main_shoppping_view = MainShoppingView(self, product_file=PRODUCT_FILE['path'], bg='black')
        self.__main_shoppping_view.grid(row=0, column=0, sticky="NSEW", padx=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        

        #self.mainloop()

app: Application = None

def __start_app():
    global app
    app = Application()
    app.mainloop()

def check(main_to_all: mpr_conn.PipeConnection):
    
    if main_to_all.poll(timeout=0.01):  # Check if there is data in the connection
        data = main_to_all.recv()

        if data == "-end":
            terminate()


    app.after(1500, check, main_to_all)



def start(main_to_all: mpr_conn.PipeConnection = None, hub_to_gui: mpr.Queue = None):
    
    if main_to_all is None:
        __start_app()
    else:
        
        while True:
            if not hub_to_gui.empty() and hub_to_gui.get(block=False) == GUI_START_SIGNAL:
                break

            time.sleep(1.5)

        print("starting gui...")
        global app
        app = Application()
        app.after(1500, check, main_to_all)

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

# __ALL__ = ['Application']
# __AUTHOR__ = "Evening Programmer"
# __VERSION__ = "1.0.0"

# import tkinter
# import os
# import sys
# import signal
# import multiprocessing as mpr
# import multiprocessing.connection as mpr_conn
# import time
# from AOSS.gui.main_shopping_view import MainShoppingView
# from config_paths import PRODUCT_FILE

# def terminate():
#     print("Terminating GUI process...")
#     os._exit(0)

# def signal_handler(signum, frame):
#     if signum == signal.SIGINT:
#         terminate()

# class Application(tkinter.Tk):
#     def __init__(self, main_queue, *args, **kw) -> None:
#         super(Application, self).__init__(*args, **kw)
#         self.title("AOSS Application 1.2.0")
#         self.geometry("900x500")
#         self.minsize(700, 500)
        
#         self.__main_shopping_view = MainShoppingView(self, product_file=PRODUCT_FILE['path'])
#         self.__main_shopping_view.grid(row=0, column=0, sticky="NSEW", padx=10)

#         self.rowconfigure(0, weight=1)
#         self.columnconfigure(0, weight=1)

#         self.main_queue = main_queue
#         self.after(1500, self.check_main_queue)

#     def check_main_queue(self):
#         while not self.main_queue.empty():
#             data = self.main_queue.get()
#             print("Received data:", data)
#             if data is not None and data == "-end":
#                 terminate()

#         self.after(1500, self.check_main_queue)

# def gui_process(main_queue):
#     app = Application(main_queue)
#     app.mainloop()

# def start(main_to_all: mpr_conn.PipeConnection = None):
#     main_queue = mpr.Queue()

#     if main_to_all is None:
#         __start_app()
#     else:
#         gui_proc = mpr.Process(target=gui_process, args=(main_queue,))
#         gui_proc.start()
#         print("HERE")
#         try:
#             while True:
#                 if main_to_all.poll(timeout=0.1):  # Check if there is data in the connection
#                     data = main_to_all.recv()
#                     main_queue.put(data)
#                 time.sleep(1.5)
#                 print("HERE")
#         except KeyboardInterrupt:
#             terminate()
#         finally:
#             gui_proc.terminate()

# if __name__ == "__main__":
#     try:
#         start()
#     except KeyboardInterrupt:
#         terminate()