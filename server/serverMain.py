from utils.network import NetworkManager
from utils.auth import AuthManager
import threading

class SocialGraph:
    def __init__(self):
        pass

class ServerApplication:
    def __init__(self):
        self.networkManager = NetworkManager()
        self.authManager = AuthManager()
        self.socialGraph = SocialGraph()

    def start(self): # funcion para iniciar el server mediante hilos
        serverThread = threading.Thread(target = self.networkManager.startServer)
        serverThread.start()

def main():
    server = ServerApplication() # inicia
    server.start() # inicia el server

if __name__ == "__main__":
    main()