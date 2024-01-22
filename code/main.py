
from tkinter import *
from typing import List, Literal
from product_grid import ProductGrid
from utils import TextEditor
import os

class EnterProductWindow(Toplevel):

    def __init__(self, parent, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.__label = Label(self, text="Enter product name:")
        self.__label.grid(row=0, column=0, sticky="NSEW")

        self.__entry = Entry(self, width=30)
        self.__entry.grid(row=0, column=1, sticky='NSEW')
        
        self.transient(parent)
        self.grab_set()
                


class Product(Frame):
    def __init__(self, *args, ID: int, name: str, **kw):
        super(Product, self).__init__(*args, **kw)

        #name = wrap_text(text=name, index=10)

        self.label = Label(self, text=str(ID))
        self.label.grid(row=0, column=0)
        self.name = Label(self, text=name)
        self.name.grid(row=1, column=0)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.columnconfigure(0, weight=1)

class ShoppingList(Frame):


    def add_product(self, product: tuple):
        prod = Product(self.products_frame, ID=product[0], name= TextEditor.join_text(product[1]), bg='#D2691E')
        prod.pack(side=LEFT, padx=3)
        self.products.append(prod)
        self.update_scrollregion()
    
    def __on_add_click_icon_click(self):
        
        modal_window = EnterProductWindow(self)
    
        # label = Label(modal_window, text="THIS IS MODAL WINDOW")
        # label.grid(row=0, column=0, sticky="NSEW")

        # modal_window.transient(self)
        # modal_window.grab_set()
        self.wait_window(modal_window)


    def __add_click_icon(self):
        
        self.__add_new_button = Button(self.products_frame, command=self.__on_add_click_icon_click, image=self.__click_to_add_icon, compound='center', width=50, height=50, bd=0)
        self.__add_new_button.pack(side=RIGHT, fill=BOTH, expand=True)

        self.update_scrollregion()

    def notify(self, frame: Frame):
        self.add_product((frame.cget('text'), frame.winfo_children()[0].cget('text')))



    def update_scrollregion(self):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, *args, **kw):
        super(ShoppingList, self).__init__(*args, **kw)

        self.products: List[Product] = []
        self.__click_to_add_icon = PhotoImage(file='./add_icon.png').subsample(15, 15)
        self.products_frame = Frame(self, bg='black')
        self.products_frame.grid(row=0, column=0, sticky='WESN')
        self.columnconfigure(0, weight=1)
        
        

        self.canvas = Canvas(self.products_frame, height=50, bg='#53868B')
        self.scrollbar = Scrollbar(self.products_frame, orient="horizontal", command=self.canvas.xview)
        self.products_frame.grid_rowconfigure(0, weight=1)
        self.products_frame.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=0, sticky="ew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.products_frame.rowconfigure(0, weight=1)
        self.products_frame.rowconfigure(1, weight=1)
        self.products_frame.columnconfigure(0, weight=1)


        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.products_frame = Frame(self.canvas, bg='#53868B')
        self.canvas.create_window((0, 0), window=self.products_frame, anchor="nw")

        self.canvas.bind('<Configure>', lambda e: self.update_scrollregion())

        self.__add_click_icon()
        # self.add_product((1, 'Product A'))
        # self.add_product((2, 'Product B'))
        # self.add_product((3, 'Product C'))



class ProductRow(LabelFrame):

    def insert_product(self, product: tuple) -> bool:
        if len(self.__products) == self.__max:
            return False


        product = Product(self, ID=product[0], name=product[1])
        #product.pack(side=LEFT, fill=BOTH, expand=True, padx=0)
        product.grid(row=0, column=self.__cur, sticky='nsew')
        
        #=wrap_textproduct.grid()
        self.columnconfigure(self.__cur, minsize=150)
        self.__cur += 1
        self.__products.append( product )

        #prod = Product(cur_row, ID=int(attributes[0]), name=attributes[2])
        #prod.pack(side=LEFT, fill=BOTH, expand=True, padx=0)
        return True

    def __init__(self, *args, max: int = 6,  **kw):
        super(ProductRow, self).__init__(*args, **kw)

        self.__products: List[Product] = []
        self.__max = max

        super().grid_rowconfigure(0, weight=1)

        for i in range(self.__max):
            super().grid_columnconfigure(i, weight=1)

        self.__cur = 0


    

