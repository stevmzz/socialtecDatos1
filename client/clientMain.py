from utils.network import NetworkManager
from utils.auth import AuthManager
import socket
import json

class ClientApplication:
    def __init__(self, host='localhost', port=5000, autoconnect=False):
        self.host = host
        self.port = port
        self.clientSocket = None
        self.networkManager = NetworkManager(host, port)
        self.authManager = AuthManager()
        self.currentUser = None

        if autoconnect:
            self.connectToServer()

    def connectToServer(self): # funcion para que el cliente se conecte el server
        if not self.clientSocket:
            try:
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crear socket
                self.clientSocket.connect((self.host, self.port)) # conectar al servidor
                print(f"Conectado al servidor en ( {self.host} ) en el puerto ( {self.port} )")
            except Exception as e:
                print(f"Error conectando al servidor: {e}")
                self.clientSocket = None

    def sendMessage(self, message): # funcion para enviar mensaje
        try:
            self.clientSocket.send(message.encode('utf-8'))
            print(f"Mensaje enviado: {message}")
        except Exception as e:
            print(f"Error enviando mensaje: {e}")
            self.reconnect()

    def receiveMessage(self): # funcion para recibir mensaje
        try:
            data = self.clientSocket.recv(1024)
            receivedMessage = data.decode('utf-8')
            print(f"Respuesta del servidor: {receivedMessage}")
            return receivedMessage
        except Exception as e:
            print(f"Error recibiendo mensaje: {e}")
            self.reconnect()
            return ""

    def reconnect(self):
        if self.clientSocket:
            self.clientSocket.close()
        self.connectToServer()

    def login(self, username, password): # funcion para loguearse
        try:
            self.sendMessage(f"LOGIN:{username}:{password}") # envia el mensjae de login
            serverResponse = self.receiveMessage()

            # parsear respuesta json del servidor
            responseData = json.loads(serverResponse)

            if responseData['status'] == 'success':
                self.currentUser = username # guardar el usuario actual

            return responseData  # retornar json completo
        except Exception as e:
            return {
                "status": "error",
                "message": f"Login error: {str(e)}"
            }

    def register(self, name, lastname, username, password): # funcion para registrarse
        try:
            localResult = self.authManager.registerUsers(name, lastname, username, password)

            if localResult['status'] == 'success':
                self.sendMessage(f"REGISTER:{name}:{lastname}:{username}:{password}") # envia mensaje de registrar
                serverResponse = self.receiveMessage()

                return localResult
            else:
                return localResult
        except Exception as e:
            return {
                "status": "error",
                "message": f"Registration error: {str(e)}"
            }

    def searchUsers(self, searchTerm): # funcion para buscar usuarios
        try:
            self.sendMessage(f"SEARCH:{searchTerm}") # envia la peticion de buscar
            response = self.receiveMessage()

            # manejar respuesta vacia o no valida
            if not response or response == "[]":
                return []

            return json.loads(response)
        except json.JSONDecodeError:
            print("Error decodificando respuesta del servidor")
            return []
        except Exception as e:
            print(f"Error de búsqueda: {e}")
            return []

    def addFriend(self, sender, receiver): # funcion para enviar solicitud al server de añadir amigo
        try:
            self.sendMessage(f"ADDFRIEND:{sender}:{receiver}") # envia la solicitud
            response = self.receiveMessage()
            return json.loads(response) # guarda la respuesta del server
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error añadiendo amigo: {str(e)}"
            }

    def removeFriend(self, sender, receiver):
        pass

    def closeConnection(self): # funcion para cerrar la conexion
        if self.clientSocket:
            self.clientSocket.close()
            self.clientSocket = None

def main():
    client = ClientApplication() # inicia
    try:
        from clientGUI import ClientGUI
        client_gui = ClientGUI()
        client_gui.start() # inicia el gui del cliente
    finally:
        client.closeConnection()

if __name__ == "__main__":
    main()