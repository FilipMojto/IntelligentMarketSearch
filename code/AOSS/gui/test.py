import tkinter as tk

class CircularProgress(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.width = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = min(self.center_x, self.center_y) - 5
        self.angle = 0
        self.speed = 1

        self.configure(bg="white", highlightthickness=0)
        self.create_oval(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            outline="gray", width=2
        )

        self.arc = self.create_arc(
            self.center_x - self.radius, self.center_y - self.radius,
            self.center_x + self.radius, self.center_y + self.radius,
            start=0, extent=0, outline="blue", width=3, style=tk.ARC
        )
        self.after(50, self.update)

    def update(self):
        self.angle += self.speed
        if self.angle > 360:
            self.angle = 0
        self.draw_arc()
        self.after(50, self.update)

    def draw_arc(self):
        self.itemconfig(
            self.arc,
            extent=self.angle,
            outline="blue" if self.angle <= 180 else "red"
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Circular progress indicator")
    progress = CircularProgress(root, width=100, height=100)
    progress.pack()
    root.mainloop()