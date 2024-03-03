import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Rounded Entry Example")

    # Create a style with rounded corners
    s = ttk.Style()
    s.configure('Rounded.TEntry', borderwidth=5, relief="flat", foreground="black", background="white")

    # Create a rounded entry
    rounded_entry = ttk.Entry(root, style='Rounded.TEntry', font=('Arial', 12))
    rounded_entry.pack(padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()