from tkinter import *
from tkinter.ttk import Combobox

import threading
import multiprocessing as mpr
from typing import List, Dict
#import math

import config_paths as cfg

from AOSS.gui.shopping_list import ShoppingListFrame, ShoppingListItem, ShoppingListDetails
from AOSS.gui.utils import CircularProgress
from AOSS.structure.shopping import MarketHub, ProductCategory
from AOSS.components.marrec import MarketExplorer
from AOSS.other.utils import TextEditor



def bind_widgets_recursive(widget, event, handler):
    widget.bind(event, handler)
    for child in widget.winfo_children():
        bind_widgets_recursive(child, event, handler)




class Table(Frame):
    def __init__(self, *args, rows: int, columns: int, **kw):
        super(Table, self).__init__(*args, **kw)

        self.rows = rows
        self.columns = columns
        self.cells: List[List[Label]] = []

        self.config(bg='black')

        for i in range(columns):
            self.columnconfigure(i, weight=1)


        for i in range(rows):
            self.cells.append([])
            self.rowconfigure(i, weight=1)

            for g in range(columns):
                self.cells[i].append(Label(self, text="", font=("Arial", 13)))
                self.cells[i][g].grid(row=i, column=g, sticky="NSEW", padx=3, pady=3)
    
    def col_proportion(self, values: tuple[int, ...]):

        if len(values) != self.columns:
            raise ValueError("Invalid amount of columns!")
        
        for i in range(self.columns):
            self.columnconfigure(index=i, weight=values[i])
        
        

    
    def insert_value(self, row: int, column: int, value: str | int | float | PhotoImage | Widget):

        if isinstance(value, PhotoImage):
            self.cells[row][column].config(text="", image=value, compound='center')
        elif isinstance(value, str):
            self.cells[row][column].config(text=value)
        elif isinstance(value, int) or isinstance(value, float):
            self.cells[row][column].config(text=str(value))            
        elif isinstance(value, Widget):
            self.cells[row][column].destroy()
            self.cells[row][column] = value
            self.cells[row][column].grid(row=row, column=column, sticky="NSEW")

            #print(self.cells[row][column].grid_info())
        else:
            raise TypeError("Unkown type of value!")
        
        




class ExplorationTable(Frame):

    ROW_COUNT = 4

    def __init__(self, *args, market_hub: MarketHub, **kw):
        super(ExplorationTable, self).__init__(*args, **kw)
        
        self.market_hub = market_hub
        self.markets = market_hub.markets()


        self.cells: List[List[ tuple[StringVar, Label] ]] = []
        market_count = len(self.markets)



        for i in range(self.ROW_COUNT):
            self.cells.append([])

            pad_y = 2

            if i == 0:
                pad_y = (5, 2)
            elif i == self.ROW_COUNT - 1:
                pad_y = (2, 5)


            for g in range(market_count + 1):

                var = StringVar()
                var.set(value="")
                label = Label(self, textvariable=var, font=("Arial",  12, "bold"))

                pad_x = 2

                if g == 0:
                    pad_x = (5, 2)
                elif g == market_count:
                    pad_x = (2, 5)

                label.grid(row=i, column=g, sticky="NSEW", padx=pad_x, pady=pad_y)

                self.cells[i].append( (var, label) )

        for i in range(4):
            self.columnconfigure(i, weight=1, minsize=100)

        for g in range(4):
            self.rowconfigure(g, weight=1)



    
       # self.cells[0][0][0].set(value="Name")
       # self.cells[0][0][1].config(font=('Arial', 13, 'bold', 'underline'))
    
        self.cells[1][0][0].set(value="Total Price")
        self.cells[1][0][1].config(font=('Arial', 13, 'bold', 'underline'))

        self.cells[2][0][0].set(value="Succession Rate")
        self.cells[2][0][1].config(font=('Arial', 13, 'bold', 'underline'))

        self.cells[3][0][0].set(value="Recommended")
        self.cells[3][0][1].config(font=('Arial', 13, 'bold', 'underline'))


        for index, market in enumerate(self.markets):
            self.cells[0][index + 1][0].set(value=market.name().lower())



    def insert_value(self, row: int, col: int, value: object | PhotoImage):
        
        # here we insert an image or icon instead of text
        if isinstance(value, PhotoImage):
            self.cells[row][col][0].set("")
            self.cells[row][col][1].config(image=value, compound='center')
        else:
            self.cells[row][col][0].set(value=value)




