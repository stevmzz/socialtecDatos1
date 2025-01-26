import tkinter as tk
from tkinter import scrolledtext, Toplevel, Button
import threading
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ServerGUI:
    def __init__(self, socialGraph, title="Socialtec Server"):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry("600x400")
        self.socialGraph = socialGraph  # referencia al grafo
        self.logMessages = [] # lista para almacenar mensajes del server
        self.logActive = False # rastrear si el log está activo

        import matplotlib
        matplotlib.use('TkAgg') # usar con tkinter

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

        searchPathButton = tk.Button(self.navFrame, text="Buscar Path", command=self.createSeachFriendsPath)
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

        self.logActive = False # marcar el log como desactivado

        # crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))

        # crear grafo dirigido
        G = nx.DiGraph()

        # añadir conexiones
        for user, friends in self.socialGraph.graph.items():
            for friend in friends:
                # verificar si la amistad es mutua
                if user in self.socialGraph.graph.get(friend, set()):
                    G.add_edge(user, friend, color = 'grey', style = 'solid', width = 2)
                else:
                    G.add_edge(user, friend, color = 'grey', style = 'dashed', width = 1)

        pos = nx.spring_layout(G, k=0.5) # calcular posiciones de los nodos

        # dibujar nodos
        nx.draw_networkx_nodes(G, pos, node_color = 'grey', node_size = 300, ax = ax)

        # nombre de nodos
        nx.draw_networkx_labels(G, pos, font_size = 8, ax = ax)

        # dibujar aristas con diferentes estilos
        edges = G.edges() # obtiene las aristas
        edgeColors = [G[u][v]['color'] for u, v in edges]
        edgeStyles = [G[u][v]['style'] for u, v in edges]
        edgeWidths = [G[u][v]['width'] for u, v in edges]
        nx.draw_networkx_edges(G, pos, edge_color = edgeColors, style = edgeStyles, width = edgeWidths, arrows = True, arrowsize = 10, ax = ax)

        ax.axis('off') # oculta ejes visuales (un cuadro)

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

    def start(self): # iniciar ventana
        self.window.mainloop()

    def close(self): # cerrar ventana
        self.window.quit()