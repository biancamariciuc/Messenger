import socket
import threading
import uuid
import json
from common.config import SERVER_HOST, SERVER_PORT, FORMAT, print_log
from login_handler import handle_login
from helper_functions.users import get_users
from helper_functions.users import search_socket_user


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

                    if msg == "GET_USERS":
                        users_list = get_users()
                        data_str = json.dumps(users_list)
                        client_socket.send(f"LIST_USERS:{data_str}".encode(FORMAT))
                    elif msg.startswith("SEND_MSG:"):
                        json_data = msg.replace("SEND_MSG:", "")
                        data = json.loads(json_data)

                        receiver_user = data["receiver"]
                        message_content = data["content"]

                        receiver_socket = search_socket_user(receiver_user, self.clients)

                        if receiver_socket:
                            format = {
                                "sender": username,
                                "content": message_content
                            }
                            receiver_socket.send(f"RECEIVE_MSG:{json.dumps(format)}".encode(FORMAT))
                        else:
                            print_log("Server", "User (receiver) not found!")
                    else :
                        print_log("Server", "Unknown command!")


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