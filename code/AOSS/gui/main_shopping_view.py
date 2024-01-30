from typing import List

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import config_paths
from AOSS.components.product_search import ProductMatcher
import AOSS.structure.shopping as shp

# --- ShoppingListItem - Class Declaration&Definition --- #

class ShoppingListItem(Frame):
    
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self, *args, product: shp.Product, ID: int,  **kw):
        super(ShoppingListItem, self).__init__(*args, **kw)



        self.__name_label = Label(self, text=f"Name: {product.name}")
        self.__name_label.grid(row=0, column=0, sticky="NSW")

        self.__category_label = Label(self, text=f"Category: {product.category}")
        self.__category_label.grid(row=1, column=0, sticky="NSW")

        self.__ID_label = Label(self, text=f"{ID}")
        self.__ID_label.grid(row=2, column=0, sticky="NSEW")


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
    
    
# --- ShoppingList - Class Declaration&Definition --- #


class ShoppingList(LabelFrame):
    def __init__(self, *args, **kw):
        super(ShoppingList, self).__init__(*args, **kw)

        self.canvas = Canvas(self, bg='blue', height=50)
        self.canvas.pack(side='top', fill='both', expand=True)

        self.scrollbar = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.pack(side='top', fill='x', expand=False)

        self.scrollbar.config(command=self.canvas.xview)

        self.__interior = Frame(self.canvas, bg='red')
        self.__interior.bind('<Configure>', self.configure_interior)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.__interior_ID =  self.canvas.create_window(0, 0, window=self.__interior, anchor='nw')

        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.__items: List[ShoppingListItem] = []

    def configure_interior(self, event):
        size = (self.__interior.winfo_reqwidth(), self.__interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))

        if self.__interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.__interior.winfo_reqwidth())

    def configure_canvas(self, event): 
        if self.__interior.winfo_reqheight() != self.canvas.winfo_height():
            self.canvas.itemconfigure(self.__interior_ID, height=self.canvas.winfo_height() - 4)
            #self.__interior.config(width=self.canvas.winfo_height())  # Update interior width

    def insert_item(self, product: shp.Product):
        item = ShoppingListItem(self.__interior, product=product, ID=len(self.__items) + 1)  
        item.pack(side="left", fill="y", expand=False, padx=5)

        self.canvas.update_idletasks()
        size = (self.__interior.winfo_reqwidth(), self.__interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.scrollbar.update()

        self.__items.append(item)


# class ProductMatchView(Frame):
#     def __init__(self, *args, **kw):
#         super(ProductMatchView, self).__init__(*args, **kw)

#         self.__entry = Entry(self, width=33)
#         self.__entry.grid(row=0, column=0, sticky="NEWS")

#         # self.menu = Menu(self, tearoff=1)
#         # e

#         # self.combo_box = ttk.Combobox(self, width=30)
#         # self.combo_box.grid(row=1, column=0, sticky="NSW")

#         self.rowconfigure(0, weight=1)
#         self.rowconfigure(1, weight=1)

#         self.columnconfigure(0, weight=1)

    # def read_entry(self):
    
    #     return self.__entry.get()

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

class AddProductToCartView(LabelFrame):
    def __init__(self, *args, shopping_list: ShoppingList, **kw):
        super(AddProductToCartView, self).__init__(*args, **kw)

        self.__shopping_list = shopping_list

        self.__product_name_label = Label(self, text="Name: ", font=("Bold", 8))
        self.__product_name_label.grid(row=0, column=0, sticky="NSE", pady=10)

        self.__entry = Entry(self, width=10)
        self.__entry.grid(row=0, column=1, sticky="WNES", pady=10)

        self.__button = Button(self, width=25, text="To Cart", font=("Bold", 10), command=self.__on_button_clicked)
        self.__button.grid(row=0, column=2, sticky="NS", padx=5, pady=10)

        # self.__category_label = Label(self, text="Category: ", font=("Bold", 8))
        # self.__category_label.grid(row=1, column=0, sticky="NES")

        self.__info_text = Text(self, height = 5, width = 52)
        self.__info_text.grid(row=1, column=2, sticky="NSEW", padx=10, pady=10)
        #self.__info_text.grid(row=0, column=0, sticky="NSEW")
        self.__info_text.config(state="disabled")
        #self.__category_info.grid(row=1, column=2, sticky="NSEW")
        #self.__category_info.config(state="disabled")

        self.__categories = CategoriesFrame(self, text="Categories", category_info_view=self, font=(20))
        self.__categories.grid(row=1, column=1, sticky="WNES", pady=10)

        
        

        self.columnconfigure(0, weight=1, minsize=50)
        self.columnconfigure(1, weight=30, minsize=600)
        self.columnconfigure(2, weight=1, minsize=240)
        self.columnconfigure(3, weight=1)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.__product_matcher = ProductMatcher(markets=shp.markets(market_file=config_paths.MARKET_FILE['path'], header=config_paths.MARKET_FILE['header']))
    
    def show_category_details(self, category_name: str, details: str):
        self.__info_text.config(state="normal")
        self.__info_text.delete(1.0, END)
        self.__info_text.insert(END, category_name + '\n' + details)
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

        self.__shopping_list.insert_item(product=shp.Product(name=name, category=shp.ProductCategory(value=self.__categories.get_option()).name ))
    

class CategoriesFrame(LabelFrame):
    TEXT_WIDTH = 20

    def __init__(self, *args, category_info_view: AddProductToCartView, **kw):
        super(CategoriesFrame, self).__init__(*args, **kw)
        self.__category_info_view = category_info_view

        self.__variable = IntVar()
        self.__old_val = self.__variable.get()

        self.__variable.trace_add("write", callback=self.__notify)

        self.__fruit_vegetables = Radiobutton(self, text="Ovocie a zelenina", width=self.TEXT_WIDTH, variable=self.__variable, value=1, anchor='w')
        self.__fruit_vegetables.grid(row=0, column=0, sticky="W")

        self.__baked_products = Radiobutton(self, text="Pečivo", width=self.TEXT_WIDTH, variable=self.__variable, value=2, anchor='w')
        self.__baked_products.grid(row=0, column=1, sticky="W")

        self.__meat_and_frost = Radiobutton(self, text="Mäso a mrazené potraviny", width=self.TEXT_WIDTH, variable=self.__variable, value=3, anchor='w')
        self.__meat_and_frost.grid(row=0, column=2, sticky="W")

        self.__smoked_paste = Radiobutton(self, text="Udeniny, natierky a pastety", width=self.TEXT_WIDTH, variable=self.__variable, value=4, anchor='w')
        self.__smoked_paste.grid(row=1, column=0, sticky="W")

        self.__dairies = Radiobutton(self, text="Mliečne výrobky", width=self.TEXT_WIDTH, variable=self.__variable, value=5, anchor='w')
        self.__dairies.grid(row=1, column=1, sticky="W")

        self.__durables_eggs = Radiobutton(self, text="Trvanlivé potraviny, vajcia", width=self.TEXT_WIDTH, variable=self.__variable, value=6, anchor='w')
        self.__durables_eggs.grid(row=1, column=2, sticky="W")

        self.__sweets = Radiobutton(self, text="Sladkosti", width=self.TEXT_WIDTH, variable=self.__variable, value=7, anchor='w')
        self.__sweets.grid(row=2, column=0, sticky="W")

        self.__snacks_seeds = Radiobutton(self, text="Slané, snacky a semienka", width=self.TEXT_WIDTH, variable=self.__variable, value=8, anchor='w')
        self.__snacks_seeds.grid(row=2, column=1, sticky="W")

        self.__non_alcoholic_drinks = Radiobutton(self, text="Nealkoholické nápoje", width=self.TEXT_WIDTH, variable=self.__variable, value=9, anchor='w')
        self.__non_alcoholic_drinks.grid(row=2, column=2, sticky="W")

        self.__alcohol = Radiobutton(self, text="Alkohol", width=self.TEXT_WIDTH, variable=self.__variable, value=10, anchor='w')
        self.__alcohol.grid(row=3, column=0, sticky="W")

        self.__hot_drinks = Radiobutton(self, text="Horúce nápoje", width=self.TEXT_WIDTH, variable=self.__variable, value=11, anchor='w')
        self.__hot_drinks.grid(row=3, column=1, sticky="W")

        self.__prepared_food = Radiobutton(self, text="Hotové či instatné jedlá", width=self.TEXT_WIDTH, variable=self.__variable, value=12, anchor='w')
        self.__prepared_food.grid(row=3, column=2, sticky="W")

        self.__healthy_products = Radiobutton(self, text="Zdravé potraviny", width=self.TEXT_WIDTH, variable=self.__variable, value=13, anchor='w')
        self.__healthy_products.grid(row=4, column=0, sticky="W")


       # self.columnconfigure(0, weight=1)
    
    def get_option(self) -> int:
        return self.__variable.get()

    def __notify(self, *args):
        new_value = self.__variable.get()
        if new_value != self.__old_val: 

            category_name = shp.ProductCategory(value=new_value).name
            self.__category_info_view.show_category_details(category_name=category_name, details=shp.category_details(category=category_name.lower()))
            self.__old_val = new_value



        


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
        #self.__shopping_list.insert_item()
        #elf.__shopping_list.insert_item()
        

        self.__product_search_view = AddProductToCartView(self, shopping_list=self.__shopping_list, text="New Product", font=("Bold", 20))
        self.__product_search_view.grid(row=2, column=0, sticky="NEWS", pady=5)

        # self.__new_item_entry = Entry(self, width=25)

        # #self.__new_item_button = Button(self, text="New", font=('Bold', 13), width=25, command=self.__on_new_item_button_click)
        # self.__new_item_entry.grid(row=2, column=0, sticky="NS")
        #self.__combo_box = ttk.Combobox(self, width=25, height=10)
        #self.__combo_box.grid(row=3, column=0, sticky="N")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1, minsize=100)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=150)
        #self.rowconfigure(3, weight=10)

        self.columnconfigure(0, weight=1, minsize=890)