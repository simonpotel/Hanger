import socket
import threading
import json
import time
from src.server_side.client_manager import ClientManager

class GameServer:
    def __init__(self, config_path, update_interval):
        self.update_interval = update_interval # updates intervals between the server and the clients
        self.monsters = {} # list of monsters
        self.clients = {} # list of clients 
        self.lock = threading.Lock() # lock to avoid multiple threads to access the same data
        self.next_entity_id = 1 # id of the next entity

        with open(config_path, 'r') as config_file:
            config = json.load(config_file) # load the config file
            self.ip = config.get('ip')
            self.port = config.get('port') 

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the server side using TCP
        server_socket.bind((self.ip, self.port)) # bind the socket to the ip and port
        server_socket.listen(20) # listen to the clients (20 clients max)

        threading.Thread(target=self.broadcast, daemon=True).start() # start the thread to broadcast the data to the clients

        while True: # while the server is running 
            # accept the connection from the clients and start a new thread to handle the clients
            # 1 client = 1 thread
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, conn, addr):
        # this function is used to handle a client connnection
        # it will create a new client manager for the client and add it to the list of clients
        # it will also handle the data received from the client
        # and remove the client from the list of clients if the client disconnects
        
        client_id = self.next_entity_id # get the id of the client
        self.next_entity_id += 1 # increment the id of the next entity
        client = ClientManager(conn, addr, client_id) # create a new client manager for the client

        initial_message = f"ID {client_id} {client.entity.uuid} {client.entity.asset_path} {client.entity.type};"
        conn.sendall(initial_message.encode()) # send the initial message to the client (it will be used by client to define the player)

        with self.lock:
            self.clients[client_id] = client

        buffer = ""
        while True: # while the client is connected
            try:
                data = conn.recv(1024).decode() # receive the data from the client
                if not data:
                    break
                buffer += data
                # we use a buffer here to avoid the loss of data if the message is too long
                # with TCP, the message can be cut in multiple parts
                while ";" in buffer: 
                    message, buffer = buffer.split(";", 1)
                    # POSITION is used to update the position of the player when he is moving
                    if message.startswith("POSITION"):
                        _, x, y, anim_current_action, anim_current_direction = message.split() # seperate the data from the message
                        with self.lock:
                            client.entity.state['x'] = int(x) # update the x position of the player
                            client.entity.state['y'] = int(y) # update the y position of the player
                            client.entity.anim_current_action = anim_current_action # update the current action of the player
                            client.entity.anim_current_direction = anim_current_direction # update the current direction of the player
            except Exception:
                break

        self.remove_client(client) # remove the client from the list of clients if the client disconnects
        conn.close() # close the connection with the client

    def broadcast(self):
        # this function is used to broadcast the data to the clients (players)
        while True:
            entities_data = [] # list of entities data
            clients_data = [{'id': p.entity.id, 'uuid': p.entity.uuid, 'state': p.entity.state, 'type': p.entity.type, 'name': p.entity.name, 'hp': p.entity.hp, 'asset_path': p.entity.asset_path, 'anim_current_action': p.entity.anim_current_action, 'anim_current_direction': p.entity.anim_current_direction}
                            for p in self.clients.values()]

            monsters_data = [{'id': e.entity.id, 'uuid': e.entity.uuid, 'state': e.entity.state, 'type': e.entity.type, 'name': e.entity.name, 'hp': e.entity.hp, 'asset_path': e.entity.asset_path, 'anim_current_action': e.entity.anim_current_action, 'anim_current_direction': e.entity.anim_current_direction}
                             for e in self.monsters.values()]
            entities_data.extend(clients_data)
            entities_data.extend(monsters_data)
            
            message = f"ENTITIES {json.dumps(entities_data)};" # create the message to send to the clients
            for client in self.clients.values(): # send the message to all the clients
                try:
                    client.conn.sendall(message.encode())
                except Exception:
                    self.remove_client(client)
            time.sleep(self.update_interval)

    def remove_client(self, client):
        # this function is used to remove a client from the list of clients if the client disconnects
        # or for other reasons
        with self.lock:
            if client.entity.id in self.clients:
                del self.clients[client.entity.id]
        client.conn.close()
        disconnect_message = f"DISCONNECT {client.entity.id};" # send a message to the client to inform him that he is disconnected
        for p in self.clients.values(): # send the message to all the clients
            try:
                p.conn.sendall(disconnect_message.encode())
            except Exception:
                pass
