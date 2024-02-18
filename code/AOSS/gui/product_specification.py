from tkinter import *
from tkinter import messagebox

from AOSS.structure.shopping import ProductCategory
from AOSS.components.processing import ProductCategorizer

from AOSS.gui.shopping_list import ShoppingListFrame
from AOSS.gui.market_explorer import MarketExplorerFrame

from config_paths import *

class ProductSpecificationMenu(LabelFrame):
    def __init__(self, *args, root, shopping_list_frame: ShoppingListFrame,
                   market_explorer_frame: MarketExplorerFrame, **kw):
        super(ProductSpecificationMenu, self).__init__(*args, **kw)

        self.root = root
        self.shopping_list_f = shopping_list_frame
        self.market_explorer_f = market_explorer_frame

        # ------ Frame Configuration ------ #
        
        self.rowconfigure(0, weight=1, minsize=110)
        self.rowconfigure(1, weight=3, minsize=50)
        self.rowconfigure(2, weight=2, minsize=55)
        self.columnconfigure(0, weight=1)

        # ------ MAIN_DETAILS_MENU - CONFIGURATION ------ #

        self.main_details_menu = Frame(self, bg='dimgrey')
        self.main_details_menu.grid(row=0, column=0, sticky="NEW", pady=5)

        # frame configuration

        self.main_details_menu.grid(row=0, column=0, sticky="NEW")
        self.main_details_menu.rowconfigure(0, weight=1, minsize=50)
        self.main_details_menu.rowconfigure(1, weight=1, minsize=50)
        self.main_details_menu.columnconfigure(0, weight=1)
        self.main_details_menu.columnconfigure(1, weight=200)
    

        # name configuration

        self.name_frame = Frame(self.main_details_menu, bg='dimgrey')
        self.name_frame.grid(row=0, column=0, sticky="NSEW", pady=8, padx=3)
        self.name_frame .rowconfigure(0, weight=1)
        self.name_frame .columnconfigure(0, weight=1)

        self.name_frame_label = Label(self.name_frame, text="Enter Name:", bg='grey', font=("Arial", 12))
        self.name_frame_label.grid(row=0, column=0, sticky="E")

        self.name_frame_entry = Entry(self.main_details_menu, font=("Arial", 13))
        self.name_frame_entry.grid(row=0, column=1, sticky="NSEW", pady=3, padx=8)

        # amount configuration

        self.amount_frame = Frame(self.main_details_menu, bg='dimgrey')
        self.amount_frame.grid(row=1, column=0, sticky="NSEW", pady=8, padx=3)
        self.amount_frame.rowconfigure(0, weight=1)
        self.amount_frame.columnconfigure(0, weight=1)

        self.amount_frame_label = Label(self.amount_frame, text="Enter Amount:", bg='grey', font=("Arial", 12))
        self.amount_frame_label.grid(row=0, column=0, sticky="E")

        self.amount_frame_entry = Entry(self.main_details_menu, font=("Arial", 13))
        self.amount_frame_entry.grid(row=1, column=1, sticky="NSEW", pady=3, padx=8)




        # ------ MAIN_DETAILS_MENU - CONFIGURATION ------ #

        self.categories_menu = CategoriesMenu(self, bg='dimgrey')
        self.categories_menu.grid(row=1, column=0, sticky="NEW", pady=5, padx=5)

        # ------- BUTTON_PANEL - CONFIGURATION ------ #

        self.button_panel = ButtonPanel(self, parent_frame=self)
        self.button_panel.grid(row=2, column=0, sticky="NEW", pady=5, padx=5)


    
    def show_error(self):
        # Create a Toplevel window
        error_window = Toplevel(self.root)
        error_window.title("Error")
        
        # Create a Message widget with the error message
        error_message = Message(error_window, text="Product Specification\nName field cannot be empty!", padx=10, pady=10)
        error_message.pack()

        # Add a button to close the error window
        btn_ok = Button(error_window, text="OK", command=error_window.destroy)
        btn_ok.pack()

    def insert_item(self):


        name = self.name_frame_entry.get()
        
        

        if name is None or name == "":
           # self.show_error()

            #message = messagebox.Message(self)
            messagebox.showerror("Product Specification", "Name field cannot be empty!")
            return

        

        category = self.categories_menu.buttons_pane.get_option()

        try:
            amount = int(self.amount_frame_entry.get())

            if amount < 1:
                raise ValueError("Product amount must be positive integer!")
            elif amount > self.shopping_list_f.product_list.ITEM_LIMIT:
                raise ValueError(f"Product amount above allowed limit: {self.shopping_list_f.product_list.ITEM_LIMIT}")
            

            self.name_frame_entry.delete(0, END)
            self.amount_frame_entry.delete(0, END)

            self.shopping_list_f.insert_item(name=name, category=category, amount=amount)
            self.market_explorer_f.search_button.config(state='normal')
            
        except ValueError as error:
            messagebox.showerror("Product Specification", error)
            return
        
        

    def clear_all_data(self):
        self.name_frame_entry.delete(0, END)
        self.amount_frame_entry.delete(0, END)



class CategoriesMenu(Frame):
    """
    
    """

    def __init__(self, *args, **kw):
        super(CategoriesMenu, self).__init__(*args, **kw)

        # --- Frame Configuration --- #

        self.rowconfigure(0, weight=2, minsize=240)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # --- ButtonsPane Configuration --- #

        self.buttons_pane = CategoryButtonsPane(self, parent_frame=self, bg='dimgrey', text="Categories", font=("Arial", 15, 'bold'))
        self.buttons_pane.grid(row=0, column=0, sticky="NSEW", padx=5, pady=3)

        # --- DetailsPanel Configuration --- #

        self.details_panel = Text(self)
        self.details_panel.grid(row=1, column=0, sticky="NEW", padx=5, pady=3)



    def show_details(self, category: str, text: str):
        if text is not None and text:
            self.details_panel.delete("1.0", END)  # Delete existing content
            self.details_panel.insert(END, category + '\n')
            self.details_panel.insert(END, text)
            





