from tkinter import *

from typing import List

from AOSS.structure.shopping import ProductCategory

# class BoundableFrame(Frame):
#     def __init__(self,*args, **kw):
#         super(BoundableFrame, self).__init__(*args, **kw)

#     def bind_widgets_recursive(self, event, handler):
#         self.bind(event, handler)
#         for child in self.winfo_children():
#             child.bind(event, handler)
#             #self.bind_widgets_recursive(event, handler)

# --- ShoppingListItem - Class Declaration&Definition --- #

class ShoppingListDetails(LabelFrame):
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self,*args, name: str, category: int, amount: int, ID: int, on_widget_click: callable = None, **kw):
        super(ShoppingListDetails, self).__init__(*args, **kw)

        self.name = name
        self.name_text = StringVar()
        self.name_text.set(f"Name: {name}")

        self.name_label = Label(self, textvariable=self.name_text, font=('Arial', 11))
        self.name_label.grid(row=0, column=0, sticky="NSW")
        self.name_label.bind("<Button-1>", on_widget_click)

    

        self.category = category
        self.category_text = StringVar()
        self.category_text.set(f"Category: {category}")

        self.amount = amount
        self.amount_text = IntVar()
        self.amount_text.set(f"Amount: {amount}")

        
        self.frame = Frame(self)
        self.frame.grid(row=1, column=0, sticky="NSEW")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.bind("<Button-1>", on_widget_click)
        


        self.category_label = Label(self.frame, textvariable=self.category_text, font=('Arial', 11))
        self.category_label.grid(row=0, column=0, sticky="W")
        self.category_label.bind("<Button-1>", on_widget_click)



        self.amount_label = Label(self.frame, textvariable=self.amount_text, font=('Arial', 11))
        self.amount_label.grid(row=0, column=1, sticky="E")
        self.amount_label.bind("<Button-1>", on_widget_click)

        

        self.ID = ID
        self.ID_text = StringVar()
        self.ID_text.set(ID)

        self.ID_label = Label(self, textvariable=self.ID_text, font=('Arial', 11, 'bold'))
        self.ID_label.grid(row=2, column=0, sticky="NSEW")
        self.ID_label.bind("<Button-1>", on_widget_click)

        if callable:
            self.name_label.bind("<Button-1>", on_widget_click)
            self.category_label.bind("<Button-1>", on_widget_click)
            self.ID_label.bind("<Button-1>", on_widget_click)


        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)


class ShoppingListItem(Frame):
    
    """
        This class represents a single product item in the user's shopping list.
    """

    def __init__(self, *args, name: str, category: str, amount: int, ID: int, on_widget_click: callable = None, **kw):
        super(ShoppingListItem, self).__init__(*args, **kw)

        self.details = ShoppingListDetails(self,  name=name, category=category, amount=amount, ID=ID, on_widget_click=self.on_item_clicked, bd=1)

        self.details.grid(row=0, column=0, sticky="NSEW", padx=2, pady=2)
        self.details.bind("<Button-1>", self.on_item_clicked)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.on_widget_click = on_widget_click

        self.is_clicked_on = False
    
    def on_item_clicked(self, event):
        self.on_widget_click()
        self.details.configure(bd=3)
        self.is_clicked_on = True


class ShoppingList(Frame):
    
    ITEM_LIMIT = 9999

    def __init__(self, *args, **kw):
        super(ShoppingList, self).__init__(*args, **kw)
        self.items: List[ShoppingListItem] = []
        self.__ID = 1
    
    def assign_ID(self):
        old_val = self.__ID
        self.__ID += 1
        return old_val

    def remove_selected_item(self, return_: bool = False):

        for item in self.items:

            if item.is_clicked_on:
                item.destroy()
                self.items.remove(item)

                if return_:
                    return item
                else:
                    break



    def get_items(self):
        """
            Returns currently stored items in the form a tuple.
        """
        product_data: List[tuple[str, ProductCategory, int]] = []


        for item in self.items:
            product_data.append((item.details.name, ProductCategory(value=item.details.category), item.details.amount))
            #item.destroy()
        
           # item.details.

        return product_data

    def remove_click_texture(self, event = None):

        for item in self.items:
            item.configure(background='white')
            item.details.configure(bd=1)
            item.is_clicked_on = False
    


class ShoppingListFrame(LabelFrame):
    def __init__(self, *args, **kw):
        super(ShoppingListFrame, self).__init__(*args, **kw)

        self.canvas = Canvas(self, bg='grey', width=5)
        self.canvas.pack(side='left', fill='both', expand=True, pady=5)
              #  self.canvas.pack(side='left', fill='both', expand=True)  # Expand in both directions

        self.scrollbar = Scrollbar(self, orient='vertical',background='grey', bg='dimgrey', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y', expand=False, pady=5, padx=3)

        self.scrollbar.config(command=self.canvas.yview)

        self.product_list = ShoppingList(self.canvas, bg='grey', width=15)

        self.product_list.bind('<Configure>', self.configure_interior)
        self.canvas.bind('<Configure>', self.configure_canvas)
        self.__interior_ID = self.canvas.create_window(0, 0, window=self.product_list, width=222, anchor='nw')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def configure_interior(self, event):
        size = (self.product_list.winfo_reqwidth(), self.product_list.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))

    def configure_canvas(self, event):
        if self.product_list.winfo_reqheight() != self.canvas.winfo_height():
            self.canvas.itemconfigure(self.__interior_ID, height=self.product_list.winfo_reqheight())
            self.update_scrollbar()


    def update_scrollbar(self):
        self.canvas.update_idletasks()
        size = (self.product_list.winfo_reqwidth(), self.product_list.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        self.scrollbar.update()



    def insert_item(self, name: str, category: int, amount: int):

        """
            Inserts a new ShoppingListItem instance into the shopping list.

            Items are stored by using pack manager, they are appended to the top, so that they are
            placed vertically representing a shopping list.

            Newly created instance is returned immediatelly.
        
        """

        item = ShoppingListItem(self.product_list,
                                name=name,
                                category=category,
                                amount=amount,
                                ID=self.product_list.assign_ID(),
                                on_widget_click=self.product_list.remove_click_texture,
                                width=240, bg='grey')

        item.pack(side="top", fill="x", expand=False, padx=2, pady=2)

        self.product_list.items.append(item)
        item.bind("<Button-1>", self.product_list.remove_click_texture)

        # Update scrollbar after inserting new item
        self.update_scrollbar()

        event = Event()
        event.widget = self.canvas
        self.configure_canvas(event)


        self.canvas.update_idletasks()
        self.canvas.update()

        return item
