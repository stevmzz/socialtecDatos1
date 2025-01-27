from utils.network import NetworkManager
from utils.auth import AuthManager
from server.serverGUI import ServerGUI
import threading
import time
import sys # para redirigir prints
import os
import json
from datetime import datetime

class SocialGraph:
    def __init__(self):
        self.graph = {}

    def addUser(self, username): # añade un nuevo usuario al grafo
        if username not in self.graph: # si el usuario no existe lo añade a una lista de amigos vacia
            self.graph[username] = set()
            return True
        return False

    def isFriends(self, user1, user2): # verifica si son amigos
        return user2 in self.graph.get(user1, set())

    def loadFriendships(self, filename = 'friendships.json'): # carga amistades desde un archivo json
        try:
            with open(filename, 'r') as f:
                loaded_graph = json.load(f)
                self.graph = {user: set(friends) for user, friends in loaded_graph.items()}
            return True
        except FileNotFoundError:
            print("Archivo no encontrado")
            return False
        except Exception as e:
            print(f"Error cargando amistades: {e}")
            return False

    def saveFriendships(self, filename = 'friendships.json'): # guarda amistades en un archivo json
        try:
            with open(filename, 'w') as f:
                json.dump({user: list(friends) for user, friends in self.graph.items()}, f, indent=4)
            return True
        except Exception as e:
            print(f"Error guardando amistades: {e}")
            return False

    def addFriend(self, user1, user2): # añade una relacion de amistad entre dos usuarios
        if user1 not in self.graph:
            self.addUser(user1)
        if user2 not in self.graph:
            self.addUser(user2)

        if user2 not in self.graph[user1]:
            self.graph[user1].add(user2)
            return True
        return False

    def removeFriendship(self, user1, user2): # elimina una relacion de amistad entre dos usuarios
        pass

    def getFriends(self, username): # obtiene la lista de amigos de un usuario
        return list(self.graph.get(username, set()))

    def findFriendPath(self, user1, user2): # funcion para buscar el path entre amigos
        # verificar si los usuarios existen en el grafo
        if user1 not in self.graph or user2 not in self.graph:
            return None

        # si ya son amigos directos
        if user2 in self.graph[user1]:
            return [user1, user2]

        queue = [[user1]] # cola para bfs
        visited = set([user1]) # conjunto para rastrear usuarios visitados

        while queue: # mientras haya caminos
            path = queue.pop(0) # tomar el primero camino
            lastUser = path[-1] # obtener el ultimo usuario en el camino actual

            # revisar amigos del ultimo usuario en el path
            for friend in self.graph.get(lastUser, set()):
                if friend == user2:
                    # camino encontrado
                    return path + [friend]

                if friend not in visited: # si el amigo no ha sido visitado
                    visited.add(friend) # marcar como visitado
                    newPath = list(path) # actualizamos el path
                    newPath.append(friend) # añadimos el amigo
                    queue.append(newPath) # añadimos el nuevo camino a la cosa para seguir buscando

        return None # no se encontró camino

class ServerApplication:
    class GuiLogger:  # clase para redirigir los prints
        def __init__(self, gui):
            self.gui = gui

        def write(self, message): # funcion para escribir el mensaje del server
            if message.strip():
                timestamp = datetime.now().strftime('[%H:%M:%S]:')
                formattedMessage = f"> {timestamp} {message.strip()}"
                self.gui.logMessage(formattedMessage)

        def flush(self):
            pass  # necesario para compatibilidad con sys.stdout

    def __init__(self, gui, socialGraph):
        self.networkManager = NetworkManager()
        self.socialGraph = socialGraph
        self.serverThread = None
        self.running = False
        self.gui = gui

    def start(self): # funcion para iniciar el server mediante hilos
        sys.stdout = self.GuiLogger(self.gui)
        self.running = True
        self.serverThread = threading.Thread(target=self.runServer)
        self.serverThread.start()

    def runServer(self): # funcion auxiliar para correr el servidor
        while self.running:
            try:
                self.networkManager.startServer()
            except Exception as e:
                print(f"Error en el servidor: {e}")
                time.sleep(1) # espera un segundo para prevenir colapsos

    def stop(self): # funcion para detener el servidor
        self.running = False
        if self.serverThread:
            self.serverThread.join()

def main():
    socialGraph = SocialGraph() # inicializa el grafo
    socialGraph.loadFriendships() # carga las amistades existentes
    gui = ServerGUI(socialGraph) # para enviar los prints y el grafo
    server = ServerApplication(gui, socialGraph) # inicia
    server.start() # inicia el server
    gui.start() # inicia el bucle de gui

if __name__ == "__main__":
    main()