import json
import os

class AuthManager:
    def __init__(self, usersFile = 'users.json'):
        self.userFile = usersFile

        if not os.path.exists(self.userFile): # si no existe el archivo de usarios crearlo
            with open(self.userFile, 'w') as f:
                json.dump({}, f)

    def loadUsers(self): # carga usarios desde archivo json
        try:
            with open(self.userFile, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def saveUsers(self, users): # guardar usarios en al archivo json
        with open(self.userFile, 'w') as f:
            json.dump(users, f, indent=4)

    def registerUsers(self, name, lastname, user, password): # registra un usario
        users = self.loadUsers()
        user = user.lower().strip()

        ############### validaciones ###############

        if not all([name, lastname, user, password]):
            return {
                "status": "error",
                "message": "All fields are required"
            }

        if user in users:
            return {
                "status": "error",
                "message": "Username already exists"
            }

        if len(user) < 4:
            return {
                "status": "error",
                "message": "Username must be at least 4 characters long"
            }

        if len(password) < 8:
            return {
                "status": "error",
                "message": "Password must be at least 8 characters long"
            }

        ############### validaciones ###############

        users[user] = {
            "nombre": name,
            "apellido": lastname,
            "contraseña": password
        }
        self.saveUsers(users)

        return {
            "status": "success",
            "message": "User successfully registered"
        }

    def loginUsers(self, user, password): # iniciar sesion con un usario
        users = self.loadUsers()
        user = user.lower().strip()

        if user not in users: # verificar si existe el usario
            return {
                "status": "error",
                "message": "User not found"
            }

        if users[user]["contraseña"] != password:  # verificar si la contraseña coincide
            return {
                "status": "error",
                "message": "Invalid username or password. Please try again"
            }

        return { # inicio de sesión exitoso
            "status": "success",
            "message": "Login successful! Welcome back"
        }

    def searchUsers(self, searchTerm): # buscar usuario en el json
        users = self.loadUsers()
        results = []
        searchTerms = searchTerm.lower().split()

        for username, userData in users.items():
            userFullname = f"{userData['nombre']} {userData['apellido']}".lower()
            if all(term in userFullname for term in searchTerms):
                result = {
                    'username': username,
                    'nombre': userData['nombre'],
                    'apellido': userData['apellido']
                }
                results.append(result)

        return results