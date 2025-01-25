import tkinter as tk
from tkinter import scrolledtext
import threading

class ServerGUI:
    def __init__(self, title = "Socialtec Server"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("600x400")

        self.logArea = tk.Text(
            self.window,
            wrap = tk.WORD,
            width = 70,
            height = 20,
            bg = "black",
            fg = "green"
        )
        self.logArea.pack(padx=10, pady=10)

    def logMessage(self, message):
        self.logArea.insert(tk.END, message + "\n")
        self.logArea.see(tk.END) # scroll automatico al final

    def start(self):
        self.window.mainloop()

    def close(self):
        self.window.quit()