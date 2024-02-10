from typing import List

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font

import config_paths

from AOSS.structure.shopping import MarketHub, ProductCategory
from AOSS.components.marrec import MarketExplorer, Market
from AOSS.components.processing import ProductCategorizer


# --- ShoppingListItem - Class Declaration&Definition --- #

class ShoppingListDetails(LabelFrame):
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self,*args, name: str, category: str, ID: int, on_widget_click: callable = None, **kw):
        super(ShoppingListDetails, self).__init__(*args, **kw)

        #self.background = 
        #self.__parent = parent
        self.__name_label = Label(self, text=f"Name: {name}", font=('Arial', 11))
        self.__name_label.grid(row=0, column=0, sticky="NSW")
        self.__name_label.bind("<Button-1>", on_widget_click)

        

        self.__category_label = Label(self, text=f"Category: {category}", font=('Arial', 11))
        self.__category_label.grid(row=1, column=0, sticky="NSW")
        self.__category_label.bind("<Button-1>", on_widget_click)

        self.__ID_label = Label(self, text=f"{ID}", font=('Arial', 11))
        self.__ID_label.grid(row=2, column=0, sticky="NSEW")
        self.__ID_label.bind("<Button-1>", on_widget_click)

        if callable:
            self.__name_label.bind("<Button-1>", on_widget_click)
            self.__category_label.bind("<Button-1>", on_widget_click)
            self.__ID_label.bind("<Button-1>", on_widget_click)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)


class ShoppingListItem(Frame):
    
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self, *args, name: str, category: str, ID: int, on_widget_click: callable = None, **kw):
        super(ShoppingListItem, self).__init__(*args, **kw)

        self.item_details = ShoppingListDetails(self,  name=name, category=category, ID=ID, on_widget_click=self.on_item_clicked, bd=1)

        self.item_details.grid(row=0, column=0, sticky="NSEW", padx=2, pady=2)
        self.item_details.bind("<Button-1>", self.on_item_clicked)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.on_widget_click = on_widget_click

    def on_item_clicked(self, event):
        self.on_widget_click()
        self.item_details.configure(bd=3)


class ShoppingList(Frame):
    def __init__(self, *args, **kw):
        super(ShoppingList, self).__init__(*args, **kw)


        self.items: List[ShoppingListItem] = []
    
    def remove_click_texture(self, event = None):

        for item in self.items:
            item.configure(background='white')
            item.item_details.configure(bd=1)



# --- ShoppingList - Class Declaration&Definition --- #


