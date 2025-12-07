import socket
from common.config import SERVER_HOST, SERVER_PORT, FORMAT, print_log


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            # IPv4, tcp connection
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            message = self.client_socket.recv(1024).decode(FORMAT)
            print_log("Client", f"Server: {message}")

            input("Press Enter to exit...")

        except ConnectionRefusedError:
            print_log("Client error", "server is running?")
        except Exception as e:
            print_log("Client error", str(e))


if __name__ == "__main__":
    client = Client(SERVER_HOST, SERVER_PORT)
    client.connect()