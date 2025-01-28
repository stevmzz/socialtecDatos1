import tkinter as tk
from tkinter import scrolledtext, Toplevel, Button, font, messagebox
from clientMain import ClientApplication
import json

class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SocialTec Client")
        self.window.geometry("300x450")
        self.window.config(bg="#c0c0c0")
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.client = ClientApplication(autoconnect = False)
        self.createLoginFrame()

    def onClosing(self):
        self.window.destroy() # cerrar ventana principal

    def createLoginFrame(self): # crea el frame del login
        for widget in self.window.winfo_children(): # recorre todos los elementos y los borra
            widget.destroy()

        # frame del contenido principal (frame de frames)
        self.contentFrame = tk.Frame(self.window, borderwidth=2, relief="sunken", bg="#c0c0c0")
        self.contentFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # header para el titulo
        headerFrame = tk.Frame(self.contentFrame, bg="navy", height=30)
        headerFrame.pack(fill="x")
        headerFrame.pack_propagate(False)

        # titulo
        tk.Label(headerFrame, text="SOCIALTEC", fg="white", bg="navy",font=("Arial", 14, "bold")).pack(pady=5)

        # frame del login
        loginFrame = tk.Frame(self.contentFrame, bg="#c0c0c0")
        loginFrame.pack(expand=True, fill="both", padx=10, pady=10)

        # usuario
        tk.Label(loginFrame, text="Username", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(20, 5))
        self.usernameEntry = tk.Entry(loginFrame, width=40)
        self.usernameEntry.pack(fill="x", ipady=10)

        # contraseña
        tk.Label(loginFrame, text="Password", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(15, 5))
        self.passwordEntry = tk.Entry(loginFrame, width=40, show="*")
        self.passwordEntry.pack(fill="x", ipady=10)

        # Remember me and Lost password frame
        optionsFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        optionsFrame.pack(fill="x", pady=15)

        # para recordar contraseña (estetica)
        self.rememberVar = tk.BooleanVar()
        tk.Checkbutton(optionsFrame, text="Remember me", variable=self.rememberVar, bg="#c0c0c0").pack(side="left")

        # olvido contraseña (estetica)
        lostPassButton = tk.Label(optionsFrame, text="Lost password?", fg="blue", cursor="hand2", bg="#c0c0c0")
        lostPassButton.pack(side="right")

        # boton de loguearse
        loginButton = tk.Button(loginFrame, text="Login",
                                command=self.login, relief="groove",
                                bg="#d3d3d3", width=30)
        loginButton.pack(pady=15, ipady=5)

        # boton de registrarse y frame
        registerFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        registerFrame.pack(fill="x", pady=10)
        tk.Label(registerFrame, text="Not registered? ", bg="#c0c0c0").pack(side="left")
        registerLink = tk.Label(registerFrame, text="Create account", fg="blue", cursor="hand2", bg="#c0c0c0")
        registerLink.pack(side="left")
        registerLink.bind("<Button-1>", lambda e: self.createRegisterFrame())

    def createRegisterFrame(self): # crea el frame del registro
        for widget in self.window.winfo_children(): # crea el frame del registro
            widget.destroy() # recorre todos los elemtos y los borra

        # frame del registro
        registerFrame = tk.Frame(self.window)
        registerFrame.pack(expand = True, fill = 'both')

        # titulo
        tk.Label(registerFrame, text = "Registrarse").pack()

        # nombre
        tk.Label(registerFrame, text="Nombre").pack()
        self.nameEntry = tk.Entry(registerFrame, width = 25)
        self.nameEntry.pack()

        # apellido
        tk.Label(registerFrame, text="Apellido").pack()
        self.lastnameEntry = tk.Entry(registerFrame, width = 25)
        self.lastnameEntry.pack()

        # usuario
        tk.Label(registerFrame, text="Usuario").pack()
        self.regUsernameEntry = tk.Entry(registerFrame, width = 25)
        self.regUsernameEntry.pack()

        # contraseña
        tk.Label(registerFrame, text="Contraseña").pack()
        self.regPasswordEntry = tk.Entry(registerFrame, show="*", width = 25)
        self.regPasswordEntry.pack()

        # boton para añadir foto de perfil
        photoButton = tk.Button(registerFrame, text="Añadir foto de perfil")
        photoButton.pack(pady=5)

        # boton de registrarse
        register_btn = tk.Button(registerFrame, text = "Crear cuenta", command = self.register)
        register_btn.pack(pady=10)

        # boton de volver al login
        back_btn = tk.Button(registerFrame, text = "Volver al login", command = self.createLoginFrame)
        back_btn.pack()

    def createProfileFrame(self, username, is_current_user=False): # frame para los perfiles de usuario
        for widget in self.window.winfo_children():
            widget.destroy()

        profileFrame = tk.Frame(self.window)
        profileFrame.pack(expand=True, fill='both')

        tk.Button(profileFrame, text="Volver", command=self.createSearchFrame).pack()

    def login(self): # intenta loguear usuario
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if not username or not password:
            messagebox.showerror("Error", "meta los dos")
            return

        try: # intenta conectar al server
            self.client.connectToServer()
            result = self.client.login(username, password)

            if result['status'] == 'success':
                messagebox.showinfo("Login", result['message'])
                self.createSearchFrame()
            else:
                messagebox.showerror("error", result['message'])
        except Exception as e:
            messagebox.showerror("error", str(e))

    def register(self): # intenta registrar ususario
        name = self.nameEntry.get()
        lastname = self.lastnameEntry.get()
        username = self.regUsernameEntry.get()
        password = self.regPasswordEntry.get()

        if not all([name, lastname, username, password]):
            messagebox.showerror("Error", "meta todo")
            return

        try: # intenta conectar al server
            self.client.connectToServer()
            result = self.client.register(name, lastname, username, password)

            if result['status'] == 'success':
                messagebox.showinfo("Registration", result['message'])
                self.createLoginFrame()
            else:
                messagebox.showerror("Registration Failed", result['message'])
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))

    def createSearchFrame(self): # crea el frame de la zona de busqueda
        for widget in self.window.winfo_children():
            widget.destroy()

        # frame de busqueda
        searchFrame = tk.Frame(self.window)
        searchFrame.pack(expand=True, fill='both')

        # frame para el header (titulo y boton de perfil)
        headerFrame = tk.Frame(searchFrame)
        headerFrame.pack(fill='x')

        # titulo y boton de perfil
        tk.Label(headerFrame, text="Buscar Personas").pack(side='left')
        tk.Button(headerFrame, text="Mi Perfil", command=lambda: self.createProfileFrame(self.client.currentUser, is_current_user=True)).pack(side='right')

        tk.Label(searchFrame, text="Buscar Personas").pack()

        # espacio de buscar
        self.searchEntry = tk.Entry(searchFrame, width=25)
        self.searchEntry.pack()

        # boton de buscar
        searchButton = tk.Button(searchFrame, text="Buscar", command=self.search)
        searchButton.pack()

        # para mostrar resultados
        self.resultsFrame = tk.Frame(searchFrame)
        self.resultsFrame.pack(expand=True, fill='both')

    def search(self): # funcion para buscar personas
        searchTerm = self.searchEntry.get()

        if not searchTerm:
            messagebox.showerror("Error", "meta algo")
            return

        try:
            self.client.connectToServer()
            results = self.client.searchUsers(searchTerm)

            for widget in self.resultsFrame.winfo_children():
                widget.destroy()

            if not results:
                tk.Label(self.resultsFrame, text="no hay gente").pack()
            else:
                for user in results: # crea un frame para cada ususario encontrado
                    userFrame = tk.Frame(self.resultsFrame)
                    userFrame.pack(fill = 'x', pady = 5)

                    # muestra la info del usario buscado
                    tk.Label(userFrame, text = f"{user['nombre']} {user['apellido']} (@{user['username']})").pack(side = 'left')

                    # frame para el boton de perfil de los usuarios
                    buttonFrame = tk.Frame(userFrame)
                    buttonFrame.pack(side='right')

                    # boton de ver perfil
                    tk.Button(buttonFrame, text="Ver perfil",
                              command=lambda u=user['username']: self.createProfileFrame(u)).pack(side='right')

                    # boton de añadir amigo
                    if user['username'] != self.client.currentUser:
                        buttonText = self.getFriendshipButtonText(user['username'])
                        friendButton = tk.Button(userFrame, text = buttonText, command = lambda u = user['username']: self.toggleFriendship(u))
                        friendButton.pack(side='right')

        except Exception:
            print("error")

    def toggleFriendship(self, username): # verifica si son amigos para eliminar o añadir
        try:
            currentUser = self.client.currentUser

            # enviar solicitud al servidor para añadir o eliminar amigo
            self.client.connectToServer()
            self.client.sendMessage(f"ISFRIEND:{currentUser}:{username}")
            response = self.client.receiveMessage()

            # parsear la respuesta del servidor
            result = json.loads(response)

            # determinar si agregar o eliminar amigo
            if result.get('status') == 'success' and result.get('isFriend'):
                result = self.client.removeFriend(currentUser, username) # si son amigos entonces "eliminar amigo"
            else:
                result = self.client.addFriend(currentUser, username) # sino "añadir amigo"

            if result['status'] == 'success':
                messagebox.showinfo("Éxito", result['message'])
                self.search()  # actualizar la vista
            else:
                messagebox.showerror("Error", result['message'])

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def getFriendshipButtonText(self, username):  # funcion para cambiar el boton de estado (eliminar/añadir amigo)
        try:
            # enviar una solicitud al servidor para verificar si son amigos
            self.client.connectToServer()
            self.client.sendMessage(f"ISFRIEND:{self.client.currentUser}:{username}")
            response = self.client.receiveMessage()

            # parsear la respuesta del servidor
            result = json.loads(response)

            # si son amigos el boton dice eliminar amigo
            if result.get('status') == 'success' and result.get('isFriend'):
                return "Eliminar amigo"
            else:
                return "Añadir amigo"
        except Exception as e:
            print(f"Error verificando amistad: {e}")
            return "Añadir amigo"

    def start(self):
        self.window.mainloop()