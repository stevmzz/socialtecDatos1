import json
import socket
import threading
from utils.auth import AuthManager

class NetworkManager:
    def __init__(self, host = 'localhost', port = 5000):
        self.host = host
        self.port = port
        self.serverSocket = None
        self.clients = {}
        self.authManager = AuthManager()

    def startServer(self): # funcion para crear el server con sockets
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea un objeto socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutiliza socket
        self.serverSocket.bind((self.host, self.port)) # asocia el socket con un puerto y un host
        self.serverSocket.listen(100) # permite que el server acepte hasta 100 conecciones
        print(f"Servidor iniciado en [ {self.host} ] en el puerto [ {self.port} ]")

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

                # manejar diferentes tipos de mensajes
                if message.startswith("LOGIN:"):
                    response = self.handleLogin(message)
                elif message.startswith("REGISTER:"):
                    response = self.handleRegister(message)
                elif message.startswith("SEARCH:"):
                    response = self.handleSearchUser(message)
                elif message.startswith("ADDFRIEND:"):
                    response = self.handleAddFriend(message)
                elif message.startswith("ISFRIEND:"):
                    response = self.handleIsFriend(message)
                elif message.startswith("REMOVEFRIEND"):
                    response = self.handleRemoveFriend(message)
                elif message.startswith("GETFRIENDS:"):
                    response = self.handleGetFriends(message)
                else:
                    response = "Recibido"

                clientSocket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error manejando cliente: {e}")
        finally:
            clientSocket.close()

    def handleLogin(self, message): # funcion para menajar el login
        _, username, password = message.split(":") # parsea los datos
        login_result = self.authManager.loginUsers(username, password) # loguear usario
        return json.dumps(login_result)

    def handleRegister(self, message): # funcion para menejar el registro
        _, name, lastname, username, password = message.split(":")
        register_result = self.authManager.registerUsers(name, lastname, username, password)
        return register_result['message']

    def handleSearchUser(self, message): # funcion para el manejo de busqueda de usuarios
        _, searchTerm = message.split(":")
        users = self.authManager.searchUsers(searchTerm)
        return json.dumps(users) # devolver lista de usarios que coinciden

    def handleAddFriend(self, message):
        try:
            _, sender, receiver = message.split(":")
            from server.serverMain import SocialGraph
            socialGraph = SocialGraph()
            socialGraph.loadFriendships()

            if socialGraph.addFriend(sender, receiver):
                socialGraph.saveFriendships()

                return json.dumps({
                    "status": "success",
                    "message": f"[{sender}] add [{receiver}] like a friend"
                })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error añadiendo amigo: {str(e)}"
            })

    def handleRemoveFriend(self, message):
        try:
            _, sender, receiver = message.split(":")
            from server.serverMain import SocialGraph
            socialGraph = SocialGraph()
            socialGraph.loadFriendships()

            # Eliminar la amistad
            result = socialGraph.removeFriend(sender, receiver)

            # Si la eliminación fue exitosa
            return json.dumps(result)
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error verificando amistad: {str(e)}"
            })

    def handleIsFriend(self, message):
        try:
            _, user1, user2 = message.split(":")
            from server.serverMain import SocialGraph
            socialGraph = SocialGraph()
            socialGraph.loadFriendships()

            isFriend = socialGraph.isFriends(user1, user2)

            return json.dumps({
                "status": "success",
                "isFriend": isFriend
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": f"Error verificando amistad: {str(e)}"
            })

    def handleGetFriends(self, message):
        try:
            _, username = message.split(":")
            from server.serverMain import SocialGraph
            socialGraph = SocialGraph()
            socialGraph.loadFriendships()

            # Obtener lista de amigos
            friends = socialGraph.getFriends(username)

            # Obtener información completa de cada amigo
            friends_info = []
            for friend_username in friends:
                # Buscar la información completa del usuario
                friend_data = self.authManager.searchUsers(friend_username)
                if friend_data:
                    # Si encontramos el usuario, lo añadimos a la lista
                    for user in friend_data:
                        if user['username'] == friend_username:
                            friends_info.append(user)
                            break

            return json.dumps(friends_info)
        except Exception as e:
            print(f"Error obteniendo amigos: {e}")
            return json.dumps([])