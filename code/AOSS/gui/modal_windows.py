import tkinter as tk
from tkinter import messagebox

root = tk.Tk()

reply = messagebox.askquestion(title="Warning", message="Complete data updated required. Proceed?")
print(reply)

root.mainloop()