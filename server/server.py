import socket
import threading
import uuid
from common.config import SERVER_HOST, SERVER_PORT, FORMAT, print_log
from loggin_client import handle_login


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen()
            self.running = True

            print_log("Server", f"Running on {self.host}:{self.port}")
            print_log("Server", "Waiting for connections...")

            while self.running:
                # accept blocheaza executia pana un client de connecteaza
                # address = adressa IP si portul
                client_socket, address = self.server_socket.accept()

                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()

                #conctine si threadul prinicipal de aia se scade -1
                print_log("Server", f"Active connections: {threading.active_count() - 1}")

        except Exception as e:
            print_log("Server error", str(e))

    def handle_client(self, client_socket, address):
        try:
            client_id = str(uuid.uuid4())[:8]
            username = client_socket.recv(1024).decode(FORMAT)

            handle_login(username)

            self.clients[client_socket] = username

            print_log("Connection", f"New connection from {address} assigned ID: {client_id} and the username: {username}")
            connected = True
            while connected:
                try:
                    msg = client_socket.recv(1024).decode(FORMAT)

                    if not msg:
                        connected = False
                        break

                    print_log("Message", f"[{username}]: {msg}")

                except:
                    connected = False
                    break
        except Exception as e:
            print_log("Error", f"Error in connection: {e}")
            client_socket.close()
        finally:
            client_socket.close()
            if client_socket in self.clients:
                del self.clients[client_socket]
            print_log("Disconnect", f"{username} has disconnected.")


if __name__ == "__main__":
    server = Server(SERVER_HOST, SERVER_PORT)
    server.start()