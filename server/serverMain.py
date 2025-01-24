from utils.network import NetworkManager
from utils.auth import AuthManager

class SocialGraph:
    def __init__(self):
        pass

class ServerApplication:
    def __init__(self):
        self.network_manager = NetworkManager()
        self.auth_manager = AuthManager()
        self.social_graph = SocialGraph()

def main():
    server = ServerApplication()

if __name__ == "__main__":
    main()