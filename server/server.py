import socket
import threading
import uuid
from common.config import SERVER_HOST, SERVER_PORT, FORMAT, print_log
from helper_functions.users import *
from helper_functions.messages import *
from helper_functions.cryptoo import *


class Server:
    """
    The core class handling network connections and data management.

    This class listens for incoming connections, authenticates users, and
    routes encrypted messages between clients. It also manages data persistence
    by saving chat history and user public keys to disk.
    """
    def __init__(self, host, port):
        """
        Initialize the class Server and create the directory for storage the public keys

        Args:
            host (str):  (127.0.0.1)
            port (int): (5555)
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = {}
        self.running = False
        self.public_keys = {}
        if not os.path.exists("server_keys"):
            os.makedirs("server_keys")

    def start(self):
        """
        Start the server loop to accept incoming connections.

        Start a new thread for each connected client to handle communication concurrently.
        """
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
        """
        Handle the communication lifecycle for a specific connected client.

        Processes incoming commands (LOGIN, SEND_MSG, GET_USERS, etc.) and does
        the appropriate actions.

        Args:
            client_socket (socket): The active socket connection for the client.
            address (tuple): The (IP, Port) of the connected client.
        """
        try:
            client_id = str(uuid.uuid4())[:8]
            username = client_socket.recv(16384).decode(FORMAT)

            handle_login(username)

            self.clients[client_socket] = username


            print_log("Connection", f"New connection from {address} assigned ID: {client_id} and the username: {username}")
            connected = True
            while connected:
                try:
                    msg = client_socket.recv(16384).decode(FORMAT)

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
                        msg_for_them = data["msg_for_receiver"]
                        msg_for_me = data["msg_for_sender"]

                        log_message(username, receiver_user, msg_for_me, True)
                        log_message(receiver_user, username, msg_for_them, False)

                        receiver_socket = search_socket_user(receiver_user, self.clients)

                        if receiver_socket:
                            format = {
                                "sender": username,
                                "content": msg_for_them
                            }
                            receiver_socket.send(f"RECEIVE_MSG:{json.dumps(format)}".encode(FORMAT))
                        else:
                            print_log("Server", "User (receiver) not found!")
                    elif msg.startswith("GET_HISTORY:"):
                        json_data = msg.replace("GET_HISTORY:", "")
                        data = json.loads(json_data)
                        target_user = data["target"]

                        history = get_chat_history(username, target_user)

                        history_json = json.dumps(history)
                        client_socket.send(f"HISTORY:{history_json}".encode(FORMAT))
                    elif msg.startswith("PUB_KEY:"):
                        key = msg.replace("PUB_KEY:", "")
                        self.public_keys[username] = key
                        save_user_pub_key(username, key)
                    elif msg.startswith("GET_KEY:"):
                        target = msg.replace("GET_KEY:", "")
                        if target in self.public_keys:
                            key_to_send = self.public_keys[target]
                        else:
                            key_to_send = get_user_pub_key_from_disk(target)
                        if key_to_send:
                            resp = {"user": target, "key": key_to_send}
                            client_socket.send(f"KEY_RESPONSE:{json.dumps(resp)}".encode(FORMAT))
                    else :
                        print_log("Server", "Unknown command!")


                except Exception as e:
                    print(e)
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