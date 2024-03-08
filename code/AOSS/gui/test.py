from tkinter import *

from tkinter import ttk

import config_paths as cfg



class AmountEntryFrame(Frame):
    DEF_BG = 'blue'
    INVALID_STATE_BG = 'red'
    ENTRY_FONT = ('Arial', 13)
    VALUE_MIN = 1
    VALUE_MAX = 9999

    def on_digit_input(self, event):
        try:
            char = event.char

            if char == '\b':
                return
            
            if char.isdigit():


                if int(self.entry.get() + char) > self.VALUE_MAX:
                    raise ValueError

                self.config(bg=self.DEF_BG)
                # Continue with the desired logic for a valid digit input

            else:
                # Non-digit key pressed
                raise ValueError

        except ValueError:
            self.config(bg=self.INVALID_STATE_BG)
   
            return 'break'


    def __init__(self, *args, **kw):
        super(AmountEntryFrame, self).__init__(*args, **kw)
        
        #self.config(background=self.DEF_BG)
        #self.border_label = Label(self, text="", bg=self.BG)
        #self.border_label.pack(padx=1, pady=1, side='left', expand=True, fill='both')
        #s = ttk.Style()
        #s.configure('Rounded.TEntry', borderwidth=5, relief="flat", foreground="black", background="white")

        

        self.entry = Entry(self, font=self.ENTRY_FONT,bg='whitesmoke', borderwidth=0, width=1)
        self.entry.insert(0, 1)
        self.entry.pack(side='left', ipady=5, pady=(2), padx=(2, 0), fill='both', expand=True)

        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)
        self.entry.bind('<KeyPress>', self.on_digit_input)
        

        self.control_panel = Frame(self, bg='lightgrey')
        self.control_panel.pack(side='left', pady=2, padx=(1, 2), fill='y')

        self.inc_icon = PhotoImage(file=cfg.PLUS_ICON).subsample(50, 50)

        self.increment_button = Label(self.control_panel, image=self.inc_icon, compound='center', width=30, bg='whitesmoke')
        self.increment_button.pack(fill='y', expand=True)
        self.increment_button.bind('<Button-1>', self.on_inc_button_click)

        self.dec_icon = PhotoImage(file=cfg.MINUS_ICON).subsample(50, 30)

        self.decrement_button = Label(self.control_panel, image=self.dec_icon, compound='center', width=30,bg='whitesmoke')
        self.decrement_button.pack(fill='y', expand=True)
        self.decrement_button.bind('<Button-1>', self.on_dec_button_click)
        #self.decrement_button.pack_propagate(False)
    
    def on_focus_in(self, event):
        self.config(background=self.DEF_BG)
    
    def on_focus_out(self, event):
        self.config(background='WHITE')

    def on_inc_button_click(self, event):
        value = int(self.entry.get())
        
        if value == self.VALUE_MAX:
            self.config(bg=self.INVALID_STATE_BG)
            return

        self.entry.delete(0, END)
        self.entry.insert(0, str(value + 1))
        self.config(bg=self.DEF_BG)

    def on_dec_button_click(self, event):
        value = int(self.entry.get())

        if value == self.VALUE_MIN:
            self.config(bg=self.INVALID_STATE_BG)
            return

        self.entry.delete(0, END)
        self.entry.insert(0, str(value - 1))
        self.config(bg=self.DEF_BG)    








if __name__ == "__main__":
    root = Tk()
    root.geometry("400x50")
    frame = AmountEntryFrame(root)
    frame.pack(fill='both', expand=True)
    root.mainloop()