from tkinter import *
from tkinter import ttk

from typing import Callable

class CategorySearchModePanel(Frame):
    BACKGROUND = 'lightblue'
    # OPTIONS = ['Off', 'Manual Mapping', 'TM-based Mapping']
    DEFAULT_OPTION = 'Off'
    FONT = ('Arial', 13)

    def __init__(self, *args, on_select: Callable[[str], None], label_text: str,
                 options, **kw):
        super(CategorySearchModePanel, self).__init__(*args, **kw)

        self.config(background=self.BACKGROUND)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, minsize=145)
        self.columnconfigure(1, weight=1)

        self.label_wrapper = Frame(self, background=self.BACKGROUND)
        self.label_wrapper.grid(row=0, column=0, sticky="WSN")
        self.label = Label(self.label_wrapper, text=label_text, font=self.FONT, background=self.BACKGROUND)
        # self.label.grid(row=0, column=0, sticky="W")
        self.label.pack(side='left', fill='y')
        
        self.selected_option = StringVar()
        self.options = ttk.Combobox(self, textvariable=self.selected_option, font=self.FONT, state='readonly')
        self.options['values'] = options
        self.options.grid(row=0, column=1, sticky="WSN", pady=3)
        # self.options.pack(side='left', pady=3, fill='both', expand=True)

        self.options.current(0)
        self.options.bind("<<ComboboxSelected>>", lambda event, name=self.selected_option: on_select(name.get()))

        



