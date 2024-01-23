from tkinter import *

from typing import List

import config_paths
from gui.main_shopping_view import MainShoppingView


class Application:



    def __init__(self) -> None:
        self.__app = Tk()

        # self.__menu = Menu(self.__app)
        # self.__file_menu = Menu(self.__menu, tearoff=0)
        # self.__file_menu.add_command(label="HAH")

        self.__app.title("AOSS Application 1.2.0")
        self.__app.geometry("900x500")
        self.__app.minsize(700, 500)
        
        self.__main_shoppping_view = MainShoppingView(self.__app, product_file=config_paths.PRODUCT_FILE_PATH)
        self.__main_shoppping_view.grid(row=0, column=0, sticky="NSEW")

        self.__app.rowconfigure(0, weight=1)
        self.__app.columnconfigure(0, weight=1)
        
        # self.__icon_image = PhotoImage(file=config_paths.SHOPPING_CART_ICON).subsample(17, 17)
        # self.__shopping_list_label = Label(self.__app, text="Shopping List",
        #                                    image=self.__icon_image, compound='right', font=('Bold', 20), fg='black')

        # self.__shopping_list_label.grid(row=0, column=0, sticky="WS")

        # self.__shopping_list = ShoppingList(self.__app)#, text="ShoppingList", font=('Bold', 20))
        # self.__shopping_list.grid(row=1, column=0, sticky="WNES")
        # self.__shopping_list.insert_item()
        # self.__shopping_list.insert_item()
        
        # self.__new_item_button = Button(self.__app, text="New")
        # self.__new_item_button.grid(row=2, column=0, sticky="N")
        # # label = Label(self.__app, text="HAHA")

        # # label.grid(row=0, column=0, sticky="NSEW")

        # self.__app.rowconfigure(0, weight=1)
        # self.__app.rowconfigure(1, weight=2)
        # self.__app.rowconfigure(2, weight=40)

        # self.__app.columnconfigure(0, weight=1)
        self.__app.mainloop()