class ExplorerView(Frame):
    def __init__(self, *args, market_hub: MarketHub, **kw):
        super(ExplorerView, self).__init__(*args, **kw)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.columnconfigure(0, weight=1)

        self.table = ExplorationTable(self, bg='black', market_hub=market_hub)
        self.table.grid(row=0, column=0, sticky="NSEW", pady=5)

        self.detailed_results = LabelFrame(self,
                                           bg='dimgrey',
                                           text='Product Details',
                                           font=('Arial', 15, 'bold'))
        
        self.detailed_results.grid(row=1, column=0, sticky="NSEW", pady=5)
        self.detailed_results.rowconfigure(0, weight=1, minsize=50)
        self.detailed_results.rowconfigure(1, weight=200)
        self.detailed_results.columnconfigure(0, weight=1)

        self.detailed_results_table = Table(self.detailed_results, rows=4, columns=3)
        self.detailed_results_table.grid(row=0, column=0, sticky="NSEW")
        self.detailed_results_table.col_proportion(values=(2, 40, 1))


        self.detailed_results_padding = Frame(self.detailed_results, bg='dimgrey')
        self.detailed_results_padding.grid(row=1, column=0, sticky="NSEW")

        


        #self.label = Label(self, text="SO FAR EMPTY!")
       # self.grid(row=0, column=0, sticky='NSEW')

        


