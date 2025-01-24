from utils.network import NetworkManager
from utils.auth import AuthManager

class ClientApplication:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.auth_manager = AuthManager()

def main():
    client = ClientApplication()

if __name__ == "__main__":
    main()