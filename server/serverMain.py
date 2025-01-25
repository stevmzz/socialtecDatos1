from utils.network import NetworkManager
from utils.auth import AuthManager
from server.serverGUI import ServerGUI
import threading
import time
import sys # para redirigir prints

class SocialGraph:
    def __init__(self):
        pass

class ServerApplication:
    class GuiLogger:  # clase para redirigir los prints
        def __init__(self, gui):
            self.gui = gui

        def write(self, message):
            if message.strip():
                self.gui.logMessage(message.strip())

        def flush(self):
            pass  # necesario para compatibilidad con sys.stdout

    def __init__(self, gui):
        self.networkManager = NetworkManager()
        self.authManager = AuthManager()
        self.socialGraph = SocialGraph()
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
    gui = ServerGUI() # para enviar los prints
    server = ServerApplication(gui) # inicia
    server.start() # inicia el server
    gui.start() # inicia el bucle de gui

if __name__ == "__main__":
    main()