from tkinter import *
from tkinter import ttk

import multiprocessing as mpr
#import ttkbootstrap as tb

from AOSS.structure.marketing import UPDATE_INTERVAL_SIGNAL, UPDATE_STOP_SIGNAL

class SettingsPanel(LabelFrame):

    BACKGROUND = 'skyblue'
    CHILD_FRAME_BG = 'lightblue'
    LABEL = 'Adjust Settings'
    LABEL_FONT = ('Arial', 17, 'bold')
    UPDATE_OPTION_FONT = ('Arial', 13)


    def __init__(self, *args, **kw):
        super(SettingsPanel, self).__init__(*args, **kw)

        self.config(background=self.BACKGROUND, text=self.LABEL, font=self.LABEL_FONT)

        # ------ Layout Configuration ------ #
        #self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)
       # self.columnconfigure(1, weight=1)

        
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1, minsize=100)
        
        # ------- ShowTipsOption Configuration -------- #

        # self.tips_option_label_frame = LabelFrame(self, bg=self.CHILD_FRAME_BG)
        # self.tips_option_label_frame.grid(row=0, column=0, padx=(10, 30), pady=(70, 0), sticky="EW")
        # self.tips_option_label_frame.grid_propagate(False)

        # self.tips_option_label = Label(self.tips_option_label_frame,
        #                                text="Show tips:",
        #                                font=("Arial", 15),
        #                                bg=self.CHILD_FRAME_BG)
        # self.tips_option_label.pack(side='right', expand=False, fill="both")


        # self.tips_option_value_frame = LabelFrame(self, bg=self.CHILD_FRAME_BG)
        # self.tips_option_value_frame.grid(row=0, column=1, padx=(0, 10), pady=(70, 0), sticky="WNSE")


        # self.tips_option_value = IntVar()
        # self.tips_toggle_button = Checkbutton(self.tips_option_value_frame,
        #                                       variable=self.tips_option_value,
        #                                       onvalue=1,
        #                                       offvalue=0,
        #                                       bg=self.CHILD_FRAME_BG)
        # self.tips_toggle_button.select()
        # self.tips_toggle_button.pack(side='top', expand=True, fill="y")
    

        # ------- PerformUpdatesOptions Configuration -------- #

        self.perform_updates_panel = LabelFrame(self, bg=self.CHILD_FRAME_BG)
        self.perform_updates_panel.grid(row=1, column=0, pady=(10, 0), padx=(10, 30), sticky="WNSE")

        #self.perform_updates_panel.pack(side='top', fill='x', expand=False, padx=20)

        self.perform_updates_label = Label(self.perform_updates_panel,
                                           text='Perform updates:',
                                           font=("Arial", 15),
                                           bg=self.CHILD_FRAME_BG)
        self.perform_updates_label.pack(side='top', expand=False, fill='y')

        self.perform_updates_option_frame = LabelFrame(self, bg=self.CHILD_FRAME_BG)
        self.perform_updates_option_frame.grid(row=1, column=1, pady=(10, 0), padx=(0, 10), sticky="WNSE")




        self.option_var = IntVar()
        self.option_var.set(0)

        self.asap_option = Radiobutton(self.perform_updates_option_frame,
                                       text='ASAP',
                                       variable=self.option_var,
                                       value=1,
                                       font=self.UPDATE_OPTION_FONT,
                                       bg=self.CHILD_FRAME_BG)
        self.asap_option.select()
        self.asap_option.pack(side='left', expand=False, padx=(0, 10))

        self.ten_seconds_option = Radiobutton(self.perform_updates_option_frame,
                                              text='10 seconds',
                                              variable=self.option_var,
                                              value=2,
                                              font=self.UPDATE_OPTION_FONT,
                                              bg=self.CHILD_FRAME_BG)
        self.ten_seconds_option.pack(side='left', expand=False, padx=10)

        self.thirty_seconds_option = Radiobutton(self.perform_updates_option_frame,
                                                 text='30 seconds',
                                                 variable=self.option_var,
                                                 value=3,
                                                 font=self.UPDATE_OPTION_FONT,
                                                 bg=self.CHILD_FRAME_BG)
        self.thirty_seconds_option.pack(side='left', expand=False, padx=10)

        self.five_minuties_option = Radiobutton(self.perform_updates_option_frame,
                                                 text='5 minutes',
                                                 variable=self.option_var,
                                                 value=4,
                                                 font=self.UPDATE_OPTION_FONT,
                                                 bg=self.CHILD_FRAME_BG)
        self.five_minuties_option.pack(side='left', expand=False, padx=10)

        self.off_option = Radiobutton(self.perform_updates_option_frame,
                                                 text='off',
                                                 variable=self.option_var,
                                                 value=5,
                                                 font=self.UPDATE_OPTION_FONT,
                                                 bg=self.CHILD_FRAME_BG)
        self.off_option.pack(side='left', expand=False, padx=10)

        self.button = Button(self, text="Save Settings", font=("Arial", 13))
        self.button.grid
    




class SettingsFrame(Frame):
    BACKGROUND = 'skyblue'

    def __init__(self, *args, gui_to_hub: mpr.Queue, **kw):
        super(SettingsFrame, self).__init__(*args, **kw)
        
        self.gui_to_hub = gui_to_hub
        self.config(bg=self.BACKGROUND)

        self.settings_panel = SettingsPanel(self, bg='skyblue')
        self.settings_panel.pack(side='top', fill='both', expand=True)

        self.save_settings_button = ttk.Button(self,
                                               text="Save",
                                               style="TButton",
                                               padding=(8, 8),
                                               command=self.do_sth)
        self.save_settings_button.pack(side='top', fill='y', expand=False)
    
    def do_sth(self):
        if self.gui_to_hub is None:
            return
        
        match self.settings_panel.option_var.get():
            case 1:
                self.gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, 0))
            case 2:
                self.gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, 10))
            case 3:
                self.gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, 30))
            case 4:
                self.gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, 300))
            case 5:
                self.gui_to_hub.put(obj=(UPDATE_INTERVAL_SIGNAL, UPDATE_STOP_SIGNAL))


        



        
