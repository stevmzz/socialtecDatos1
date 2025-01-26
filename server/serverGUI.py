import tkinter as tk
from tkinter import scrolledtext
import threading

class ServerGUI:
    def __init__(self, socialGraph, title="Socialtec Server"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("600x400")
        self.socialGraph = socialGraph  # referencia al grafo
        self.logMessages = [] # lista para almacenar mensajes del server
        self.logActive = False # rastrear si el log está activo

        # main frame
        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        # frame de navegacion
        self.navFrame = tk.Frame(self.mainFrame, bg = 'lightgray')
        self.navFrame.pack(side = tk.TOP, fill = tk.X)

        # frame del contenido principal (frame de frames)
        self.contentFrame = tk.Frame(self.mainFrame)
        self.contentFrame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self.createNavButtons() # crear botones
        self.createLogFrame() # iniciar con el frame del log

    def createNavButtons(self): # funcion para crear botones
        logButton = tk.Button(self.navFrame, text = "Servidor", command = self.createLogFrame)
        logButton.pack(side = tk.LEFT, padx = 5, pady = 5)

        graphButton = tk.Button(self.navFrame, text = "Grafo Social", command = self.createGraphFrame)
        graphButton.pack(side = tk.LEFT, padx = 5, pady = 5)

        statsButton = tk.Button(self.navFrame, text="Estadísticas", command=self.createStatsFrame)
        statsButton.pack(side=tk.LEFT, padx=5, pady=5)

    def createLogFrame(self): # funcion para crear el frame del log
        for widget in self.contentFrame.winfo_children(): # borrar todo lo que haya
            widget.destroy()

        self.logActive = True # marcar log como activo

        # crear area del log
        self.logArea = tk.Text(
            self.contentFrame,
            wrap=tk.WORD,
            width=70,
            height=20,
            bg="black",
            fg="green"
        )
        self.logArea.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # borra los logs y los guarda
        self.logArea.delete('1.0', tk.END)
        for message in self.logMessages:
            self.logArea.insert(tk.END, message + "\n")

        self.logArea.see(tk.END) # scroll automatico al final

    def createGraphFrame(self): # crea el frame del grafo
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        self.logActive = False

        graphLabel = tk.Label(self.contentFrame, text="Grafo Social")
        graphLabel.pack()

    def createStatsFrame(self): # crea el frame de las stats
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        self.logActive = False

        statsLabel = tk.Label(self.contentFrame, text="Estadísticas")
        statsLabel.pack()

    def logMessage(self, message): # funcion para mostrar los mensajes del server
        self.logMessages.append(message)

        try:
            if self.logActive and hasattr(self, 'logArea'):
                self.logArea.insert(tk.END, message + "\n")
                self.logArea.see(tk.END)
        except Exception as e:
            print(f"Error logging message: {e}")

    def showGraph(self): # funcion para mostrar el grafo
        pass

    def start(self): # iniciar ventana
        self.window.mainloop()

    def close(self): # cerrar ventana
        self.window.quit()