class ShoppingListFrame(LabelFrame):
    def __init__(self, *args, **kw):
        super(ShoppingListFrame, self).__init__(*args, **kw)

        self.canvas = Canvas(self, bg='dimgrey', height=50)
        self.canvas.pack(side='top', fill='both', expand=True)

        self.scrollbar = Scrollbar(self, orient='horizontal', bg='dimgrey', command=self.canvas.xview)
        self.scrollbar.pack(side='top', fill='x', expand=False)

        self.scrollbar.config(command=self.canvas.xview)

        self.shopping_list = ShoppingList(self.canvas, bg='dimgrey')
        self.shopping_list.bind('<Configure>', self.configure_interior)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.__interior_ID =  self.canvas.create_window(0, 0, window=self.shopping_list, anchor='nw')

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        #self.__items: List[ShoppingListItem] = []

    def configure_interior(self, event):
        size = (self.shopping_list.winfo_reqwidth(), self.shopping_list.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))

        if self.shopping_list.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.shopping_list.winfo_reqwidth())



    def configure_canvas(self, event): 
        if self.shopping_list.winfo_reqheight() != self.canvas.winfo_height():
            self.canvas.itemconfigure(self.__interior_ID, height=self.canvas.winfo_height() - 4)
            #self.__interior.config(width=self.canvas.winfo_height())  # Update interior width

    def items(self):
        return self.shopping_list.items
    
        #return self.__items

    def insert_item(self, name: str, category: ProductCategory):
        item = ShoppingListItem(self.shopping_list, name=name, category=category.name, ID=len(self.shopping_list.items) + 1,
                                on_widget_click=self.shopping_list.remove_click_texture)
        
        item.pack(side="left", fill="y", expand=False, padx=2, pady=2)

        self.canvas.update_idletasks()
        size = (self.shopping_list.winfo_reqwidth(), self.shopping_list.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.scrollbar.update()
        
        self.shopping_list.items.append(item)
        item.bind("<Button-1>", self.shopping_list.remove_click_texture)



    def consume_entry(self):
        content = self.__entry.get()
        self.__entry.delete(0, END)

        return content

# class ProductCategory(Enum):
#     OVOCIE_ZELENINA = 1
#     PECIVO = 2
#     MASO_MRAZENE_VYROBKY = 3
#     UDENINY_NATIERKY_PASTETY = 4
#     MLIECNE_VYROBKY = 5
#     TRVANLIVE_POTRAVINY_VAJCIA = 6
#     SLADKOSTI = 7
#     SLANE_SNACKY_SEMIENKA = 8
#     NEALKOHOLICKE_NAPOJE = 9
#     ALKOHOL = 10
#     TEPLE_NAPOJE = 11
#     HOTOVE_INSTANTNE = 12
#     ZDRAVE_POTRAVINY = 13


class CategoryInfoView(Frame):
    def __init__(self, *args, **kw):
        super(CategoryInfoView, self).__init__(*args, **kw)
        #self.__categories_frame = categories_frame
        #self.__button = Button(self, text="More Info", font=("Bold", 12), command=self.__show_category_info).pack(side='top')

        self.__info_text = Text(self, height = 5, width = 52)
        self.__info_text.pack(side='top', expand=True, fill='both', padx=10, pady=10)
        #self.__info_text.grid(row=0, column=0, sticky="NSEW")
        self.__info_text.config(state="disabled")
    
    def notify(self, category_name: str):
        self.__info_text.config(state="normal")
        self.__info_text.delete(1.0, END)
        self.__info_text.insert(END, category_name)
        self.__info_text.config(state="disabled")

    # def __show_category_info(self):
    #     self.__categories_frame.

class NewProductView(LabelFrame):
    def __init__(self, *args, shopping_list: ShoppingListFrame, **kw):
        super(NewProductView, self).__init__(*args, **kw)

        self.__shopping_list = shopping_list

        self.__product_name_label = Label(self, text="Name: ", font=("Bold", 12), padx=5, bg='grey')
        self.__product_name_label.grid(row=0, column=0, sticky="E", pady=7)

        self.__entry = Entry(self, font=('Bold', 13))
        self.__entry.grid(row=0, column=1, sticky="WNES", pady=7)

        self.__button = Button(self, text="To Cart", font=("Arial", 12, "bold", "underline"), height=1, command=self.__on_button_clicked)
        self.__button.grid(row=0, column=2, sticky="EWNS", padx=3, pady=7)



        self.__info_text = Text(self, width = 15)
        self.__info_text.grid(row=1, column=2, sticky="NSEW", padx=10, pady=10)
        self.__info_text.config(state="disabled")


        self.__categories = CategoriesFrame(self, text="Categories", category_info_view=self, font=(20))
        self.__categories.grid(row=1, column=1, sticky="WNES", padx=10, pady=10)

        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        #self.columnconfigure(3, weight=1)

        # self.columnconfigure(1, weight=2, minsize=510)
        # self.columnconfigure(2, weight=1, minsize=240)
        # self.columnconfigure(3, weight=1)


        self.rowconfigure(0, weight=1, minsize=50)
        #self.rowconfigure(0, weight=1, minsize=60)
        self.rowconfigure(1, weight=20)

        self.__market_hub = MarketHub(src_file=config_paths.MARKET_HUB_FILE['path'])
        self.__market_hub.load_markets()

    
    def show_category_details(self, category_name: str, details: str):
        self.__info_text.config(state="normal")
        self.__info_text.delete(1.0, END)
        try:
            self.__info_text.insert(END, category_name + '\n' + details)
        except TypeError:
            pass
        
        self.__info_text.config(state="disabled")

    def consume_entry(self):
        content = self.__entry.get()
        self.__entry.delete(0, END)

        return content
    
    def __on_button_clicked(self):
        name = self.consume_entry()

        if name is None or name == "":
            messagebox.showwarning("Warning", "Name field cannot be empty!")
            return

        self.__shopping_list.insert_item(name=name, category=ProductCategory(value=self.__categories.get_option()) )
    

class CategoriesFrame(LabelFrame):
    TEXT_WIDTH = 20

    def __init__(self, *args, category_info_view: NewProductView, **kw):
        super(CategoriesFrame, self).__init__(*args, **kw)
        self.__category_info_view = category_info_view

        self.__variable = IntVar()
        self.__old_val = self.__variable.get()

        self.__variable.trace_add("write", callback=self.__notify)

        self.__unspecified = Radiobutton(self, text="Neurčená",  width=self.TEXT_WIDTH, variable=self.__variable, value=0, anchor='w')
        self.__unspecified.grid(row=0, column=0, sticky="W")


        self.__fruit_vegetables = Radiobutton(self, text="Ovocie a zelenina", width=self.TEXT_WIDTH, variable=self.__variable, value=1, anchor='w')
        self.__fruit_vegetables.grid(row=0, column=1, sticky="W")

        self.__baked_products = Radiobutton(self, text="Pečivo", width=self.TEXT_WIDTH, variable=self.__variable, value=2, anchor='w')
        self.__baked_products.grid(row=1, column=0, sticky="W")

        self.__meat_and_frost = Radiobutton(self, text="Mäso a mrazené potraviny", width=self.TEXT_WIDTH, variable=self.__variable, value=3, anchor='w')
        self.__meat_and_frost.grid(row=1, column=1, sticky="W")

        self.__smoked_paste = Radiobutton(self, text="Udeniny, natierky a pastety", width=self.TEXT_WIDTH, variable=self.__variable, value=4, anchor='w')
        self.__smoked_paste.grid(row=2, column=0, sticky="W")

        self.__dairies = Radiobutton(self, text="Mliečne výrobky", width=self.TEXT_WIDTH, variable=self.__variable, value=5, anchor='w')
        self.__dairies.grid(row=2, column=1, sticky="W")

        self.__durables_eggs = Radiobutton(self, text="Trvanlivé potraviny, vajcia", width=self.TEXT_WIDTH, variable=self.__variable, value=6, anchor='w')
        self.__durables_eggs.grid(row=3, column=0, sticky="W")

        self.__sweets = Radiobutton(self, text="Sladkosti", width=self.TEXT_WIDTH, variable=self.__variable, value=7, anchor='w')
        self.__sweets.grid(row=3, column=1, sticky="W")

        self.__snacks_seeds = Radiobutton(self, text="Slané, snacky a semienka", width=self.TEXT_WIDTH, variable=self.__variable, value=8, anchor='w')
        self.__snacks_seeds.grid(row=4, column=0, sticky="W")

        self.__non_alcoholic_drinks = Radiobutton(self, text="Nealkoholické nápoje", width=self.TEXT_WIDTH, variable=self.__variable, value=9, anchor='w')
        self.__non_alcoholic_drinks.grid(row=4, column=1, sticky="W")

        self.__alcohol = Radiobutton(self, text="Alkohol", width=self.TEXT_WIDTH, variable=self.__variable, value=10, anchor='w')
        self.__alcohol.grid(row=5, column=0, sticky="W")

        self.__hot_drinks = Radiobutton(self, text="Horúce nápoje", width=self.TEXT_WIDTH, variable=self.__variable, value=11, anchor='w')
        self.__hot_drinks.grid(row=5, column=1, sticky="W")

        self.__prepared_food = Radiobutton(self, text="Hotové či instatné jedlá", width=self.TEXT_WIDTH, variable=self.__variable, value=12, anchor='w')
        self.__prepared_food.grid(row=6, column=0, sticky="W")

        self.__healthy_products = Radiobutton(self, text="Zdravé potraviny", width=self.TEXT_WIDTH, variable=self.__variable, value=13, anchor='w')
        self.__healthy_products.grid(row=6, column=1, sticky="W")


    
    def get_option(self) -> int:
        return self.__variable.get()

    def __notify(self, *args):
        new_value = self.__variable.get()
        if new_value != self.__old_val: 

            category_name = ProductCategory(value=new_value).name
            self.__category_info_view.show_category_details(category_name=category_name, details=ProductCategorizer.category_details(category=category_name.lower()))
            self.__old_val = new_value


#class ShoppingListOptionPanel(Frame):

class ShoppingListMenu(Frame):
    def __init__(self, *args, shopping_list: ShoppingListFrame, **kw):
        super(ShoppingListMenu, self).__init__(*args, **kw)

        self.search_market_button = Button(self, text="search", font=(font.BOLD, 13), width=20, height=1, command=self.search_market_pressed)
        self.search_market_button.pack(side='right', fill='y', padx=3, pady=3)
        
        #self.search_market_button.grid(row=0, column=0, sticky="ENS", padx=5, pady=3)

        self.delete_product_button = Button(self, text="delete", font=(font.BOLD, 13), width=20, height=1, command=self.delete_product_pressed)
        self.delete_product_button.pack(side='right', fill='y', padx=3, pady=3)
        #self.delete_product_button.grid(row=0, column=1, sticky="ENS", padx=5, pady=3)

        self.shopping_list = shopping_list
       # self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=1)

    
    def search_market_pressed(self):


        items = self.shopping_list.items()

        if not items:
            messagebox.showwarning("Warning", "Product list contains no items!")
            pass
    
    def delete_product_pressed(self):
        print("PRESSED!")


class ShoppingListView(Frame):
    def __init__(self, *args, **kw):
        super(ShoppingListView, self).__init__(*args, **kw)

        
        self.__icon_image = PhotoImage(file=config_paths.SHOPPING_CART_ICON).subsample(17, 17)
        self.__label = Label(self, text="Shopping List",
                            image=self.__icon_image, compound='right', font=('Arial', 20, 'bold'), height=45, fg='black', bg='dimgrey')

        self.__label.grid(row=0, column=0, sticky="WS")

        self.__list = ShoppingListFrame(self, bg='black')
        self.__list.grid(row=1, column=0, sticky="WNES")

    

        self.menu = ShoppingListMenu(self, shopping_list=self.__list, bg='dimgrey')
        self.menu.grid(row=2, column=0, sticky="NSEW")

        # self.__search_market_button = Button(self, text="search", font=(font.BOLD, 13), width=20, height=1, command=self.search_market_pressed)
        # self.__search_market_button.grid(row=2, column=0, sticky="ENS", padx=5, pady=3)

        # self.delete_product_button = Button(self, text="delete", font=(font.BOLD, 13), width=20, height=1, command=self.delete_product_pressed)
        # self.delete_product_button.grid(row=2, column=1, stic)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        
        self.columnconfigure(0, weight=1)
    
    


    def shopping_list(self):
        return self.__list


class ExplorationTable(Frame):
     def __init__(self, *args, markets: tuple[Market], **kw):
        super(ExplorationTable, self).__init__(*args, **kw)

        self.market_name_col = Label(self, text="Name", font=("Arial",  12, "bold"))
        self.market_name_col.grid(row=0, column=0, sticky="NSEW", padx=2, pady=2)

        self.total_price_col = Label(self, text="Total Price", font=("Arial",  12, "bold"))
        self.total_price_col.grid(row=0, column=1, sticky="NSEW", padx=2, pady=2)
        
        self.succession_rate = Label(self, text="Succession Rate", font=("Arial",  12, "bold"))
        self.succession_rate.grid(row=0, column=2, sticky="NSEW", padx=2, pady=2)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


        for index, market in enumerate(markets):
            cell = Label(self, text=market.name().lower(), font=('Arial', 12))
            cell.grid(row=index + 1, column=0, sticky="NSEW", padx=1, pady=1)

            self.rowconfigure(index + 1, weight=1)
                


class MarketExplorerView(LabelFrame):
    def __init__(self, *args, **kw):
        super(MarketExplorerView, self).__init__(*args, **kw)
        
        self.market_hub = MarketHub(src_file=config_paths.MARKET_HUB_FILE['path'])
        self.market_hub.load_markets()
        self.market_hub.load_products()

        self.explorer = MarketExplorer(market_hub=self.market_hub)
        
        self.table = ExplorationTable(self, markets=self.market_hub.markets(), bg='black')
        self.table.grid(row=0, column=0, sticky="NSEW", padx=3, pady=3)

        self.padding = Frame(self)
        self.padding.grid(row=1, column=0, sticky="NSEW")
    
    def explore_markets(self, product_list: List[tuple[str, ProductCategory]]):

        results = self.explorer.explore(product_list=product_list)





        # markets = ('Billa', 'Tesco', 'Coop Jednota')
        # var = Variable(value=markets)

        # self.market_list = Listbox(self, listvariable=var, selectmode=EXTENDED)


        # #self.label = Label(self, text="NIECO!")
        # self.market_list.grid(row=0, column=0, sticky="NSEW")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=500)
        self.columnconfigure(0, weight=1)

    





class SpecificationExplorationView(Frame):
     def __init__(self, *args, shopping_list_frame: ShoppingListFrame, **kw):
        super(SpecificationExplorationView, self).__init__(*args, **kw)

        #self.haha = MarketExplorerView(self, text="Market Explorer", font=("Bold", 20))
        #self.haha.grid(row=0, column=0, sticky="NSEW", padx=5)
        self.__product_search_view = NewProductView(self, shopping_list=shopping_list_frame.shopping_list(), bg='grey', text="New Product", font=('Arial', 20, 'bold'))
        self.__product_search_view.grid(row=0, column=0, sticky="NWS")

        self.__market_explorer_view = MarketExplorerView(self, text="Market Explorer", font=('Arial', 20, 'bold'), bg='grey')
        self.__market_explorer_view.grid(row=0, column=1, padx=5, sticky="NSEW")

        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=50, minsize=100)

        self.rowconfigure(0, weight=1)





