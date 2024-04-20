from tkinter import *
from tkinter import ttk

from typing import Callable

class CategorySearchModePanel(Frame):
    BACKGROUND = 'lightblue'
    OPTIONS = ['Off', 'Manual Mapping', 'TM-based Mapping']
    DEFAULT_OPTION = 'Off'
    FONT = ('Arial', 13)

    def __init__(self, *args, on_select: Callable[[str], None], **kw):
        super(CategorySearchModePanel, self).__init__(*args, **kw)

        self.config(background=self.BACKGROUND)

        self.label = Label(self, text='Category Search: ', font=self.FONT, background=self.BACKGROUND)
        self.label.pack(side='left', fill='y')
        
        self.selected_option = StringVar()
        self.options = ttk.Combobox(self, textvariable=self.selected_option, font=self.FONT, state='readonly')
        self.options['values'] = CategorySearchModePanel.OPTIONS
        self.options.pack(side='left', pady=3, fill='y', expand=True)

        self.options.current(0)
        self.options.bind("<<ComboboxSelected>>", lambda event, name=self.selected_option: on_select(name.get()))

        



