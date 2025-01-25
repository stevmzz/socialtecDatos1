from utils.network import NetworkManager
from utils.auth import AuthManager
import threading
import time

class SocialGraph:
    def __init__(self):
        pass

class ServerApplication:
    def __init__(self):
        self.networkManager = NetworkManager()
        self.authManager = AuthManager()
        self.socialGraph = SocialGraph()
        self.serverThread = None
        self.running = False

    def start(self): # funcion para iniciar el server mediante hilos
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
    server = ServerApplication() # inicia
    server.start() # inicia el server

if __name__ == "__main__":
    main()