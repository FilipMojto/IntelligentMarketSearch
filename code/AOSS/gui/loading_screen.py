from tkinter import *
from tkinter import ttk


class LoadingScreen(Tk):

    WIDTH = 500
    HEIGHT = 290
    SCROLLBAR_WIDTH = 250
    INFO_FONT = ('Arial', 11)


    def __init__(self, *args, **kw):
        super(LoadingScreen, self).__init__(*args, **kw)
        self.overrideredirect(True)


        # here we get the width and height of the machine's screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - LoadingScreen.WIDTH) // 2
        y = (screen_height - LoadingScreen.HEIGHT) // 2

        self.geometry(f"{LoadingScreen.WIDTH}x{LoadingScreen.HEIGHT}+{x}+{y}")

        # self.frame = Frame(self)
        # self.frame.pack()
        #self.frame.grid(row=0, column=0, sticky="NSEW")

        


        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, length=LoadingScreen.SCROLLBAR_WIDTH, mode='determinate')
        self.progress_bar.pack(side='bottom')



        self.info_text = Label(self, text="loading...", font=('Arial', 11))
        self.info_text.pack(side='bottom')
        self.info_text.config(font=self.INFO_FONT)

        #self.progress_bar.grid(row=0, column=0, sticky="S", pady=5)

        #self.label = Label(self.frame, text="THIS IS LOADING SCREEN!", font=("Arial", 12))
        #self.label.grid(row=0, column=0)

        #self.frame.rowconfigure(0, weight=1)
        #self.frame.columnconfigure(0, weight=1)

        

        #self.rowconfigure(0, weight=1)
        #self.columnconfigure(0, weight=1)

