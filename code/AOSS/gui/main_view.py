from tkinter import *

import multiprocessing as mpr

import os, sys

# Set the starting point to the directory containing the script
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_directory)

# Move up two directories to reach the parent directory (AOSS)
parent_directory = os.path.abspath(os.path.join(script_directory, '..', '..'))
sys.path.append(parent_directory)

import config_paths as cfg

from AOSS.gui.shopping_list import ShoppingListFrame

from AOSS.gui.product_specification import ProductSpecificationMenu

from AOSS.gui.market_explorer import MarketExplorerFrame
from AOSS.gui.settings import SettingsFrame

from AOSS.structure.shopping import MarketHub





class MainView(Frame):

    def on_key_press(self, event, main_view):

        key_pressed = event.keysym

        if key_pressed == "Delete":
            main_view.market_explorer_window.delete_product()



    def __init__(self, *args, root: Tk, market_hub, gui_to_hub: mpr.Queue,
                 app_name: str, app_version: str, **kw):
        super(MainView, self).__init__(*args, **kw)
        


        self.root = root
        self.market_hub = market_hub

        self.main_menu_panel = MainMenu(self, app_name=app_name, app_version=app_version, parent=self, bg='skyblue')
        self.main_menu_panel.pack(side='left', fill='y', expand=False)

        self.main_window = Frame(self, bg='lightblue', width=50)

        self.main_window.pack(side='left', fill='both', expand=True)


        self.list_frame = Frame(self.main_window, bg='skyblue')
        self.list_frame.pack(side='left', fill='both', expand=True)

        self.market_explorer_window = None

        self.shopping_list_window = ShoppingListFrame(self.list_frame,
                                                      text='Shopping List',
                                                      font=('Arial', 17, 'bold'),
                                                      bg='skyblue',
    
                                                      on_delete=lambda item: self.market_explorer_window.delete_product(item))
        self.shopping_list_window.pack(side='right', fill='y', expand=False, pady=6, padx=(3, 5))
        
        market_hub = MarketHub(src_file=cfg.MARKET_HUB_FILE['path'])
        market_hub.load_markets()
        market_hub.load_products()



        self.market_explorer_window = MarketExplorerFrame(self.list_frame,
                                                          bg='skyblue',
                                                    root=self.list_frame,
                                                    market_hub=self.market_hub,
                                                    shopping_list_frame=self.shopping_list_window,
                                                    text='Explore Markets',
                                                    font=("Arial", 17, 'bold'))
        



        self.specification_window = ProductSpecificationMenu(self.list_frame,
                                                text='Specify Product',
                                                font=('Arial', 17, 'bold'),
                                                root=self.root,
                                                shopping_list_frame=self.shopping_list_window,
                                                market_explorer_frame=self.market_explorer_window,
                                                bg='skyblue')
        self.specification_window.pack(side='right', fill='both', expand=True, pady=6, padx=(0, 3))


        # self.explorer_frame = Frame(self.main_window)

       
        self.settings_frame = SettingsFrame(self.main_window, gui_to_hub=gui_to_hub)

        #market_explorer_window 
    
    def exit(self):
        self.quit()
        self.root.quit()


