__ALL__ = ['Application']
__AUTHOR__ = "Evening Programmer"
__VERSION__ = "1.0.0"

import tkinter

import config_paths
from AOSS.gui.main_shopping_view import MainShoppingView


class Application:

    def __init__(self) -> None:
        self.__app = tkinter.Tk()

        self.__app.title("AOSS Application 1.2.0")
        self.__app.geometry("900x500")
        self.__app.minsize(700, 500)
        
        self.__main_shoppping_view = MainShoppingView(self.__app, product_file=config_paths.PRODUCT_FILE_PATH)
        self.__main_shoppping_view.grid(row=0, column=0, sticky="NSEW", padx=10)

        self.__app.rowconfigure(0, weight=1)
        self.__app.columnconfigure(0, weight=1)
        

        self.__app.mainloop()

if __name__ == "__main__":
    app = Application()

