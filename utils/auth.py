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
                "message": "Todos los campos son obligatorios"
            }

        if user in users:
            return {
                "status": "error",
                "message": "El nombre de usario ya existe"
            }

        if len(user) < 4:
            return {
                "status": "error",
                "message": "El nombre de usuario debe tener al menos 4 caracteres"
            }

        if len(password) < 8:
            return {
                "status": "error",
                "message": "La contraseña debe tener al menos 8 caracteres"
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
            "message": "Usuario registrado exitosamente"
        }

    def loginUsers(self, user, password): # iniciar sesion con un usario
        users = self.loadUsers()
        user = user.lower().strip()

        if user not in users: # verificar si existe el usario
            return {
                "status": "error",
                "message": "Usuario no encontrado"
            }

        if users[user]["contraseña"] != password:  # verificar si la contraseña coincide
            return {
                "status": "error",
                "message": "Contraseña incorrecta"
            }

        return { # inicio de sesión exitoso
            "status": "success",
            "message": "Inicio de sesión exitoso"
        }

    def searchUsers(self, searchTerm):
        users = self.loadUsers()
        results = []

        # Convertir término de búsqueda a minúsculas
        searchTerms = searchTerm.lower().split()

        for username, userData in users.items():
            # Buscar si TODOS los términos coinciden parcialmente
            if all(
                    any(term in campo.lower() for campo in
                        [userData['nombre'], userData['apellido'], username])
                    for term in searchTerms
            ):
                result = {
                    'username': username,
                    'nombre': userData['nombre'],
                    'apellido': userData['apellido']
                }
                results.append(result)

        return results