class MainMenu(Frame):

    BUTTON_Y_PAD = 2


    def __init__(self, *args, parent: MainView, app_name: str, app_version: str, **kw):
        super(MainMenu, self).__init__(*args, **kw)
        
        self.parent = parent
        


        #self.parent = parent
        # ----- Layout Configuration ------ #
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        self.app_name_label = Label(self, text=app_name + " v" + app_version, font=('Arial', 17, 'bold'), bg='deepskyblue')
        self.app_name_label.pack(side='top', fill='x', expand=False, pady=(51, 20))
        
        ##self.shopping_list_option = Frame(self, bg='aqua')
       # self.shopping_list_option.pack(side='top', fill='x', expand=False, pady=(6, self.BUTTON_Y_PAD))

        self.shopping_list_icon = PhotoImage(file=cfg.SHOPPING_CART_ICON).subsample(13, 13)
        
        # ----- Specification Option Configuration ----- #
        self.shopping_list_option = Button(self, pady=10, padx=9, bg='aqua', text="Shopping List", font=('Arial', 15, 'bold'),
                                           image=self.shopping_list_icon,
                                           compound='right',
                                           anchor='e',
                                           state='disabled',
                                           command=self.to_shopping_list)
        self.shopping_list_option.pack(side='top', fill='x', expand=False, pady=(0,2))
        
        #self.shopping_list_l = Label(self.shopping_list_option, image=self.shopping_list_icon, compound='right', bg='aqua')
        #self.shopping_list_l.pack(side='left', fill='y', expand=False)

        #self.shopping_list_option.pack(side='top', fill='x', expand=False, pady=(6, self.BUTTON_Y_PAD))  # Set the height to 50 (adjust as needed)
        # self.shopping_list_option.rowconfigure(0, weight=1)
        # self.shopping_list_option.columnconfigure(0, weight=1)
        # self.shopping_list_option_label = Label(self.shopping_list_option, text="Shopping List", font=('Arial', 15, 'bold'))
        # self.shopping_list_option_label.pack(side='top', expand=False)  

        self.magnifier_icon = PhotoImage(file=cfg.MAGNIFIER_ICON).subsample(19, 19)
        # ----- Explorer Option Configuration ----- #
        self.explorer_option = Button(self,  pady=12, padx=12, bg='aqua', text="Market Explorer ", font=('Arial', 15, 'bold'),
                                      image=self.magnifier_icon,
                                      compound='right',
                                      anchor='e',
                                      command=self.to_market_explorer)
        self.explorer_option.pack(side='top', fill='x', expand=False, pady=self.BUTTON_Y_PAD)

       # self.explorer_option.grid(row=1, column=0, sticky="NEW")
        # self.explorer_option_label = Button(self.explorer_option, text="Market Explorer", font=('Arial', 15, 'bold'))
        # self.explorer_option_label.pack(side='top')

        self.gear_icon = PhotoImage(file=cfg.GEAR_ICON).subsample(19, 19)

        # ----- Settings Option Configuration ----- #
        self.settings_option = Button(self, pady=12, padx=12, bg='aqua', text="Settings ", font=('Arial', 15, 'bold'),
                                      image=self.gear_icon,
                                      compound='right',
                                      anchor='e',
                                      command=self.to_settings_panel)
        self.settings_option.pack(side='top', fill='x', expand=False, pady=self.BUTTON_Y_PAD)

       # self.explorer_option.grid(row=1, column=0, sticky="NEW")
        # self.settings_option_label = Label(self.settings_option, text="Settings", font=('Arial', 15, 'bold'))
        # self.settings_option_label.pack(side='top')

        # ----- Exit Option Configuration ----- #

        self.exit_icon = PhotoImage(file=cfg.EXIT_ICON).subsample(19, 19)
        self.exit_option = Button(self, pady=12, padx=12, bg='aqua', text="Exit ", font=('Arial', 15, 'bold'),
                                  image=self.exit_icon,
                                  compound='right',
                                  anchor='e',
                                  command=self.exit)
        self.exit_option.pack(side='top', fill='x', expand=False, pady=self.BUTTON_Y_PAD)

        self.selected_option = self.shopping_list_option

        # # self.explorer_option.grid(row=1, column=0, sticky="NEW")
        # self.exit_option_label = Label(self.exit_option, text="Exit", font=('Arial', 15, 'bold'))
        # self.exit_option_label.pack(side='top')  
    
    def exit(self):
        self.quit()
        self.parent.exit()


    def to_market_explorer(self):

        for child in self.parent.main_window.winfo_children():
            child.pack_forget()

        self.parent.specification_window.pack_forget()
        self.parent.market_explorer_window.pack(side='right', fill='both', expand=True, pady=6, padx=(0, 3))
        self.parent.list_frame.pack(side='left', fill='both', expand=True)

        self.selected_option.config(state='normal')
        self.explorer_option.config(state='disabled')
        self.selected_option = self.explorer_option

    

    def to_shopping_list(self):
        for child in self.parent.main_window.winfo_children():
            child.pack_forget()

        self.parent.market_explorer_window.pack_forget()
        self.parent.specification_window.pack(side='right', fill='both', expand=True, pady=6, padx=(0, 3))
        self.parent.list_frame.pack(side='left', fill='both', expand=True)

        self.selected_option.config(state='normal')
        self.shopping_list_option.config(state='disabled')
        self.selected_option = self.shopping_list_option


    
    def to_settings_panel(self):
        for child in self.parent.main_window.winfo_children():
            child.pack_forget()
        
        self.parent.settings_frame.pack(side='left', fill='both', expand=True, padx=(0, 5), pady=6)

        self.selected_option.config(state='normal')
        self.settings_option.config(state='disabled')
        self.selected_option = self.settings_option

        self.parent.main_window.config(bg='skyblue')

