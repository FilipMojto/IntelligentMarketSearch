from tkinter import *

import config_paths as cfg

from AOSS.gui.product_specification import ProductSpecificationMenu
from AOSS.gui.shopping_list import ShoppingListFrame
from AOSS.gui.market_explorer import MarketExplorerFrame
from AOSS.structure.shopping import MarketHub

class MainView(Frame):

    def __init__(self, *args, root: Tk, market_hub: MarketHub, **kw):
        super(MainView, self).__init__(*args, **kw)
        self.root = root

        self.market_hub = market_hub

     


        # ------- Frame Layout ------- #

        self.columnconfigure(0, weight=1, minsize=400)
        self.columnconfigure(1, weight=3, minsize=265)
        self.columnconfigure(2, weight=1, minsize=460)
        self.rowconfigure(0, weight=1)


        # ------- ShoppingListFrame Configuration ------- #

        self.shopping_list = ShoppingListFrame(self, text="Shopping List", bg='dimgrey', font=('Arial', 18, 'bold'), labelanchor='n',
                                               bd=3)
        self.shopping_list.grid(row=0, column=1, sticky="NSEW", padx=5)


        # -------- MarketExplorerFrame Configuration -------- #

        self.market_explorer_frame = MarketExplorerFrame(self,
                                                         text='Market Explorer',
                                                         root=self,
                                                         bg='dimgrey',
                                                         font=('Arial', 18, 'bold'),
                                                         market_hub=self.market_hub,
                                                         shopping_list_frame=self.shopping_list)
        
        self.market_explorer_frame.grid(row=0, column=2, sticky="NSEW")


        # -------- ProductSpecificationMenu Configuration -------- #

        self.specification_menu = ProductSpecificationMenu(self, text="Product Specification", bg='dimgrey', font=('Arial', 18, 'bold'),
                                                           bd=3,
                                                           shopping_list_frame=self.shopping_list,
                                                           market_explorer_frame=self.market_explorer_frame,
                                                           root=self.root)
        self.specification_menu.grid(row=0, column=0, sticky="NSEW", padx=5)

        

        