# --- MainShoppingView - Class Declaration&Definition --- #

class MainShoppingView(Frame):
    
    # def __on_new_item_button_click(self):
    #     self.__shopping_list.insert_item()

    def __init__(self, *args, product_file: str, **kw):
        super(MainShoppingView, self).__init__(*args, **kw)

        self.__shopping_list_frame = ShoppingListView(self)

        self.__shopping_list_frame.grid(row=0, column=0, sticky="NSEW")


        self.specification_exploration_view = SpecificationExplorationView(self, shopping_list_frame=self.__shopping_list_frame, bg='grey')
        self.specification_exploration_view.grid(row=1, column=0, sticky="NSEW")

        self.padding_view = Frame(self)
        self.padding_view.grid(row=2, column=0, sticky="NSEW")

        # self.__product_search_view = NewProductView(self, shopping_list=self.__shopping_list_frame.shopping_list(), text="New Product", font=("Bold", 20))
        # self.__product_search_view.grid(row=1, column=0, sticky="NEWS", pady=5)

        # self.__market_explorer_view = MarketExplorerView(self, text="Market Explorer", font=("Bold", 20))
        # self.__market_explorer_view.grid(row=1, column=1, sticky="NSEW")c

        self.rowconfigure(0, weight=1, minsize=250)
        self.rowconfigure(1, weight=1, minsize=100)
        self.rowconfigure(2, weight=200)


        self.columnconfigure(0, weight=1)
