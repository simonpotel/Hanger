import uuid
import socket
import threading
import json
import time
from loguru import logger
from colorama import init, Fore
from common.entity import Entity
import uuid 

init(autoreset=True)

logger.add("logs/game_server.log",
           format="{time} {level} {message}", level="DEBUG")


class Client:
    def __init__(self, conn, addr, client_id):
        """
        class to represent a client in the game (a client connected to the server)
        """
        self.conn = conn  # connection object to communicate with the client
        self.addr = addr  # address of the client
        self.entity = Entity(id=client_id, uuid=str(uuid.uuid4(
        )), name="Joueur", position=(0, 0), asset_path="assets/dev.png", type=1)


class GameServer:
    def __init__(self, config_path, update_interval):
        # intervals in seconds between broadcast data to all clients
        self.update_interval = update_interval
        self.clients = {}  # stock clients object from class client
        # garrant on multi-threading that only one thread can access the shared resource at a time
        self.lock = threading.Lock()
        self.next_client_id = 1  # next client id to give to a new client

        # load the server configuration from a JSON file
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.ip = config.get('ip')
            self.port = config.get('port')

        logger.info(f"{Fore.GREEN}Server initialized with IP: {
                    self.ip}, Port: {self.port}")

    def start_server(self):
        """
        start the game server and listen for incoming connections from clients on the specified IP and port
        """
        # create a socket object IPV4 and TCP
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the ip and port specified in the configuration file
        server_socket.bind((self.ip, self.port))
        # listen for incoming connections with a maximum of 10 connections (prevent DDOS, etc)
        server_socket.listen(10)

        # start a thread to broadcast the positions of all clients
        logger.info(f"{Fore.GREEN}Server started and listening on {
                    self.ip}:{self.port}")

        threading.Thread(target=self.broadcast_positions, daemon=True).start()

        while True:  # loop to accept incoming connections
            # accept a new connection and start a new thread to handle it with the handle_client method
            # 1 client = 1 thread
            client_socket, client_address = server_socket.accept()
            logger.info(f"{Fore.BLUE}New connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(
                client_socket, client_address)).start()

    def handle_client(self, conn, addr):
        """
        handle a new client connection by creating a new client object and adding it to the list of clients
        this method will run in a separate thread for each client
        """
        client_id = self.next_client_id
        self.next_client_id += 1
        client = Client(conn, addr, client_id)

        initial_message = f"ID {client_id} {client.entity.uuid};"
        # everyone will receive that new client joined
        conn.sendall(initial_message.encode())

        with self.lock:
            self.clients[client_id] = client

        buffer = ""  # buffer to store incomplete messages
        while True:  # loop to receive data from the client
            try:
                data = conn.recv(1024).decode()  # receive data from the client
                # if no data is received, break the loop (client disconnected or something went wrong)
                if not data:
                    break
                buffer += data  # add the received data to the buffer
                while ";" in buffer:  # loop to handle all complete messages in the buffer
                    # split the buffer into the first complete message and the rest of the buffer
                    message, buffer = buffer.split(";", 1)
                    # if the message is a position update
                    if message.startswith("POSITION"):
                        _, x, y = message.split()
                        with self.lock:  # update the client's position
                            client.entity.state['x'] = int(x)
                            client.entity.state['y'] = int(y)
            except Exception as e:
                logger.error(f"{Fore.RED}Error handling client {addr}: {e}")
                break

        # remove the client from the list of clients
        self.remove_client(client)
        conn.close()  # close the connection between the server and the client

    def broadcast_positions(self):
        """
        method to broadcast the positions of all clients to all connected clients at regular intervals
        """
        while True:  # loop to broadcast positions
            positions = [{'id': p.entity.id, 'uuid': p.entity.uuid, 'state': p.entity.state}
                         # create a list of client positions
                         for p in self.clients.values()]
            # create a message with the positions
            message = f"POSITIONS {json.dumps(positions)};"
            for client in self.clients.values():  # send the message to all connected clients
                try:
                    # send the message to the client
                    client.conn.sendall(message.encode())
                except Exception as e:
                    logger.error(f"{Fore.RED}Error sending to client {
                                 client.entity.id}: {e}")
                    self.remove_client(client)
            # wait for the specified interval before broadcasting again (avoid flooding the network)
            time.sleep(self.update_interval)

    def remove_client(self, client):
        """
        method to remove a client from the list of clients and send a disconnect message to all connected clients
        """
        with self.lock:  # remove the client from the list of clients
            if client.entity.id in self.clients:
                del self.clients[client.entity.id]
        client.conn.close()  # close the connection between the server and the client
        logger.info(f"{Fore.BLUE}client {client.entity.id} disconnected")
        disconnect_message = f"DISCONNECT {
            client.entity.id};"  # create a disconnect message
        for p in self.clients.values():  # send the disconnect message to all connected clients
            try:
                # send the disconnect message to the client
                p.conn.sendall(disconnect_message.encode())
            except Exception as e:
                logger.error(
                    f"{Fore.RED}Error sending disconnect message to client {p.id}: {e}")
