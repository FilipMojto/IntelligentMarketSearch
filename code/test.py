from tkinter import Tk, Menu

def file_new():
    print("New File")

def file_open():
    print("Open File")

def file_save():
    print("Save File")

# def edit_cut():
#     print("Cut")

# def edit_copy():
#     print("Copy")

# def edit_paste():
#     print("Paste")

# Create the main application window
app = Tk()
app.title("Menu Example")

# Create a Menu widget
main_menu = Menu(app)
app.config(menu=main_menu)

# Create a File menu
file_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=file_new)
file_menu.add_command(label="Open", command=file_open)
file_menu.add_command(label="Save", command=file_save)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

# # Create an Edit menu
# edit_menu = Menu(main_menu, tearoff=0)
# main_menu.add_cascade(label="Edit", menu=edit_menu)

# edit_menu.add_command(label="Cut", command=edit_cut)
# edit_menu.add_command(label="Copy", command=edit_copy)
# edit_menu.add_command(label="Paste", command=edit_paste)

# Start the Tkinter event loop
app.mainloop()