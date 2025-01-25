import tkinter as tk
from tkinter import messagebox
from clientMain import ClientApplication

class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("SocialTec Client")
        self.window.geometry("300x400")
        self.window.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.client = ClientApplication(autoconnect = False)
        self.client = ClientApplication()
        self.createLoginFrame()

    def onClosing(self):
        self.window.destroy() # cerrar ventana principal

    def createLoginFrame(self): # crea el frame del login
        for widget in self.window.winfo_children(): # recorre todos los elementos y los borra
            widget.destroy()

        # frame del login
        loginFrame = tk.Frame(self.window)
        loginFrame.pack(expand = True, fill = "both")

        # titulo
        tk.Label(loginFrame, text = "Login").pack()

        # usuario
        tk.Label(loginFrame, text = "Usuario").pack()
        self.usernameEntry = tk.Entry(loginFrame, width = 25)
        self.usernameEntry.pack()

        # contraseña
        tk.Label(loginFrame, text="Contraseña").pack()
        self.passwordEntry = tk.Entry(loginFrame, width = 25)
        self.passwordEntry.pack()

        # boton de loguearse
        loginButton = tk.Button(loginFrame, text = "Login", command = self.login)
        loginButton.pack()

        # boton de registrarse
        registerButton = tk.Button(loginFrame, text="Registrarse", command = self.createRegisterFrame)
        registerButton.pack()

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

        # boton de registrarse
        register_btn = tk.Button(registerFrame, text = "Crear cuenta", command = self.register)
        register_btn.pack(pady=10)

        # boton de volver al login
        back_btn = tk.Button(registerFrame, text = "Volver al login", command = self.createLoginFrame)
        back_btn.pack()

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

        searchFrame = tk.Frame(self.window)
        searchFrame.pack(expand=True, fill='both')

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
                for user in results:
                    userFrame = tk.Frame(self.resultsFrame)
                    userFrame.pack(fill = 'x', pady = 5)
                    tk.Label(userFrame, text=f"{user['nombre']} {user['apellido']} (@{user['username']})").pack(side='left')
        except Exception:
            print("error")

    def start(self):
        self.window.mainloop()