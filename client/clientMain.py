from utils.network import NetworkManager
from utils.auth import AuthManager
import socket
import json

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
        except Exception as e:
            print(f"Error conectando al servidor: {e}")

    def sendMessage(self, message): # funcion para enviar mensaje
        try:
            if not self.clientSocket:
                self.connectToServer()
            self.clientSocket.send(message.encode('utf-8'))
            print(f"Mensaje enviado: {message}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            self.clientSocket = None

    def receiveMessage(self): # funcion para recibir mensaje
        try:
            if not self.clientSocket:
                self.connectToServer()
            data = self.clientSocket.recv(1024)
            received_message = data.decode('utf-8')
            print(f"Respuesta del servidor: {received_message}")
            return received_message
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            self.clientSocket = None
            return ""

    def login(self, username, password):
        try:
            self.sendMessage(f"LOGIN:{username}:{password}")
            server_response = self.receiveMessage()

            # Parsear respuesta JSON del servidor
            response_data = json.loads(server_response)
            return response_data  # Retornar JSON completo
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

    def searchUsers(self, searchTerm):
        try:
            self.connectToServer()
            self.sendMessage(f"SEARCH:{searchTerm}")
            response = self.receiveMessage()

            # Manejar respuesta vacía o inválida
            if not response or response == "[]":
                return []

            return json.loads(response)
        except json.JSONDecodeError:
            print("Error decodificando respuesta del servidor")
            return []
        except Exception as e:
            print(f"Search error: {e}")
            return []
        finally:
            if self.clientSocket:
                self.clientSocket.close()
                self.clientSocket = None

def main():
    client = ClientApplication() # inicia
    client.connectToServer() # se conecta al server
    from clientGUI import ClientGUI
    client_gui = ClientGUI()
    client_gui.start() # inicia el gui del cliente

if __name__ == "__main__":
    main()