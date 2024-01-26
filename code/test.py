import tkinter as tk
import tkinter.ttk as ttk
from typing import List

class ScrallableCanvas(tk.Tk):

    def add_frame(self):
        frame = tk.Frame(self.canvas, bg="red", width=50, height=50)

        self.canvas.create_window(len(self.__frames) * 60, 0, window=frame, anchor="nw")
        self.__frames.append(frame)

    def __init__(self, *args, **kw):
        super(ScrallableCanvas, self).__init__(*args,)
        self.__frames: List[tk.Frame] = []

        self.title("Canvas with Frame")
        #ttk.Scrollbar(self, orient="horizontal")

        self.canvas = tk.Canvas(self, bg='blue', width=400, height=300)
        self.canvas.pack(side='top', fill='both', expand=True)

        self.scrollbar = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.pack(side='top', fill='x', expand=False)

        self.scrollbar.config(command=self.canvas.xview)

        self.__interior = tk.Frame(self.canvas, bg='red')
        self.__interior.bind('<Configure>', self.configure_interior)
        self.__interior.bind('<Configure>', self.configure_canvas)
        self.__interior_ID =  self.canvas.create_window(0, 0, window=self.__interior, anchor='nw')

        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        #self.canvas.bind("<Configure>", self.on_frame_configure)

        for i in range(10):
            self.add_frame()
    
    def configure_interior(self, event):
        size = (self.__interior.winfo_reqwidth(), self.__interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))

        if self.__interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width=self.__interior.winfo_reqwidth())


    def configure_canvas(self, event):
        if self.__interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.__interior_ID, width=self.canvas.winfo_width())

    # def on_frame_configure(self, event):
    #     canvas_height = self.canvas.winfo_height()
    #     for frame in self.__frames:
    #         self.canvas.itemconfig(frame, height=canvas_height)

    #     self.canvas.update_idletasks()
    #     self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    app = ScrallableCanvas()
    app.geometry("500x400")
    app.mainloop()