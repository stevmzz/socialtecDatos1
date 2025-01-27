import tkinter as tk
from tkinter import scrolledtext, Toplevel, Button, font
import threading
import networkx as nx
import matplotlib.pyplot as plt
from PIL.ImageOps import expand
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ServerGUI:
    def __init__(self, socialGraph, title="Socialtec Server"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("650x450")
        self.window.config(bg="#c0c0c0")
        self.socialGraph = socialGraph  # referencia al grafo
        self.logMessages = [] # lista para almacenar mensajes del server
        self.logActive = False # rastrear si el log está activo

        import matplotlib
        matplotlib.use('TkAgg') # usar con tkinter
        plt.style.use('classic')

        self.retroFont = font.Font(family="Courier New", size=10, weight="bold") # fuente para los botones

        # main frame
        self.mainFrame = tk.Frame(self.window, relief="raised", borderwidth=3, bg="#c0c0c0")
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # frame de navegacion
        self.navFrame = tk.Frame(self.mainFrame, borderwidth=2, relief="sunken", bg="#c0c0c0")
        self.navFrame.pack(side = tk.TOP, fill = tk.X, padx=5, pady=5)

        # frame del contenido principal (frame de frames)
        self.contentFrame = tk.Frame(self.mainFrame, borderwidth=2, relief="sunken", bg="#c0c0c0")
        self.contentFrame.pack(side = tk.TOP, fill = tk.BOTH, expand = True, padx=5, pady=5)

        self.createNavButtons() # crear botones
        self.createLogFrame() # iniciar con el frame del log

    def createRetroButtons(self, parent, text, command): # funcion auxiliar para botones
        return tk.Button(parent, text=text, command = command, relief="raised", borderwidth=3, font=self.retroFont, bg="#c0c0c0", width=15, height=2, activebackground="#d4d0c8")

    def createNavButtons(self): # funcion para crear botones
        buttonFrame = tk.Frame(self.navFrame, bg="#c0c0c0")
        buttonFrame.pack(expand=True, pady=10)  # centra el frame dentro de navframe

        logButton = self.createRetroButtons(buttonFrame, text="Servidor", command=self.createLogFrame)
        logButton.pack(side=tk.LEFT, padx=5, pady=5)

        graphButton = self.createRetroButtons(buttonFrame, text="Grafo Social", command=self.createGraphFrame)
        graphButton.pack(side=tk.LEFT, padx=5, pady=5)

        statsButton = self.createRetroButtons(buttonFrame, text="Estadísticas", command=self.createStatsFrame)
        statsButton.pack(side=tk.LEFT, padx=5, pady=5)

        searchPathButton = self.createRetroButtons(buttonFrame, text="Buscar Path", command=self.createSeachFriendsPath)
        searchPathButton.pack(side=tk.LEFT, padx=5, pady=5)

    def createSeachFriendsPath(self): # crea el frame de las stats
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        self.logActive = False

        pathLabel = tk.Label(self.contentFrame, text="Buscar Path")
        pathLabel.pack()

        # entry para amigo "a"
        entryFriendA = tk.Entry(self.contentFrame, width=25)
        entryFriendA.pack()

        # entry para amigo "b"
        entryFriendB = tk.Entry(self.contentFrame, width=25)
        entryFriendB.pack()

        # boton de buscar path
        searchPathButton = tk.Button(self.contentFrame, text="Buscar Path", command=self.searchPath)
        searchPathButton.pack()

    def searchPath(self):
        userA = self.contentFrame.winfo_children()[1].get() # entryFriendA
        userB = self.contentFrame.winfo_children()[2].get() # entryFriendB

        # limpiar resultados previos
        for widget in self.contentFrame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget('text') != "Buscar Path":
                widget.destroy()

        # buscar path
        path = self.socialGraph.findFriendPath(userA, userB)

        # mostrar resultados
        if path:
            if len(path) > 2:
                result = f"Path encontrado: {' -> '.join(path)}"
            else:
                result = f"Son amigos directos: {path[0]} y {path[1]}"

            resultLabel = tk.Label(self.contentFrame, text=result)
            resultLabel.pack()
        else:
            resultLabel = tk.Label(self.contentFrame, text="No existe path")
            resultLabel.pack()

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
            fg="#00ff00",
            font=("Courier New", 10),
            relief="sunken",
            borderwidth=2
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

        self.logActive = False # marcar el log como desactivado
        self.socialGraph.loadFriendships() # recargar los datos mas recientes para actualizar grafo
        plt.clf() # limpiar cualquier figura existente para actualizar el grafo

        # crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))

        fig.patch.set_facecolor('#f0f0f0') # color del fondo

        # crear grafo dirigido
        G = nx.DiGraph()

        # añadir conexiones
        for user, friends in self.socialGraph.graph.items():
            for friend in friends:
                # verificar si la amistad es mutua
                if user in self.socialGraph.graph.get(friend, set()):
                    G.add_edge(user, friend, color = '#808080', style = 'solid', width = 2)
                else:
                    G.add_edge(user, friend, color = '#000080', style = 'dashed', width = 2)

        pos = nx.spring_layout(G, k=0.5) # calcular posiciones de los nodos

        # limpiar el eje actual
        ax.clear()

        # dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color = '#c0c0c0', node_size = 1000, ax = ax, edgecolors="#000080", linewidths=1)

        # nombre de nodos
        nx.draw_networkx_labels(G, pos, font_size = 12, ax = ax, font_family="Courier New", font_weight="bold")

        # dibujar aristas con diferentes estilos
        edges = G.edges() # obtiene las aristas
        edgeColors = [G[u][v]['color'] for u, v in edges]
        edgeStyles = [G[u][v]['style'] for u, v in edges]
        edgeWidths = [G[u][v]['width'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, edge_color = edgeColors, style = edgeStyles, width = edgeWidths, arrows = True, arrowsize = 15, min_source_margin=10, min_target_margin=15)

        ax.axis('off') # oculta ejes visuales (un cuadro)

        # frame para info
        infoFrame = tk.Frame(self.contentFrame, relief="raised", borderwidth=2, bg="#c0c0c0")
        infoFrame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # label de info
        tk.Label(infoFrame, text="Info:", font=self.retroFont, bg="#c0c0c0").pack(side=tk.LEFT, padx=5)
        tk.Label(infoFrame, text="── Amistad mutua", font=self.retroFont, bg="#c0c0c0", fg="#808080").pack(side=tk.LEFT, padx=5)
        tk.Label(infoFrame, text="--- Amistad unidireccional", font=self.retroFont, bg="#c0c0c0", fg="#000080").pack(side=tk.LEFT, padx=5)

        # incrustar grafico de matplotlib en tkinter
        canvas = FigureCanvasTkAgg(fig, master = self.contentFrame)
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.pack(fill = tk.BOTH, expand = True)
        canvas.draw() # dibujar canvas
        plt.close(fig) # limpiar grafico

    def createStatsFrame(self): # crea el frame de las stats
        for widget in self.contentFrame.winfo_children():
            widget.destroy()

        self.logActive = False

        statsLabel = tk.Label(self.contentFrame, text="Estadísticas\n\n(En desarrollo)", font=self.retroFont, bg="#c0c0c0", relief="sunken", borderwidth=2, padx=20, pady=20)
        statsLabel.pack(expand=True)

    def logMessage(self, message): # funcion para mostrar los mensajes del server
        self.logMessages.append(message)

        try:
            if self.logActive and hasattr(self, 'logArea'):
                self.logArea.insert(tk.END, message + "\n")
                self.logArea.see(tk.END)
        except Exception as e:
            print(f"Error logging message: {e}")

    def start(self): # iniciar ventana
        self.window.mainloop()

    def close(self): # cerrar ventana
        self.window.quit()