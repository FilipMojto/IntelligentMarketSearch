from tkinter import Frame, Tk, LabelFrame, Canvas, Scrollbar, Label
from AOSS.other.utils import TextEditor

# def update_scrollregion(canvas: Canvas):
#     canvas.update_idletasks()
#     canvas.configure(scrollregion=canvas.bbox("all"))

# def insert_new_frame(frames, my_canvas):
#     print("INSERTING")
#     # Insert a new frame into the Canvas
#     new_frame = LabelFrame(my_canvas, text=f"Frame {len(frames)}", padx=10, pady=10, bg="Red")
#     frames.append(new_frame)

#     # Calculate the y-coordinate to avoid overlapping frames
#     y_coordinate = len(frames) * (new_frame.winfo_reqheight() + 10)

#     my_canvas.create_window(0, y_coordinate, anchor='nw', window=new_frame)

#     # Update the scroll region
#     update_scrollregion(my_canvas)

from tkinter import *
from tkinter import messagebox

from tkinter import Tk, Canvas, LabelFrame

class Product(LabelFrame):
    def __init__(self, *args, text_wrap: int = 25, parent: Frame, name: str, **kwargs):
        super(Product, self).__init__(*args, **kwargs)

        self.__parent = parent
        name = TextEditor.wrap_text(name, index=text_wrap)

        name: Label = Label(self, text=name, font=('Italic', 9))
        #label : Label = self.winfo_children()[0]
        #label.configure(text= wrap_text(text=label.cget("text"), index=text_wrap))

        name.grid(row=0, column=0, sticky='NSEW')
        name.rowconfigure(0, minsize=80)
        name.columnconfigure(0, minsize=80)

        self.grid_propagate(False)
        self.bind("<Button-1>", lambda event: self.__on_click())


    def __on_click(self):
        print("CLICKED!")
        self.__parent.notify(self)

class CanvasGrid(Canvas):

    def notify(self, product: Product):
        if self.__target:
            self.__target.notify(product)


    def __init__(self, *args, x_max: int = 6, h_spacing: int = 0, v_spacing: int = 0, target = None, **kwargs):
        super(CanvasGrid, self).__init__(*args, **kwargs)

        self.canvas_grid = self

        print(f"PARENT HERE: {self.winfo_parent()}")
        self.__x_max = x_max
        self.__cur_x = 0
        self.__cur_y = 0
        self.__h_spacing = h_spacing
        self.__v_spacing = v_spacing

        self.__target = target

    def insert_window(self, frame: Frame):
                              
        if frame.master != self: # not self.nametowidget(frame.winfo_parent()) == self:
            raise TypeError("Invalid parent for the window. The parent must be this object!")


        if self.__cur_x == self.__x_max:
            self.__cur_x = 0
            self.__cur_y += 1
        
        self.create_window((self.__cur_x * frame.winfo_reqwidth() + (frame.winfo_reqwidth() * 0.5) + (self.__cur_x * self.__h_spacing),
                            self.__cur_y * frame.winfo_reqheight() + (frame.winfo_reqwidth() * 0.5) + (self.__cur_y * self.__v_spacing)), window=frame)

        self.__cur_x += 1
    
    #def insert_frame(self, )

class ScrollableCanvasGrid(Frame):
    def __init__(self, *args, x_max: int = None, row: int, col: int, target = None, **kwargs):
        super(ScrollableCanvasGrid, self).__init__(*args, **kwargs)
        
        parent: Canvas = self.nametowidget(self.winfo_parent())

        #self.__main_frame = LabelFrame(parent, text="Top", font=('Bold', 20), bg='Blue', labelanchor='n')
        self.grid(row=row, column=col, sticky='NSEW')

        parent.rowconfigure(row, weight=1)
        #top.rowconfigure(1, weight=1)

        parent.columnconfigure(col, weight=1)

        # Create an instance of Canvaser, passing 'top' as the master
        if not x_max:
            self.C = CanvasGrid(self, bg="blue", height=400, target=target, width=800)
        else:
            self.C = CanvasGrid(self, bg="blue", x_max=x_max, target=target, height=400, width=800)
        self.C.pack()  # Pack the Canvaser widget

        self.C.grid(row=0, column=0, sticky="NSEW")
    
        self.C.bind('<Configure>', lambda e: self.__update_scrollregion())

        scrollbar = Scrollbar(self, orient='vertical', command=self.C.yview)
        scrollbar.grid(row=0, column=1, sticky='SN')

        self.C.configure(yscrollcommand=scrollbar.set)
        
        scrollbar = Scrollbar(self, orient='horizontal', command=self.C.xview)
        scrollbar.grid(row=1, column=0, sticky="EW")

        self.C.configure(xscrollcommand=scrollbar.set)

        # #self.C: CanvasGrid = C
       # for i in range(60):
        #    self.insert_window(frame = LabelFrame(self.C, text=f"Frame {i + 1}", font=('Bold', 15), height=100, width=100, padx=50, pady=50 ))
            #self.__update_scrollregion()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=100)
        self.columnconfigure(1, weight=1)
        print(f"Parent: {self.winfo_parent()}")

    def insert_window(self, frame: LabelFrame):
        
        self.C.insert_window(frame)
        self.__update_scrollregion()

    def __update_scrollregion(self):
        self.C.update_idletasks()
        #self.C.configure(scrollregion=self.bbox("all"))

        bbox = self.C.bbox("all")

        #if bbox:
        if bbox:
            total_height = bbox[3] - bbox[1]
            total_width = bbox[2] - bbox[0]
            self.C.configure(scrollregion=(0, 0, total_width, total_height))
  

class ProductGrid(ScrollableCanvasGrid):
    def __init__(self, *args, src_file_path = "./code/resources/products.csv", **kwargs):
        super(ProductGrid, self).__init__(*args, **kwargs)
        self.__src_file_path = src_file_path

    def load_products(self, src_file_path: str = None, header: bool = False, wrap_i: int = 25):

        #for i in range(60):
            #self.insert_window(frame = LabelFrame(self.C, text=f"Frame {i + 1}", font=('Bold', 15), height=100, width=100, padx=50, pady=50 ))
            #self.__update_scrollregion()

        if not src_file_path:
            src_file_path = self.__src_file_path

        with open(src_file_path, 'r') as file:
            
            if header: file.readline()

            line = file.readline()

            while(line):
                attributes = line.strip().split(',')

                frame = Product(self.C, parent=self.C, text=attributes[0], name=attributes[2], font=('Bold', 15), height=150, width=150)

                #attributes[2] = wrap_text(text=attributes[2], index=wrap_i)

                # name = Label(frame, text=attributes[2], font=('Italic', 9))

                # #name.pack()
                # name.grid(row=0, column=0, sticky='NSEW')
                # name.rowconfigure(0, minsize=80)
                # name.columnconfigure(0, minsize=80)

                # frame.grid_propagate(False)

                #self.C.rowconfigure(0, weight=1)
                #.columnconfigure(0, weight=1)


                try:
                    self.insert_window(frame = frame)#, height=100, width=100, padx=50, pady=50 ))
                    #self.insert_window( LabelFrame(self.C, text=attributes[0], font=('Bold', 15)) )
   
                except ValueError:
                    pass
                    
                line = file.readline()



if __name__ == "__main__":
    top = Tk()
    #top.minsize(500, 500)

    obj = ProductGrid(top, row=0, col=0)
    obj.load_products()

    print(obj.master)    


    top.mainloop()



 