class ProductList(LabelFrame):

    def __insert_product_row(self):
        print("Expanding..")
        self.product_rows.append(ProductRow(self))

        cur_size = self.grid_size()[1]
        print(cur_size)
        self.product_rows[len(self.product_rows) - 1].grid(row=cur_size, column=0, sticky="EW")
        self.rowconfigure(cur_size, weight=15)


    def __init__(self, *args, shopping_list: ShoppingList,  **kw):
        super(ProductList, self).__init__(*args, **kw)

        self.shopping_list: ShoppingList = shopping_list
        
        self.add_product_button = Button(self, text='Add', command=self.on_button_click)
        self.add_product_button.grid(row=0, column=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.product_rows: List[ProductRow] = []
        self.__insert_product_row()
        

    def load_products(self, path: str = "./resources/products.csv"):

        with open(path, 'r') as file:
            line = file.readline()

            while line:
                attributes = line.strip().split(',')
                
                try:
                    cur_row = self.product_rows[len(self.product_rows) - 1]

                    print(f"Frame: {cur_row.grid_size()[0]}")
                    if not cur_row.insert_product( product= (int(attributes[0]), attributes[2])):
                        self.__insert_product_row()

                except ValueError:
                    pass

                line = file.readline()
        

    def on_button_click(self):
        self.shopping_list.add_product(product=(1, "Random"))

    
    def __ID(self):
        return_val = self.__ID
        self.__ID += 1

        return return_val

class MainShoppingView(Frame):
    def __init__(self, *args, **kw):
        super(MainShoppingView, self).__init__(*args, **kw)

        self.__icon_image = PhotoImage(file='./icon_2.png').subsample(17, 17)
        
        self.label = Label(self, text='Shopping Cart', image=self.__icon_image, compound='right', font=('Bold', 18), fg='black')
        self.label.grid(row=0, column=0, sticky='W', padx=5)
        
        self.shopping_list = ShoppingList(self, bg='red')
        self.shopping_list.grid(row=1, column=0, sticky="ENSW")

        self.columnconfigure(0, weight=1)
        

        #self.product_list = ProductList(self, shopping_list=self.shopping_list, bg='purple', text="Products", font=('Bold', 20), labelanchor='nw')
        self.product_list = LabelFrame(self, text="Popular Products", font=('Bold', 15), padx=10, pady=10)
        
        grid = ProductGrid(self.product_list, row=0, col=0, target=self.shopping_list, src_file_path="./resources/products.csv", x_max=8)
        grid.load_products(header=True)

        self.product_list.grid(row=2, column=0, sticky="ENSW")
        #self.product_list.load_products()
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, minsize=50)
        self.rowconfigure(2, weight=350)


class Application(Tk):

    def __configure(self):
        self.title("AOSS Application 1.2.0")
        self.minsize(700, 500)

        # GRID configuration
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, minsize=200, weight=1)
        self.columnconfigure(1, weight=1000)

    def switch_view(self, view: Literal['shopping', 'templates']):
        self.__cur_view.grid_forget()

        match view:
            

            case 'shopping':
                self.__cur_view = self.__shopping_view
            case 'templates':
                self.__cur_view = self.__templates_view

        self.__cur_view.grid(row=0, column=1, sticky="WSEN")


    def __init__(self, *args, **kw):
        super(Application, self).__init__(*args, **kw)

        self.__configure()


        #TOGGLE MENU configuration
        self.__toggle_menu = ToggleMenu(self, parent=self, bg='#7AC5CD')
        self.__toggle_menu.grid(row=0, column=0, sticky="WSEN", pady=(5, 0))
        
    
        # SHOPPING VIEW configuration
        self.__shopping_view = MainShoppingView(self)
        self.__shopping_view.grid(row=0, column=1, sticky="WSEN")

        # TEMPLATES VIEW configuration
        self.__templates_view = Frame(self)
        # self.__templates_view.grid(row=0, column=1, sticky="WSEN")
        # self.__templates_view.grid_forget()

        self.button = Button(self.__templates_view, text='SO FAR EMPTY!')
        self.button.grid(row=0, column=0)

        self.__cur_view = self.__shopping_view
        self.mainloop()

class ToggleMenu(Frame):

    def __on_shopping_click(self):
        self.__parent.switch_view(view='shopping')
    
    def __on_templates_click(self): 
        self.__parent.switch_view(view='templates')

    def __init__(self, *args, parent: Application, **kw):
        super(ToggleMenu, self).__init__(*args, **kw)
        
        self.__parent = parent
        #self.icon_image = PhotoImage(file='./icon_1.png').subsample(8, 8)

        self.__shopping = Button(self, font=('Bold', 20), command=self.__on_shopping_click, text='Shopping',  bd=0, bg='#98F5FF', fg='white', anchor='w')
        self.__shopping.grid(row=0, column=0, sticky='ew')

        self.__templates = Button(self, font=('Bold', 20), command=self.__on_templates_click, text='Templates', bd=0, bg='#98F5FF', fg='white', anchor='w')
        self.__templates.grid(row=1, column=0, sticky='ew', pady=1)


        self.columnconfigure(0, weight=1)
        #self.rowconfigure(1, weight=1)


from scraping import ProductScraper
from marketing import Market
import json

if __name__ == '__main__':

    CONFIG_FILE_PATH = "./.config.json"

    with open(file=CONFIG_FILE_PATH, mode='r') as config_file:
        data = json.load(config_file)
    
    MARKETS_PATH = data["resources"]["data"]["markets"]
    PRODUCTS_PATH = data["resources"]["data"]["products"]
    PRODUCT_HASHES = data['resources']["data"]["product_hashes"]

    market: Market = Market.get_market(ID=3, market_file=MARKETS_PATH, product_file=PRODUCTS_PATH, hash_file=PRODUCT_HASHES)

    assert(market is not None)

    scraper = ProductScraper(market=market, session_limit=6)
    scraper.scrape_all(register=True, _print=True)
    
    scraper.quit()
    market.register_products()

    #app = Application()
    #print("continuing")
    #app.mainloop()

    #app = Tk()
    #app.title("AOSS Application 1.2.0")
    #app.geometry("900x500")
    
    #app.minsize(700, 500)

    #toggle_menu = ToggleMenu(app, bg='#7AC5CD')
    
    #toggle_menu.grid(row=0, column=0, sticky="WSEN", pady=(5, 0))

    #product_view = MainShoppingView(app)
    #product_view.grid(row=0, column=1, sticky="WSEN")


    #toggle_menu.place(x=0, y=5)
    #app.rowconfigure(0, weight=1)

    #app.columnconfigure(0, minsize=toggle_menu.winfo_reqwidth(), weight=3)
    #app.columnconfigure(1, weight=8)

    


    #app.mainloop()