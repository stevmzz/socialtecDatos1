import tkinter as tk
from tkinter import scrolledtext, Toplevel, Button, font
from clientMain import ClientApplication
import json


class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SocialTec Client")
        self.window.geometry("350x650")
        self.window.config(bg="#c0c0c0")
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.client = ClientApplication(autoconnect=False)
        self.createLoginFrame()

    def onClosing(self):
        self.window.destroy()  # cerrar ventana principal

    def showMessage(self, message, isError=False): # funcion para mostrar mensajes en un frame
        # limpia mensajes anteriores si existen
        if hasattr(self, 'messageFrame'):
            self.messageFrame.destroy()

        bgColor = "#ffcccc" if isError else "#ccffcc"  # rojo claro para errores, verde claro para exito

        # crea el frame del mensaje
        self.messageFrame = tk.Frame(self.window, bg=bgColor, relief="sunken", borderwidth=1)
        self.messageFrame.pack(side="bottom", fill="x", padx=5, pady=5)

        # muestra el mensaje
        messageLabel = tk.Label(self.messageFrame, text=message, bg=bgColor, wraplength=250)
        messageLabel.pack(pady=20)

        # autodestruye el mensaje después de 3 segundos
        self.window.after(3000, self.messageFrame.destroy)

    def togglePasswordVisibility(self, entry_widget): # funcion para la visibilidad de la contraseña
        if entry_widget.cget('show') == '':
            entry_widget.config(show='*')
        else:
            entry_widget.config(show='')

    def createLoginFrame(self):  # crea el frame del login
        for widget in self.window.winfo_children():  # recorre todos los elementos y los borra
            widget.destroy()

        # frame del contenido principal (frame de frames)
        self.contentFrame = tk.Frame(self.window, borderwidth=2, relief="sunken", bg="#c0c0c0")
        self.contentFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # header para el titulo
        headerFrame = tk.Frame(self.contentFrame, bg="navy", height=30)
        headerFrame.pack(fill="x")
        headerFrame.pack_propagate(False)

        # titulo
        tk.Label(headerFrame, text="SOCIALTEC", fg="white", bg="navy", font=("Arial", 14, "bold")).pack(pady=5)

        # frame del login
        loginFrame = tk.Frame(self.contentFrame, bg="#c0c0c0")
        loginFrame.pack(expand=True, fill="both", padx=10, pady=10)

        # usuario
        tk.Label(loginFrame, text="Username", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(20, 5))
        self.usernameEntry = tk.Entry(loginFrame, width=40)
        self.usernameEntry.pack(fill="x", ipady=10)

        # contraseña
        passwordFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        passwordFrame.pack(fill="x", pady=(15, 5))
        passwordContentFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        passwordContentFrame.pack(fill="x")
        tk.Label(passwordFrame, text="Password", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(15, 5))
        self.passwordEntry = tk.Entry(passwordContentFrame, width=35, show="*")
        self.passwordEntry.pack(side="left", ipady=10, fill="x", expand=True, pady=2)

        # boton de mostrar/ocultar contraseña
        showPasswordBtn = tk.Button(passwordContentFrame, text="👁", relief="raised",
                                    bg="#d3d3d3", width=2, height=1,
                                    command=lambda: self.togglePasswordVisibility(self.passwordEntry))
        showPasswordBtn.pack(side="right", padx=10)

        # remember me frame
        optionsFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        optionsFrame.pack(fill="x", pady=15)

        # para recordar contraseña (estetica)
        self.rememberVar = tk.BooleanVar()
        tk.Checkbutton(optionsFrame, text="Remember me", variable=self.rememberVar, bg="#c0c0c0").pack(side="left")

        # olvido contraseña (estetica)
        lostPassButton = tk.Label(optionsFrame, text="Lost password?", fg="blue", cursor="hand2", bg="#c0c0c0")
        lostPassButton.pack(side="right")

        # boton de loguearse
        loginButton = tk.Button(loginFrame, text="Login", command=self.login, relief="groove", bg="#d3d3d3", width=30)
        loginButton.pack(pady=15, ipady=5)

        # boton de registrarse y frame
        registerFrame = tk.Frame(loginFrame, bg="#c0c0c0")
        registerFrame.pack(fill="x", pady=10)
        tk.Label(registerFrame, text="Not registered? ", bg="#c0c0c0").pack(side="left")
        registerLink = tk.Label(registerFrame, text="Create account", fg="blue", cursor="hand2", bg="#c0c0c0")
        registerLink.pack(side="left")
        registerLink.bind("<Button-1>", lambda e: self.createRegisterFrame())

    def createRegisterFrame(self):  # crea el frame del registro
        for widget in self.window.winfo_children():  # recorre todos los elementos y los borra
            widget.destroy()

        # frame del contenido principal (frame de frames)
        self.contentFrame = tk.Frame(self.window, borderwidth=2, relief="sunken", bg="#c0c0c0")
        self.contentFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # header para el titulo
        headerFrame = tk.Frame(self.contentFrame, bg="navy", height=30)
        headerFrame.pack(fill="x")
        headerFrame.pack_propagate(False)

        # titulo
        tk.Label(headerFrame, text="CREATE ACCOUNT", fg="white", bg="navy", font=("Arial", 14, "bold")).pack(pady=5)

        # frame del registro
        registerFrame = tk.Frame(self.contentFrame, bg="#c0c0c0")
        registerFrame.pack(expand=True, fill="both", padx=10, pady=10)

        # nombre
        tk.Label(registerFrame, text="Nombre", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(20, 5))
        self.nameEntry = tk.Entry(registerFrame, width=40)
        self.nameEntry.pack(fill="x", ipady=5)

        # apellido
        tk.Label(registerFrame, text="Apellido", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(15, 5))
        self.lastnameEntry = tk.Entry(registerFrame, width=40)
        self.lastnameEntry.pack(fill="x", ipady=5)

        # usuario
        tk.Label(registerFrame, text="Usuario", bg="#c0c0c0", anchor="w").pack(fill="x", pady=(15, 5))
        self.regUsernameEntry = tk.Entry(registerFrame, width=40)
        self.regUsernameEntry.pack(fill="x", ipady=5)

        # frame para contraseña
        passwordFrame = tk.Frame(registerFrame, bg="#c0c0c0")
        passwordFrame.pack(fill="x", pady=(15, 5))

        tk.Label(passwordFrame, text="Contraseña", bg="#c0c0c0", anchor="w").pack(fill="x")

        # frame para el contenido de la contraseña
        passwordContentFrame = tk.Frame(registerFrame, bg="#c0c0c0")
        passwordContentFrame.pack(fill="x")

        self.regPasswordEntry = tk.Entry(passwordContentFrame, width=35, show="*")
        self.regPasswordEntry.pack(side="left", ipady=5, fill="x", expand=True)

        # boton de mostrar/ocultar contraseña
        showPasswordBtn = tk.Button(passwordContentFrame, text="👁", relief="raised",
                                    bg="#d3d3d3", width=2, height=1,
                                    command=lambda: self.togglePasswordVisibility(self.regPasswordEntry))
        showPasswordBtn.pack(side="right", padx=10)

        # frame para botones de perfil y registro
        buttonsFrame = tk.Frame(registerFrame, bg="#c0c0c0")
        buttonsFrame.pack(fill="x", pady=20)

        # boton para añadir foto de perfil
        photoButton = tk.Button(buttonsFrame, text="Añadir foto de perfil", relief="raised",
                                bg="#d3d3d3", width=30)
        photoButton.pack(pady=5, ipady=5)

        # boton de registrarse
        registerButton = tk.Button(buttonsFrame, text="Crear cuenta", command=self.register,
                                   relief="groove", bg="#d3d3d3", width=30)
        registerButton.pack(pady=5, ipady=5)

        # frame para volver al login
        backFrame = tk.Frame(registerFrame, bg="#c0c0c0")
        backFrame.pack(fill="x", pady=10)

        tk.Label(backFrame, text="¿Ya tienes cuenta? ", bg="#c0c0c0").pack(side="left")
        backLink = tk.Label(backFrame, text="Iniciar sesión", fg="blue", cursor="hand2", bg="#c0c0c0")
        backLink.pack(side="left")
        backLink.bind("<Button-1>", lambda e: self.createLoginFrame())

    def createProfileFrame(self, username, is_current_user=False):  # frame para los perfiles de usuario
        for widget in self.window.winfo_children():
            widget.destroy()

        profileFrame = tk.Frame(self.window)
        profileFrame.pack(expand=True, fill='both')

        tk.Button(profileFrame, text="Volver", command=self.createSearchFrame).pack()

    def login(self):  # intenta loguear usuario
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        if not username or not password:
            self.showMessage("Please enter both username and password", isError=True)
            return

        try:  # intenta conectar al server
            self.client.connectToServer()
            result = self.client.login(username, password)

            if result['status'] == 'success':
                self.showMessage(result['message'])
                self.createSearchFrame()
            else:
                self.showMessage(result['message'], isError=True)
        except Exception as e:
            self.showMessage(str(e), isError=True)

    def register(self):  # intenta registrar ususario
        name = self.nameEntry.get()
        lastname = self.lastnameEntry.get()
        username = self.regUsernameEntry.get()
        password = self.regPasswordEntry.get()

        if not all([name, lastname, username, password]):
            self.showMessage("Please complete all required fields", isError=True)
            return

        try:  # intenta conectar al server
            self.client.connectToServer()
            result = self.client.register(name, lastname, username, password)

            if result['status'] == 'success':
                self.showMessage(result['message'])
                self.createLoginFrame()
            else:
                self.showMessage(result['message'], isError=True)
        except Exception as e:
            self.showMessage(str(e), isError=True)

    def createSearchFrame(self):  # crea el frame de la zona de busqueda
        for widget in self.window.winfo_children():
            widget.destroy()

        # frame de busqueda
        searchFrame = tk.Frame(self.window, bg="#c0c0c0", relief="raised", borderwidth=2)
        searchFrame.pack(expand=True, fill='both')

        # frame para el header (titulo y boton de perfil)
        headerFrame = tk.Frame(searchFrame, bg="navy", height=30)
        headerFrame.pack(fill="x")
        headerFrame.pack_propagate(False)

        # frame para contenido del header
        titleBarFrame = tk.Frame(headerFrame, bg="navy")
        titleBarFrame.pack(fill="x", padx=5)

        # titulo
        titleLabel = tk.Label(titleBarFrame, text="Search Users", fg="white", bg="navy", font=("System", 12, "bold"))
        titleLabel.pack(side="left", pady=5)

        # boton de perfil
        profileBtn = tk.Button(titleBarFrame, text="My Profile", relief="raised", bg="#c0c0c0",
                               activebackground="#d4d0c8", borderwidth=2, font=("System", 9),
                               command=lambda: self.createProfileFrame(self.client.currentUser, is_current_user=True))
        profileBtn.pack(side="right", pady=2, padx=2)

        # frame para el entry de buscar
        searchBoxFrame = tk.Frame(searchFrame, bg="#c0c0c0", relief="sunken", borderwidth=2)
        searchBoxFrame.pack(fill="x", padx=10, pady=10)

        # espacio de buscar
        tk.Label(searchBoxFrame, text="Enter username:", bg="#c0c0c0", font=("System", 9), anchor="w").pack(fill="x", padx=5, pady=(5, 0))
        self.searchEntry = tk.Entry(searchBoxFrame, relief="sunken", bg="white", font=("System", 9), borderwidth=2)
        self.searchEntry.pack(fill="x", padx=5, pady=5)

        # boton de buscar
        searchButton = tk.Button(searchBoxFrame, text="Search", relief="raised", bg="#c0c0c0",
                                 activebackground="#d4d0c8", borderwidth=2, font=("System", 9), command=self.search)
        searchButton.pack(pady=(0, 5))

        # para mostrar resultados
        self.resultsFrame = tk.Frame(searchFrame, bg="#c0c0c0", relief="sunken", borderwidth=2)
        self.resultsFrame.pack(expand=True, fill="both", padx=10, pady=(0, 10))

    def search(self):  # funcion para buscar personas
        searchTerm = self.searchEntry.get()

        if not searchTerm:
            self.showMessage("Please enter a search term", isError=True)
            return

        try:
            self.client.connectToServer()
            results = self.client.searchUsers(searchTerm)

            for widget in self.resultsFrame.winfo_children():
                widget.destroy()

            if not results:
                self.showMessage("No users found", isError=True)
            else:
                for user in results:  # crea un frame para cada ususario encontrado
                    userFrame = tk.Frame(self.resultsFrame, bg="#c0c0c0", relief="sunken", borderwidth=1)
                    userFrame.pack(fill="x", padx=5, pady=2)

                    # muestra la info del usario buscado
                    tk.Label(userFrame, text=f"{user['nombre']} {user['apellido']}", bg="#c0c0c0",
                             font=("System", 8), anchor="w").pack(side="left", padx=5, pady=2)

                    # frame para el boton de perfil de los usuarios
                    buttonFrame = tk.Frame(userFrame, bg="#c0c0c0")
                    buttonFrame.pack(side="right", padx=2)

                    # boton de ver perfil
                    tk.Button(buttonFrame, text="👤", font=("Arial", 10), relief="raised", bg="#c0c0c0", width=2,
                              command=lambda u=user['username']: self.createProfileFrame(u)).pack(side="right", padx=2,
                                                                                                  pady=2)

                    # boton de añadir amigo
                    if user['username'] != self.client.currentUser:
                        buttonText = self.getFriendshipButtonText(user['username'])
                        friendButton = tk.Button(buttonFrame, text=buttonText, font=("Arial", 10), relief="raised",
                                                 bg="#c0c0c0", width=2,
                                                 command=lambda u=user['username']: self.toggleFriendship(u))
                        friendButton.pack(side='right', padx=2)

        except Exception:
            self.showMessage("Unable to retrieve user data. Please try again", isError=True)

    def toggleFriendship(self, username):  # verifica si son amigos para eliminar o añadir
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
                result = self.client.removeFriend(currentUser, username)  # si son amigos entonces "eliminar amigo"
            else:
                result = self.client.addFriend(currentUser, username)  # sino "añadir amigo"

            if result['status'] == 'success':
                self.showMessage(result['message'])
                self.search()  # actualizar la vista
            else:
                self.showMessage(result['message'], isError=True)

        except Exception as e:
            self.showMessage(str(e), isError=True)

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
                return "-"
            else:
                return "+"
        except Exception as e:
            print(f"Error verificando amistad: {e}")
            return "+"

    def start(self):
        self.window.mainloop()