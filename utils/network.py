import socket
import threading

class NetworkManager:
    def __init__(self, host = 'localhost', port = 5000):
        self.host = host
        self.port = port
        self.serverSocket = None
        self.clients = []

    def startServer(self): # funcion para crear el server con sockets
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea un objeto socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutiliza socket
        self.serverSocket.bind((self.host, self.port)) # asocia el socket con un puerto y un host
        self.serverSocket.listen(100) # permite que el server acepte hasta 100 conecciones
        print(f"Servidor iniciado en ( {self.host} ) en el puerto ( {self.port} )")

        try: # acepta conexiones entrantes
            while True:
                clientSocket, address = self.serverSocket.accept()
                print(f"Conexión desde: {address}")

                clientThread = threading.Thread(target = self.handleClient, args = (clientSocket,)) # para manejar clientes por separado
                clientThread.start()
        except Exception as e:
            print(f"Error en el servidor: {e}")
        finally:
            if self.serverSocket:
                self.serverSocket.close()

    def handleClient(self, clientSocket): # funcion para manejar clientes
        try:
            while True:
                data = clientSocket.recv(1024) # recibe info del cliente hasta de 1024 bytes
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"Mensaje recibido: {message}")

                response = "Recibido".encode('utf-8')
                clientSocket.send(response)
        except Exception as e:
            print(f"Error manejando cliente: {e}")
        finally:
            clientSocket.close()