class CategoryButtonsPane(LabelFrame):
    TEXT_WIDTH = 23
    FONT = ('Arial', 12)

    def __init__(self, *args, parent_frame: CategoriesMenu, **kw):
        super(CategoryButtonsPane, self).__init__(*args, **kw)

        self.parent = parent_frame

       # self.__category_info_view = category_info_view

        self.__variable = IntVar()
        self.__old_val = self.__variable.get()

        self.__variable.trace_add("write", callback=self.__notify)

        self.__unspecified = Radiobutton(self, bg='dimgrey', text="0 - Neurčená", font=self.FONT,  width=self.TEXT_WIDTH, variable=self.__variable, value=0, anchor='w',
                                         activebackground='grey')#highlightbackground='grey', highlightcolor='grey', highlightthickness='grey')
        
        self.__unspecified.config(highlightbackground='grey', highlightcolor='grey')
        self.__unspecified.grid(row=0, column=0, sticky="W")



        self.__fruit_vegetables = Radiobutton(self, activebackground='grey', bg='dimgrey', text="1 - Ovocie a zelenina", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=1, anchor='w')
        self.__fruit_vegetables.grid(row=0, column=1, sticky="W")

        self.__baked_products = Radiobutton(self, bg='dimgrey', activebackground='grey', text="2 - Pečivo", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=2, anchor='w')
        self.__baked_products.grid(row=1, column=0, sticky="W")

        self.__meat_and_frost = Radiobutton(self, bg='dimgrey', activebackground='grey', text="3 - Mäso a mrazené potraviny", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=3, anchor='w')
        self.__meat_and_frost.grid(row=1, column=1, sticky="W")

        self.__smoked_paste = Radiobutton(self, bg='dimgrey',  activebackground='grey', text="4 - Udeniny, natierky a pastety", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=4, anchor='w')
        self.__smoked_paste.grid(row=2, column=0, sticky="W")

        self.__dairies = Radiobutton(self, bg='dimgrey', activebackground='grey', text="5 - Mliečne výrobky", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=5, anchor='w')
        self.__dairies.grid(row=2, column=1, sticky="W")

        self.__durables_eggs = Radiobutton(self, bg='dimgrey', activebackground='grey', text="6 - Trvanlivé potraviny, vajcia", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=6, anchor='w')
        self.__durables_eggs.grid(row=3, column=0, sticky="W")

        self.__sweets = Radiobutton(self, bg='dimgrey', activebackground='grey', text="7 - Sladkosti", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=7, anchor='w')
        self.__sweets.grid(row=3, column=1, sticky="W")

        self.__snacks_seeds = Radiobutton(self, bg='dimgrey',  activebackground='grey', text="8 - Slané, snacky a semienka", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=8, anchor='w')
        self.__snacks_seeds.grid(row=4, column=0, sticky="W")

        self.__non_alcoholic_drinks = Radiobutton(self, bg='dimgrey', activebackground='grey', text="9 - Nealkoholické nápoje", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=9, anchor='w')
        self.__non_alcoholic_drinks.grid(row=4, column=1, sticky="W")

        self.__alcohol = Radiobutton(self, bg='dimgrey', text="10 - Alkohol", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=10, anchor='w')
        self.__alcohol.grid(row=5, column=0, sticky="W")

        self.__hot_drinks = Radiobutton(self, bg='dimgrey', text="11 - Horúce nápoje", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=11, anchor='w')
        self.__hot_drinks.grid(row=5, column=1, sticky="W")

        self.__prepared_food = Radiobutton(self, bg='dimgrey', text="12 - Hotové či instatné jedlá", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=12, anchor='w')
        self.__prepared_food.grid(row=6, column=0, sticky="W")

        self.__healthy_products = Radiobutton(self, bg='dimgrey', text="13 - Zdravé potraviny", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=13, anchor='w')
        self.__healthy_products.grid(row=6, column=1, sticky="W")        


    
    def get_option(self) -> int:
        return self.__variable.get()

    def __notify(self, *args):

        new_value = self.__variable.get()

        if new_value != self.__old_val: 

            category_name = ProductCategory(value=new_value).name
            
            self.parent.show_details(text=ProductCategorizer.category_details(category=category_name.lower()),
                                     category=category_name)

           # self.__category_info_view.show_category_details(category_name=category_name, details=ProductCategorizer.category_details(category=category_name.lower()))
            self.__old_val = new_value



class ButtonPanel(Frame):
    def __init__(self, *args, parent_frame: ProductSpecificationMenu, **kw):
        super(ButtonPanel, self).__init__(*args, **kw)

        self.parent = parent_frame
        
        self.rowconfigure(0, weight=1, minsize=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.trash_bin_icon = PhotoImage(file=TRASH_BIN_ICON).subsample(18, 18)

        self.clear_button = Button(self, text='   clear', font=('Arial', 13), command=self.parent.clear_all_data, image=self.trash_bin_icon,
                                   compound='left')
        self.clear_button.grid(row=0, column=0, sticky="NSEW")

        self.cart_icon = PhotoImage(file=SHOPPING_CART_ICON_2).subsample(17, 17)

        self.to_cart_button = Button(self, text="   to List", font=('Arial', 13) ,
                                     command=self.parent.insert_item, image=self.cart_icon, compound='left')
        
        self.to_cart_button.grid(row=0, column=1, sticky="SNEW")

        
        



