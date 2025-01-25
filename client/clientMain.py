from utils.network import NetworkManager
from utils.auth import AuthManager
import socket

class ClientApplication:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clientSocket = None

    def connectToServer(self): # funcion para que el cliente se conecte el server
        try:
            self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crear socket

            # conectar al servidor
            self.clientSocket.connect((self.host, self.port))
            print(f"Conectado al servidor en ( {self.host} ) en el puerto ( {self.port} )")

            self.sendMessage("hola") # mensaje de prueba
            self.receiveMessage() # recibir respuesta del server

        except Exception as e:
            print(f"Error conectando al servidor: {e}")
        finally:
            if self.clientSocket:
                self.clientSocket.close()

    def sendMessage(self, message): # funcion para enviar mensaje
        if self.clientSocket:
            try:
                self.clientSocket.send(message.encode('utf-8'))
                print(f"Mensaje enviado: {message}")
            except Exception as e:
                print(f"Error enviando mensaje: {e}")

    def receiveMessage(self): # funcion para recibir mensaje
        if self.clientSocket:
            try:
                data = self.clientSocket.recv(1024)
                print(f"Respuesta del servidor: {data.decode('utf-8')}")
            except Exception as e:
                print(f"Error recibiendo mensaje: {e}")

def main():
    client = ClientApplication() # inicia
    client.connectToServer() # se conecta al server

if __name__ == "__main__":
    main()