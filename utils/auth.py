# Servidor/auth.py
from passlib.hash import pbkdf2_sha256
import json
import os

class AuthManager:
    def __init__(self, usersFile='users.json'):
        self.userFile = usersFile
        if not os.path.exists(self.userFile):
            with open(self.userFile, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False)

    def loadUsers(self):
        try:
            with open(self.userFile, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def saveUsers(self, users):
        with open(self.userFile, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def registerUsers(self, name, lastname, user, password):
        users = self.loadUsers()
        user = user.lower().strip()

        if user in users:
            return {
                "status": "error",
                "message": "Username already exists"
            }

        # Hash the password using PBKDF2
        hashed_password = pbkdf2_sha256.hash(password)

        users[user] = {
            "nombre": name,
            "apellido": lastname,
            "contraseña": hashed_password
        }
        self.saveUsers(users)

        return {
            "status": "success",
            "message": "User successfully registered"
        }

    def loginUsers(self, user, password):
        users = self.loadUsers()
        user = user.lower().strip()

        if user not in users:
            return {
                "status": "error",
                "message": "User not found"
            }

        # Verify the password against the stored hash
        stored_hash = users[user]["contraseña"]
        try:
            if pbkdf2_sha256.verify(password, stored_hash):
                return {
                    "status": "success",
                    "message": "Login successful! Welcome back"
                }
            else:
                return {
                    "status": "error",
                    "message": "Invalid username or password. Please try again"
                }
        except Exception:
            # Si la contraseña aún no está hasheada (durante la transición)
            if password == stored_hash:
                # Actualizar a hash si coincide la contraseña antigua
                users[user]["contraseña"] = pbkdf2_sha256.hash(password)
                self.saveUsers(users)
                return {
                    "status": "success",
                    "message": "Login successful! Welcome back"
                }
            return {
                "status": "error",
                "message": "Invalid username or password. Please try again"
            }

    def searchUsers(self, searchTerm):  # buscar usuario en el json
        users = self.loadUsers()
        results = []
        searchTerm = searchTerm.lower().strip()

        for username, userData in users.items():
            userFullname = f"{userData['nombre']} {userData['apellido']}".lower()

            # Buscar en el nombre de usuario
            if searchTerm in username.lower():
                results.append({
                    'username': username,
                    'nombre': userData['nombre'],
                    'apellido': userData['apellido']
                })
            # Buscar en el nombre completo
            elif searchTerm in userFullname:
                results.append({
                    'username': username,
                    'nombre': userData['nombre'],
                    'apellido': userData['apellido']
                })

        return results
