from typing import List

from tkinter import *
from tkinter import ttk

import config_paths
from matching import ProductMatcher

# --- ShoppingListItem - Class Declaration&Definition --- #

class ShoppingListItem(Frame):
    
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self, *args, **kw):
        super(ShoppingListItem, self).__init__(*args, **kw)

        self.__label = Label(self, text="ITEM")
        self.__label.grid(row=0, column=0, sticky="NSEW", pady=20, padx=20)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
    
    
# --- ShoppingList - Class Declaration&Definition --- #


class ShoppingList(LabelFrame):
    def __init__(self, *args, **kw):
        super(ShoppingList, self).__init__(*args, **kw)

        self.__canvas = Canvas(self, bg='white', height=100)
        self.__h_scrollbar = Scrollbar(self, orient="horizontal", command=self.__canvas.xview)

        self.__canvas.grid(row=0, column=0, sticky="WNSE")
        self.__h_scrollbar.grid(row=1, column=0, sticky="WESN")

        self.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.__canvas.configure(xscrollcommand=self.__h_scrollbar.set)

        self.__inner_frame = Frame(self.__canvas)
        self.__inner_frame.grid(row=0, column=0, sticky="WNE")

        self.__canvas.create_window((0, 0), window=self.__inner_frame, anchor="nw")
        self.__inner_frame.bind("<Configure>", self.on_frame_configure)

        self.__items: List[ShoppingListItem] = []
    
    def on_frame_configure(self, event):
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))
        


    def insert_item(self):
        item = ShoppingListItem(self.__inner_frame)

        item.grid(row=0, column=len(self.__items), sticky="WNS")
        self.columnconfigure(len(self.__items))

        self.__items.append(item)


class ProductMatchView(Frame):
    def __init__(self, *args, **kw):
        super(ProductMatchView, self).__init__(*args, **kw)

        self.__entry = Entry(self, width=33)
        self.__entry.grid(row=0, column=0, sticky="NSW")

        # self.menu = Menu(self, tearoff=1)
        # e

        # self.combo_box = ttk.Combobox(self, width=30)
        # self.combo_box.grid(row=1, column=0, sticky="NSW")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)

    def read_entry(self):
        return self.__entry.get()



class ProductSearchView(Frame):
    def __init__(self, *args, product_file: str, **kw):
        super(ProductSearchView, self).__init__(*args, **kw)

        self.__product_match_view = ProductMatchView(self)
        self.__product_match_view.grid(row=0, column=0, sticky="NSE")

        self.__button = Button(self, width=25, text="Search", font=("Bold", 10), command=self.__on_button_clicked)
        self.__button.grid(row=0, column=1, sticky="NSW")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.__product_matcher = ProductMatcher(product_file=product_file)
    
    def __on_button_clicked(self):
        product_matches = self.__product_matcher.match(text=self.__product_match_view.read_entry(), headerless=False)

        haa = []

        #self.__menu = Menu(self, tearoff=1)

        for match in product_matches:
            for key, value in match.items():
                #haa.append(key.name())
                self.__product_match_view.menu.add_command(label=key.name())

        #self.__product_match_view.combo_box['values'] = tuple(haa)
        

# --- MainShoppingView - Class Declaration&Definition --- #

class MainShoppingView(Frame):
    
    def __on_new_item_button_click(self):
        self.__shopping_list.insert_item()

    def __init__(self, *args, product_file: str, **kw):
        super(MainShoppingView, self).__init__(*args, **kw)

        self.__icon_image = PhotoImage(file=config_paths.SHOPPING_CART_ICON).subsample(17, 17)
        self.__shopping_list_label = Label(self, text="Shopping List",
                                            image=self.__icon_image, compound='right', font=('Bold', 20), fg='black')

        self.__shopping_list_label.grid(row=0, column=0, sticky="WS")

        self.__shopping_list = ShoppingList(self)#, text="ShoppingList", font=('Bold', 20))
        self.__shopping_list.grid(row=1, column=0, sticky="WNES")
        self.__shopping_list.insert_item()
        self.__shopping_list.insert_item()
        

        self.__product_search_view = ProductSearchView(self, product_file=product_file)
        self.__product_search_view.grid(row=2, column=0, sticky="NEW")

        # self.__new_item_entry = Entry(self, width=25)

        # #self.__new_item_button = Button(self, text="New", font=('Bold', 13), width=25, command=self.__on_new_item_button_click)
        # self.__new_item_entry.grid(row=2, column=0, sticky="NS")
        #self.__combo_box = ttk.Combobox(self, width=25, height=10)
        #self.__combo_box.grid(row=3, column=0, sticky="N")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=10)
        #self.rowconfigure(3, weight=10)

        self.columnconfigure(0, weight=1)