class MarketExplorerFrame(LabelFrame):
    def __init__(self, *args, root: Tk, market_hub: MarketHub, shopping_list_frame: ShoppingListFrame,
                 **kw):
        super(MarketExplorerFrame, self).__init__(*args, **kw)

        self.accept_icon = PhotoImage(file=cfg.ACCEPT_ICON).subsample(18, 18)
        self.decline_icon = PhotoImage(file=cfg.DECLINE_ICON).subsample(18, 18)
        
        self.root = root
        self.shopping_list = shopping_list_frame
        self.market_hub = market_hub
        self.markets = market_hub.markets()
        self.market_explorer = MarketExplorer(market_hub=market_hub, limit=5)


        self.product_items: List[ShoppingListItem] = []
        self.explorations: List[List[MarketExplorer.Exploration]] = []

        # ---- Frame Configuration ---- #

        self.rowconfigure(0, weight=40)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

        # ---- ExplorerView Configuration ---- #

        self.explorer_view = ExplorerView(self, market_hub=market_hub, bg='dimgrey')
        self.explorer_view.grid(row=0, column=0, sticky="NSEW")

        # ---- ControlPanel Configuration ---- #

        self.control_panel = Frame(self)
        self.control_panel.grid(row=1, column=0, sticky="NSEW")
        self.control_panel.rowconfigure(0, weight=1)
        self.control_panel.columnconfigure(0, weight=1)
        self.control_panel.columnconfigure(1, weight=1)
        

        self.delete_button = Button(self.control_panel,
                                    text="delete",
                                    font=('Arial', 13),
                                    command=self.delete_product,
                                    width=10)
                                    
        self.delete_button.grid(row=0, column=0, sticky="ENSW", padx=3, pady=(5, 12))
        

        self.search_button = Button(self.control_panel,
                                    text="search",
                                    font=("Arial", 13),
                                    command=self.explore_markets,
                                    state='disabled',
                                    width=10)
        self.search_button.grid(row=0, column=1, sticky="EWSN", padx=3, pady=(5, 12))

        self.search_bar = CircularProgress(self.control_panel, width=30, height=30)

        self.explorer_view.detailed_results_table.insert_value(row=0, column=0, value="Market")
        self.explorer_view.detailed_results_table.insert_value(row=0, column=1, value="Product")
        self.explorer_view.detailed_results_table.insert_value(row=0, column=2, value="Price")
    
    
    def delete_product(self):
        item = self.shopping_list.product_list.remove_selected_item(return_=True)
        
        if item is None:
            return
        
    
        if not self.shopping_list.product_list.items:
            self.search_button.config(state='disabled')


        self.market_explorer.remove_target(ID=item.details.ID)
        self.product_items.remove(item)
        

    def combobox_selected(self, event, box: Combobox):
        info = box.grid_info()
        cur_price = float(self.explorer_view.detailed_results_table.cells[info['row']][info['column'] + 1].cget('text'))
        new_price = self.product_price_mappings[info['row'] - 1][box.get()]
        market = self.explorer_view.detailed_results_table.cells[info['row']][info['column'] - 1].cget('text')
        for i in range(len(self.markets)):
            
            if self.explorer_view.table.cells[0][i + 1][0].get() == market:

                original_val = float(self.explorer_view.table.cells[1][i + 1][0].get())

                self.explorer_view.table.insert_value(row=1, col=i + 1, value=round(original_val + (new_price - cur_price), 2))


        self.explorer_view.detailed_results_table.insert_value(row=info['row'], column=info['column'] + 1, value=
                                              self.product_price_mappings[info['row'] - 1][box.get()])
        
        self.refresh_recommendation()
        



    def show_product_details(self, event, item: ShoppingListItem, index: int):
        item.on_item_clicked(event=event)
        

        products: List[List[str]] = []
        prices: List[List[float]] = []

        market_len = len(self.markets)

        self.product_price_mappings: List[Dict[str, float]] = []

        for i in range(market_len):
            self.product_price_mappings.append({})

        for i in range(market_len):
            products.append([])
            prices.append([])

        markets = []
       # prices = []

        for i in range(market_len):
            
            #k = (i * 5) + 5

            markets.append(self.explorations[i][0].market_ID)
            prices.append(self.explorations[i][0].products[0][1].price)

            for g in range(5):
                expl = self.explorations[i][g]
                self.product_price_mappings[i][expl.products[index][1].name] = expl.products[index][1].price
                products[i].append(expl.products[index][1].name)
                prices[i].append(expl.products[index][1].price)

            # for g in range(i * 5, (i * 5) + 5):
                
            #     expl = self.explorations[g]
            #     self.product_price_mappings[i][expl.products[index][0].name] = expl.products[index][0].price
            #     products[i].append(expl.products[index][0].name)
            #     prices[i].append(expl.products[index][0].price)


                # for index, product in enumerate(expl.products):

                    
                #     products[index % len(self.product_data)] = product[0].name


        combo_boxes = []

        for i in range(market_len):
            box = Combobox(self.explorer_view.detailed_results_table, state='readonly')
            #text = products[i]
            box['values'] = products[i]
            box.set(box['values'][0])
            box.bind('<<ComboboxSelected>>', lambda event, box=box: self.combobox_selected(event, box=box))
   
            combo_boxes.append(box)


        for i, market in enumerate(markets):
            self.explorer_view.detailed_results_table.insert_value(row=i + 1, column=0,
                                                                    value=self.market_hub.market(
                                                                        identifier=market
                                                                    ).name().lower())
            self.explorer_view.detailed_results_table.insert_value(row=i + 1, column=1,
                                                                    value=combo_boxes[i])
            self.explorer_view.detailed_results_table.insert_value(row=i + 1, column=2,
                                                                    value=prices[i][0])

        # for index, expl in enumerate(self.exploration):
            
        #     if index % (5 * len(self.product_data)) == 0:
        #         products.clear()
        #         self.explorer_view.detailed_results_table.insert_value(row=index + 1, column=0,
        #                                                             value=self.market_hub.market(identifier=expl.market_ID).name().lower())
        #     else:



        # for index, expl in enumerate(self.exploration):
        #     self.explorer_view.detailed_results_table.insert_value(row=index + 1, column=0,
        #                                                             value=self.market_hub.market(identifier=expl.market_ID).name().lower())

        #     combo_box = Combobox(self.explorer_view.detailed_results_table)

        #     products = []

        #     for product in enumerate(expl.products):
        #         products.append()

        #     #acombo_box['values'] = tuple(expl.)


        #     self.explorer_view.detailed_results_table.insert_value(row=index + 1, column=1,
        #                                                            value=expl.products[item.ID - 1][0].name)
        #     self.explorer_view.detailed_results_table.insert_value(row=index + 1, column=2,
        #                                                            value=expl.products[item.ID - 1][0].price)



    def create_handler(self, item, index):
        return lambda event: self.show_product_details(event=event, index=index, item=item)    


    def refresh_recommendation(self):
        best_market: List[tuple[str, float]] = []

        for i in range(len(self.markets)):

            if not best_market or best_market[0][1] == float(self.explorer_view.table.cells[1][i + 1][0].get()):
                best_market.append(( self.explorer_view.table.cells[0][i + 1][0].get(),
                                    float(self.explorer_view.table.cells[1][i + 1][0].get()) ))
            else:
                if best_market[0][1] > float(self.explorer_view.table.cells[1][i + 1][0].get()):
                    best_market.clear()
                    best_market.append(( self.explorer_view.table.cells[0][i + 1][0].get(),
                                    float(self.explorer_view.table.cells[1][i + 1][0].get()) ))
             

        for i in range(len(self.markets)):

            for market, price in best_market:

                if self.explorer_view.table.cells[0][i + 1][0].get() == market:
                    self.explorer_view.table.insert_value(row=3, col=i + 1,
                                                          value=self.accept_icon)
                else:
                    self.explorer_view.table.insert_value(row=3, col=i + 1,
                                                          value=self.decline_icon)

    def explore_product(self, item: ShoppingListItem):

        self.product_items.append(item)

        category = None if item.details.category == 0 else ProductCategory(value=item.details.category)
    
        item_data = [(item.details.ID,
                      TextEditor.standardize_str(item.details.name),
                      category,
                      item.details.amount)]
        
        self.market_explorer.explore(product_list=item_data)
        #self.product_data.extend(item_data)


    def serch_markets(self):
        
        # self.product_data = self.shopping_list.product_list.get_items()
        # self.items = self.shopping_list.product_list.items
        
        #bind_widgets_recursive(widget=self.items[0], event="<Button-1>", handler=lambda event: self.show_product_details(event=event, item=self.items[0].details))
        #bind_widgets_recursive(widget=self.items[1], event="<Button-1>", handler=lambda event: self.show_product_details(event=event, item=self.items[1].details))

        

        for i, item in enumerate(self.product_items):
            bind_widgets_recursive(widget=item, event="<Button-1>", handler=self.create_handler(index=i, item=item))
            #bind_widgets_recursive(widget=item, event="<Button-1>", handler=self.do_sth)

            #item.bind_widgets_recursive(event="<Button-1>", handler=lambda event: self.show_product_details(event=event, item=item.details))

        #self.items[0].bind_class(self.items[0].winfo_class(), "<Button-1>", lambda event, item=self.items[0]: self.show_product_details(event, item.details))
        #self.items[1].bind_class(self.items[1].winfo_class(), "<Button-1>", lambda event, item=self.items[1]: self.show_product_details(event, item.details))

        #self.items[0].bind_class("<Button-1>", lambda event: self.show_product_details(event, self.items[0].details))
        #self.items[1].bind_class("<Button-1>", lambda event: self.show_product_details(event, self.items[1].details))

        
        # def create_lambda_handler(item):
        #     return lambda event, item=item: self.show_product_details(event, item.details)
    
        # for item in self.items:
        #     item.bind_all("<Button-1>", create_lambda_handler(item))

           # item.bind_all("<Button-1>", lambda event, item=item: self.show_product_details(event, item))

        #self.exploration = self.market_explorer.explore(product_list=self.product_data, metric='price', limit=5)
        
        #self.market_explorer.expected_size(size=len(self.product_items))
        self.explorations = self.market_explorer.get_explorations()
        best_market = []
        best_market.append((self.explorations[0][0].market_ID, self.explorations[0][0].total_price))


        
        for index, expl in enumerate(self.explorations):
            expl = expl[0]

            #if index % 5 == 0:
            if best_market[0][1] > expl.total_price:
                best_market.clear()
                best_market.append((expl.market_ID, expl.total_price))
            elif best_market[0][1] == expl.total_price:
                best_market.append((expl.market_ID, expl.total_price))
            
            #assert(expl.total_price >= best_price)

            
            self.explorer_view.table.insert_value(row=0, col=expl.market_ID, value=self.market_hub.market(identifier=expl.market_ID).name().lower())
            self.explorer_view.table.insert_value(row=1, col=expl.market_ID, value= round(expl.total_price, 2))
            self.explorer_view.table.insert_value(row=2, col=expl.market_ID, value=expl.succession_rate)
            
        self.explorations = self.market_explorer.get_explorations(metric='price')
        #self.market_explorer.clear_buffer()

        for index, expl in enumerate(self.explorations):
            expl = expl[0]

           # if index % 5 == 0:
            if any([market == expl.market_ID for market, price in best_market]):
                self.explorer_view.table.insert_value(row=3, col=expl.market_ID, value=self.accept_icon)
            else:
                self.explorer_view.table.insert_value(row=3, col=expl.market_ID, value=self.decline_icon)
            
                

        #best_price = self.explorations[0][0].total_price

        self.search_bar.grid_forget()
        self.search_bar.config(state="disabled")
        self.search_button.config(text="search")



    def explore_markets(self):
        self.search_button.config(text="")
        #self.search_button.set

        #self.search_bar = CircularProgress(self.control_panel, width=40, height=40)
        self.search_bar.grid(row=0, column=1, pady=(5, 12))
        self.search_bar.config(state="normal")
        # self.control_panel.columnconfigure(0, weight=1)
        # self.control_panel.columnconfigure(1, weight=1)


        thread = threading.Thread(target=self.serch_markets)
        thread.start()

    




        
        

