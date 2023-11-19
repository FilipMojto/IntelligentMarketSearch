import tkinter
from tkinter import font
import tkinter.messagebox
import customtkinter
import os
from shopping import MarketViewer
#from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="View products", width=100, height=24)
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return



class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        
        self.__shopping = MarketViewer()
        self.__shopping.load_markets()
        

        # configure window
        self.title("Automated Online Shopping System v2.0.2")
        self.geometry(f"{1000}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.label_list = []

        label = customtkinter.CTkLabel(self, text="Registered Markets", compound="left", padx=5, anchor="w")
        label.grid(row=0, column=0, pady=(20), sticky="n")

        custom_font = customtkinter.CTkFont(family="Arial", size=15, weight="bold")

        # Apply the custom font to the label
        label.configure(font=custom_font)

        self.label_list.append(label)

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, height=230, width=300, command=self.label_button_frame_event, corner_radius=0)
        self.scrollable_label_button_frame.grid(row=1, column=0, padx=0, pady=0, sticky="new")
        for i in range(self.__shopping.get_count()):  # add items with images
            market = self.__shopping.get_market_by_index(i)

            self.scrollable_label_button_frame.add_item(f"{i}. {market.name}"), #image=customtkinter.CTkImage(Image.open(os.path.join(current_dir, "test_images", "chat_light.png"))))


    def checkbox_frame_event(self):
        print(f"checkbox frame modified: {self.scrollable_checkbox_frame.get_checked_items()}")

    def radiobutton_frame_event(self):
        print(f"radiobutton frame modified: {self.scrollable_radiobutton_frame.get_checked_item()}")

    def label_button_frame_event(self, item):
        print(f"label button frame clicked: {item}")

if __name__ == "__main__":
    app = App()
    app.mainloop()