from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import csv
from typing import List, Dict
import threading
import time
from datetime import datetime

from AOSS.structure.shopping import ProductCategory
from AOSS.components.categorization import ProductCategorizer

from AOSS.gui.shopping_list import ShoppingListFrame
from AOSS.gui.market_explorer import MarketExplorerFrame
from AOSS.gui.utils import AmountEntryFrame
from AOSS.gui.category_search_mode_panel import CategorySearchModePanel


from config_paths import *

BACKGROUND = 'lightblue'

class SearchedProductWindow(Toplevel):

    WIDTH = 38
    FONT = ("Arial", 13, 'italic')

    def __init__(self, *args, row_limit, min_char_limit = 10, max_char_limit, **kw):
        super(SearchedProductWindow, self).__init__(*args, **kw)

        self.row_limit = row_limit
        self.min_char_limit = min_char_limit
        self.max_char_limit = max_char_limit

        self.overrideredirect(True)
        self.bind("<Destroy>", self.save_products)


        self.listbox = Listbox(self, width=self.WIDTH, font=self.FONT)
        self.listbox.bind("<Motion>", self.on_motion)
        self.listbox.bind("<Leave>", self.on_leave)
        self.listbox.pack(side='left')

        self.close_window_button = Button(self, text='-', padx=2, pady=0, height=1)
        self.close_window_button.pack(side='top')

        self.products: Dict[str, List[int, str, str]] = {}
        self.next_ID = None

    def on_motion(self, event):
        index = self.listbox.nearest(event.y)
        self.listbox.selection_clear(0, END)  # Clear previous selection
        self.listbox.selection_set(index)  # Set new selection
        self.listbox.activate(index)  # Set the item as active

    def on_leave(self, event):
        self.listbox.selection_clear(0, END)  # Clear selection


    def update_listbox_size(self, char_count: int = None):
        # Get the number of items in the listbox
        num_items = self.listbox.size()

        # Set the height of the listbox based on the number of items
        self.listbox.config(height=num_items if num_items < self.row_limit else self.row_limit)

        # if char_count is not None and char_count > self.listbox.winfo_width():

        #     # if char_count > self.max_char_limit:
        #     #     char_count = self.max_char_limit
            
        #     self.listbox.config(width=self.max_char_limit if char_count > self.max_char_limit else char_count)

    
    def insert_product(self, content: str):
        """
            Inserts new searched product and its metadata to the dictionary.

            If the content is already present in the dictionary, searched_at attribute is updated.
        """

        if content in self.products:
            self.products[content][2] = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        else:
            self.products[content] = [self.next_ID, content, datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')]
            self.next_ID += 1
            self.update_listbox_size(char_count=len(content))



    def show_matches(self, content: str):
       
        self.listbox.delete(0, END)

        # Filter and display matching recommendations
        matching_results = [element for element in self.products.values() if content in element[1].lower()]
        for result in matching_results:
            self.listbox.insert(END, result[1])
        
        self.update_listbox_size(char_count=None)

        
    def load_products(self):
        """
            Loads the history of previosly searched products into the dictionary.
            Searched text is used as a key which maps a tuple containing metadata about
            the search.
        """

        with open(file=SEARCHED_PRODUCTS_FILE['path'], mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
        
            if SEARCHED_PRODUCTS_FILE['header']:
                try:
                    next(reader)
                except StopIteration:
                    self.next_ID = 1
                    return


            for row in reader:
                cur_ID = int(row[SEARCHED_PRODUCTS_FILE['cols']['ID']])

                if self.next_ID is None or self.next_ID < cur_ID:
                    self.next_ID = cur_ID

                self.products[row[SEARCHED_PRODUCTS_FILE['cols']['content']]] = [row[SEARCHED_PRODUCTS_FILE['cols']['ID']],
                                                                                row[SEARCHED_PRODUCTS_FILE['cols']['content']],
                                                                                row[SEARCHED_PRODUCTS_FILE['cols']['searched_at']]]
                


        self.next_ID += 1
                
        
    def save_products(self, event = None):
        """
            Saves the object's current dictionary data back to the source file.
        """

        with open(file=SEARCHED_PRODUCTS_FILE['path'], mode='w', encoding='utf-8', newline='') as file:
            
            writer = csv.writer(file)
            writer.writerow(('ID', 'content', 'searched_at'))

            for element in self.products.values():
                writer.writerow(element)
        
            #writer.writerows(self.products)

class ProductSpecificationMenu(LabelFrame):

    BACKGROUND = 'lightblue'


    def __init__(self, *args, root: Tk, shopping_list_frame: ShoppingListFrame,
                   market_explorer_frame: MarketExplorerFrame, **kw):
        super(ProductSpecificationMenu, self).__init__(*args, **kw)
        

        #self.config(background=BACKGROUND)

        self.root = root
        self.root.bind("<Configure>", self.on_root_window_moved)
        self.shopping_list_f = shopping_list_frame
        self.market_explorer_f = market_explorer_frame

        # ------ Frame Configuration ------ #
        
        self.rowconfigure(0, weight=1, minsize=110)
        self.rowconfigure(1, weight=3, minsize=50)
        self.rowconfigure(2, weight=5, minsize=55)
        self.columnconfigure(0, weight=1)

        # ------ MAIN_DETAILS_MENU - CONFIGURATION ------ #

        self.main_details_menu = Frame(self, bg=BACKGROUND)
        self.main_details_menu.grid(row=0, column=0, sticky="NEW", pady=(15, 5))

        # frame configuration

        self.main_details_menu.grid(row=0, column=0, sticky="NEW")
        self.main_details_menu.rowconfigure(0, weight=1)
        self.main_details_menu.rowconfigure(1, weight=1)
        self.main_details_menu.columnconfigure(0, weight=1)

        # self.main_details_menu.rowconfigure(0, weight=1, minsize=50)
        # self.main_details_menu.rowconfigure(1, weight=1, minsize=50)
        # self.main_details_menu.columnconfigure(0, weight=1)
        # self.main_details_menu.columnconfigure(1, weight=100)
    

        # name configuration

        self.upper_wrapper_frame = Frame(self.main_details_menu, background=BACKGROUND)
        self.upper_wrapper_frame.grid(row=0, column=0, sticky="NSEW")
        self.upper_wrapper_frame.rowconfigure(0, weight=1, minsize=50)
        self.upper_wrapper_frame.columnconfigure(0, weight=1)
        self.upper_wrapper_frame.columnconfigure(1, weight=100)

        self.name_frame = Frame(self.upper_wrapper_frame, bg=BACKGROUND)
        self.name_frame.grid(row=0, column=0, sticky="NSEW", pady=8, padx=(3, 17))
        self.name_frame.rowconfigure(0, weight=1)
        self.name_frame.columnconfigure(0, weight=1)

        self.name_frame_label = Label(self.name_frame, text="Enter Name:", bg=BACKGROUND, font=("Arial", 12))
        
        
        self.name_frame_label.grid(row=0, column=0, sticky="E")

        s = ttk.Style()
        s.configure('Rounded.TEntry', borderwidth=5, relief="flat", foreground="black", background="white")

        self.name_frame_entry = ttk.Entry(self.upper_wrapper_frame, style='Rounded.TEntry', font=("Arial", 13))
        self.name_frame_entry.grid(row=0, column=1, sticky="NSEW", pady=3, padx=8)
        self.name_frame_entry.bind("<KeyRelease>", self.show_product_name_matches)
        self.name_frame_entry.bind("<FocusOut>", self.destroy_product_name_matches)
        # amount configuration
        
        self.lower_wrapper_frame = Frame(self.main_details_menu, background=BACKGROUND)
        self.lower_wrapper_frame.grid(row=1, column=0, sticky="NSEW")
        self.lower_wrapper_frame.rowconfigure(0, weight=1, minsize=50)
        self.lower_wrapper_frame.columnconfigure(0, weight=1)
        self.lower_wrapper_frame.columnconfigure(1, weight=1, minsize=100)
        self.lower_wrapper_frame.columnconfigure(2, weight=100)


        self.amount_frame = Frame(self.lower_wrapper_frame, bg=self.BACKGROUND)
        self.amount_frame.grid(row=0, column=0, sticky="NSEW", pady=8, padx=3)
        self.amount_frame.rowconfigure(0, weight=1)
        self.amount_frame.columnconfigure(0, weight=1)

        self.amount_frame_label = Label(self.amount_frame, text="Enter Amount:", bg=BACKGROUND, font=("Arial", 13))
        self.amount_frame_label.grid(row=0, column=0, sticky="E")
        
        #self.amount_frame_entry = ttk.Entry(self.main_details_menu, style='Rounded.TEntry', font=("Arial", 13))
        self.amount_frame_entry = AmountEntryFrame(self.lower_wrapper_frame)
        self.amount_frame_entry.grid(row=0, column=1, sticky="NSEW", padx=8, pady=(0, 3))

        self.categories_menu = CategoriesMenu(self, bg=BACKGROUND)

        self.category_search_mode_panel = CategorySearchModePanel(self.lower_wrapper_frame, on_select=self.categories_menu.set_mode)
        self.category_search_mode_panel.grid(row=0, column=2, sticky="NSEW", padx=(0, 9))
        # self.category_mode_label = Label(self.lower_wrapper_frame, text="Category Search:")
        # self.category_mode_label.grid(row=0, column=2, sticky="NSEW")


        # ------ CATEGORIES - CONFIGURATION ------ #

        # self.categories_menu = CategoriesMenu(self, bg=BACKGROUND)
        self.categories_menu.grid(row=1, column=0, sticky="NEW", pady=(10, 5), padx=5)

        # ------- BUTTON_PANEL - CONFIGURATION ------ #

        self.button_panel = ButtonPanel(self, parent_frame=self)
        self.button_panel.grid(row=2, column=0, sticky="NEW", pady=5, padx=5)


        

        # Create a modal window positioned beneath the Entry widget
        self.modal_window = SearchedProductWindow(self.root, row_limit=5, max_char_limit=50)
        #self.modal_window.listbox.config(width=self.name_frame_entry.winfo_width())

        self.modal_window.load_products()
        self.modal_window.withdraw()



    def on_root_window_moved(self, event):

        # Catching some exceptions that will be thrown when the main window is created and the modal
        # window not yet.
        try:
            self.modal_window.withdraw()
        except AttributeError:
            pass   


    def show_product_name_matches(self, event):
        self.modal_window.deiconify()

        x, y = self.name_frame_entry.winfo_rootx(), self.name_frame_entry.winfo_rooty()
        _, h = self.name_frame_entry.winfo_width(), self.name_frame_entry.winfo_height()

        self.modal_window.geometry(f"+{x}+{y + h}")
        
        self.modal_window.show_matches(content=self.name_frame_entry.get())

    def get_selected_product(self):
        time.sleep(0.1)
        selection = self.modal_window.listbox.curselection()
        
        if selection:
            self.name_frame_entry.delete(0, END)
            self.name_frame_entry.insert(0, self.modal_window.listbox.get(selection[0]))
            #print(self.modal_window.listbox.get(selection[0]))



        self.modal_window.withdraw()
        
    
    def destroy_product_name_matches(self, event):
        thread = threading.Thread(target=self.get_selected_product)
        thread.start()
    
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
            amount = int(self.amount_frame_entry.entry.get())

            if amount < 1:
                raise ValueError("Product amount must be positive integer!")
            elif amount > self.shopping_list_f.product_list.ITEM_LIMIT:
                raise ValueError(f"Product amount above allowed limit: {self.shopping_list_f.product_list.ITEM_LIMIT}")
            

            self.name_frame_entry.delete(0, END)
            self.amount_frame_entry.entry.delete(0, END)
            self.amount_frame_entry.entry.insert(0, 1)

            # here program sents the newly inserted item to the market explorer so that it can pre-explore it
            item = self.shopping_list_f.insert_item(name=name, category=category, amount=amount,
                                                    category_search_mode=self.category_search_mode_panel.selected_option.get())
            self.market_explorer_f.explore_product(item=item)

            self.market_explorer_f.search_button.config(state='normal')
            
        except ValueError as error:
            messagebox.showerror("Product Specification", error)
            return
        
        return 0
        
        

    def clear_all_data(self):
        self.name_frame_entry.delete(0, END)
        self.amount_frame_entry.entry.delete(0, END)
        self.amount_frame_entry.entry.insert(0, 1)



class CategoriesMenu(Frame):
    """
    
    """

    def __init__(self, *args, **kw):
        super(CategoriesMenu, self).__init__(*args, **kw)

        # --- Frame Configuration --- #

        self.rowconfigure(0, weight=2, minsize=100)
        self.rowconfigure(1, weight=1, minsize=0)
        self.columnconfigure(0, weight=1)

        # --- ButtonsPane Configuration --- #

        self.buttons_pane = CategoryButtonsPanel(self, parent_frame=self, bg=BACKGROUND, text="Categories", font=("Arial", 15, 'bold'))
        self.buttons_pane.grid(row=0, column=0, sticky="NSEW", padx=5, pady=3)

        # --- DetailsPanel Configuration --- #

        self.details_panel = Text(self, height=5)
        self.details_panel.configure(state='disabled')
        self.details_panel.grid(row=1, column=0, sticky="NEW", padx=5, pady=3)

    
    def set_mode(self, mode: str):
        """
            Sets the category search mode, accepted values of mode:
                
                a) Off - disables whole frame, user is unable to specify any category
                b) Manual Mapping - sets the state to normal, user has to specify a category
                c) TM-based Mapping - sets the state to normal, user has to specify a category
        """


        if mode == 'Off':
            self.grid_remove()
            
        elif mode == 'Manual Mapping' or mode == 'TM-based Mapping':
            self.grid()
        #     self.enable_widgets()

    def disable_widgets(self):
        for widget in self.winfo_children():
            widget.configure(state='disabled')

    def enable_widgets(self):
        for widget in self.winfo_children():
            widget.configure(state='normal')


    def show_details(self, category: str, text: str):
        if text is not None and text:
            self.details_panel.configure(state='normal')
            self.details_panel.delete("1.0", END)  # Delete existing content
            self.details_panel.insert(END, category + '\n')
            self.details_panel.insert(END, text)
            self.details_panel.configure(state='disabled')
            





class CategoryButtonsPanel(LabelFrame):
    TEXT_WIDTH = 23
    FONT = ('Arial', 12)
    _BACKGROUND = BACKGROUND


    def __init__(self, *args, parent_frame: CategoriesMenu, **kw):
        super(CategoryButtonsPanel, self).__init__(*args, **kw)

        self.parent = parent_frame

        

       # self.__category_info_view = category_info_view

        self.__variable = IntVar()
        self.__old_val = self.__variable.get()

        self.__variable.trace_add("write", callback=self.__notify)

        # self.__unspecified = Radiobutton(self, bg=self._BACKGROUND, text="0 - Neurčená", font=self.FONT,  width=self.TEXT_WIDTH, variable=self.__variable, value=0, anchor='w',
        #                                  activebackground='grey')#highlightbackground='grey', highlightcolor='grey', highlightthickness='grey')
        
        # self.__unspecified.config(highlightbackground='grey', highlightcolor='grey')
        # self.__unspecified.grid(row=0, column=0, sticky="W")


        self.__fruit_vegetables = Radiobutton(self, activebackground='grey', bg=self._BACKGROUND, text="1 - Ovocie a zelenina", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=1, anchor='w')
        self.__fruit_vegetables.grid(row=0, column=1, sticky="W")

        self.__baked_products = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="2 - Pečivo", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=2, anchor='w')
        self.__baked_products.grid(row=1, column=0, sticky="W")

        self.__meat_and_frost = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="3 - Mäso a mrazené potraviny", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=3, anchor='w')
        self.__meat_and_frost.grid(row=1, column=1, sticky="W")

        self.__smoked_paste = Radiobutton(self, bg=self._BACKGROUND,  activebackground='grey', text="4 - Udeniny, natierky a pastety", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=4, anchor='w')
        self.__smoked_paste.grid(row=2, column=0, sticky="W")

        self.__dairies = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="5 - Mliečne výrobky", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=5, anchor='w')
        self.__dairies.grid(row=2, column=1, sticky="W")

        self.__durables_eggs = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="6 - Trvanlivé potraviny, vajcia", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=6, anchor='w')
        self.__durables_eggs.grid(row=3, column=0, sticky="W")

        self.__sweets = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="7 - Sladkosti", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=7, anchor='w')
        self.__sweets.grid(row=3, column=1, sticky="W")

        self.__snacks_seeds = Radiobutton(self, bg=self._BACKGROUND,  activebackground='grey', text="8 - Slané, snacky a semienka", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=8, anchor='w')
        self.__snacks_seeds.grid(row=4, column=0, sticky="W")

        self.__non_alcoholic_drinks = Radiobutton(self, bg=self._BACKGROUND, activebackground='grey', text="9 - Nealkoholické nápoje", font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=9, anchor='w')
        self.__non_alcoholic_drinks.grid(row=4, column=1, sticky="W")

        self.__alcohol = Radiobutton(self, bg=self._BACKGROUND, text="10 - Alkohol", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=10, anchor='w')
        self.__alcohol.grid(row=5, column=0, sticky="W")

        self.__hot_drinks = Radiobutton(self, bg=self._BACKGROUND, text="11 - Horúce nápoje", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=11, anchor='w')
        self.__hot_drinks.grid(row=5, column=1, sticky="W")

        self.__prepared_food = Radiobutton(self, bg=self._BACKGROUND, text="12 - Hotové či instatné jedlá", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=12, anchor='w')
        self.__prepared_food.grid(row=6, column=0, sticky="W")

        self.__healthy_products = Radiobutton(self, bg=self._BACKGROUND, text="13 - Zdravé potraviny", activebackground='grey', font=self.FONT, width=self.TEXT_WIDTH, variable=self.__variable, value=13, anchor='w')
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

        self.eraser_icon = PhotoImage(file=ERASER_ICON).subsample(17, 17)
        
        self.rowconfigure(0, weight=1, minsize=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.trash_bin_icon = PhotoImage(file=TRASH_BIN_ICON).subsample(18, 18)

        self.style_1 = ttk.Style()
        self.style_1.configure("TButton", font=("Arial", 13), background="skyblue", foreground="black")

        self.clear_button = ttk.Button(self,
                                   text='   clear',
                                   style="TButton",
                                   command=self.parent.clear_all_data,
                                   image=self.eraser_icon,
                                   compound='left')
        self.clear_button.grid(row=0, column=0, sticky="NSEW")

        self.cart_icon = PhotoImage(file=SHOPPING_CART_ICON_2).subsample(17, 17)

        

        self.to_cart_button = ttk.Button(self,
                                         text="   to List",
                                         style="TButton",
                                     command=self.to_list,
                                     image=self.cart_icon,
                                     compound='left',
                                     padding=(0, 8))
        
        self.to_cart_button.grid(row=0, column=1, sticky="SNEW")
    
    def to_list(self):
        content = self.parent.name_frame_entry.get()
        
        # updating the search history
        if self.parent.insert_item() == 0:
            self.parent.modal_window.insert_product(content=content)
        

        
        



