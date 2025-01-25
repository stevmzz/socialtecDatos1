from utils.network import NetworkManager
from utils.auth import AuthManager
import socket

class ClientApplication:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.clientSocket = None
        self.networkManager = NetworkManager(host, port)
        self.authManager = AuthManager()

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

    def login(self, username, password):
        try:
            localResult = self.authManager.loginUsers(username, password)

            if localResult['status'] == 'success':
                self.sendMessage(f"LOGIN:{username}:{password}") # envia el mensaje de login
                server_response = self.receiveMessage()

                return localResult
            else:
                return localResult
        except Exception as e:
            return {
                "status": "error",
                "message": f"Login error: {str(e)}"
            }
        finally:
            if self.clientSocket:
                self.clientSocket.close()

    def register(self, name, lastname, username, password):
        try:
            localResult = self.authManager.registerUsers(name, lastname, username, password)

            if localResult['status'] == 'success':
                self.sendMessage(f"REGISTER:{name}:{lastname}:{username}:{password}") # envia mensaje de registrar
                server_response = self.receiveMessage()
                return localResult
            else:
                return localResult
        except Exception as e:
            return {
                "status": "error",
                "message": f"Registration error: {str(e)}"
            }
        finally:
            if self.clientSocket:
                self.clientSocket.close()

def main():
    client = ClientApplication() # inicia
    client.connectToServer() # se conecta al server
    from clientGUI import ClientGUI
    client_gui = ClientGUI()
    client_gui.start() # inicia el gui del cliente

if __name__ == "__main__":
    main()