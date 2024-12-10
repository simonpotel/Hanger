import socket
import threading
import json
import time
from src.server_side.client_manager import ClientManager
from src.maps import Maps, maps_load_config, maps_update_required
from loguru import logger

class GameServer:
    def __init__(self, config_path, update_interval):
        self.update_interval = update_interval # updates intervals between the server and the clients
        self.monsters = {} # list of monsters
        self.clients = {} # list of clients 
        self.maps = Maps()
        maps_load_config(self.maps)
        self.lock = threading.Lock() # lock to avoid multiple threads to access the same data
        self.next_entity_id = 1 # id of the next entity

        with open(config_path, 'r') as config_file:
            config = json.load(config_file) # load the config file
            self.ip = config.get('ip')
            self.port = config.get('port') 

        logger.info(f"GameServer initialized with IP: {self.ip} and Port: {self.port}")

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the server side using TCP
        server_socket.bind((self.ip, self.port)) # bind the socket to the ip and port
        server_socket.listen(20) # listen to the clients (20 clients max)

        logger.info("Server started and listening for connections")

        threading.Thread(target=self.broadcast_entities, daemon=True).start() # start the thread to broadcast the data to the clients
        threading.Thread(target=self.broadcast_maps, daemon=True).start() # start the thread to broadcast the data to the clients

        while True: # while the server is running 
            client_socket, client_address = server_socket.accept()
            logger.info(f"Accepted connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, conn, addr):
        client_id = self.next_entity_id # get the id of the client
        self.next_entity_id += 1 # increment the id of the next entity
        client = ClientManager(conn, addr, client_id) # create a new client manager for the client

        logger.info(f"Client {client_id} connected from {addr}")

        initial_message = f"ID {client_id} {client.entity.uuid} {client.entity.asset_path} {client.entity.type};"
        initial_message = initial_message + f"MAPS {json.dumps(self.maps.maps)};"
        conn.sendall(initial_message.encode()) # send the initial message to the client

        with self.lock:
            self.clients[client_id] = client

        buffer = ""
        while True: # while the client is connected
            try:
                data = conn.recv(4096).decode() # receive the data from the client
                if not data:
                    break
                buffer += data
                while ";" in buffer: 
                    message, buffer = buffer.split(";", 1)
                    if message.startswith("POSITION"):
                        _, x, y, anim_current_action, anim_current_direction = message.split() # separate the data from the message
                        with self.lock:
                            client.entity.state['x'] = int(x) # update the x position of the player
                            client.entity.state['y'] = int(y) # update the y position of the player
                            client.entity.anim_current_action = anim_current_action # update the current action of the player
                            client.entity.anim_current_direction = anim_current_direction # update the current direction of the player
                        logger.debug(f"Updated position for client {client_id}: x={x}, y={y}, action={anim_current_action}, direction={anim_current_direction}")
                    elif message.startswith("ATTACK"):
                        _, attack_type = message.split()
                        client.entity.attack_type = int(attack_type)
                        with self.lock:
                            if client.entity.attack_type == 1:
                                for other_client in self.clients.values():
                                    if client.entity.anim_current_direction == 'up' and (abs(other_client.entity.state['x'] - client.entity.state['x']) <= 32 and
                                        other_client.entity.state['y'] < client.entity.state['y'] and abs(other_client.entity.state['y'] - client.entity.state['y']) <= 32):
                                        other_client.entity.hp -= 10
                                        logger.debug(f"Entity {other_client.entity.id} took damage from client {client_id}. New HP: {other_client.entity.hp}")
                                    elif client.entity.anim_current_direction == 'down' and (abs(other_client.entity.state['x'] - client.entity.state['x']) <= 32 and
                                        other_client.entity.state['y'] > client.entity.state['y'] and abs(other_client.entity.state['y'] - client.entity.state['y']) <= 32):
                                        other_client.entity.hp -= 10
                                        logger.debug(f"Entity {other_client.entity.id} took damage from client {client_id}. New HP: {other_client.entity.hp}")
                                    elif client.entity.anim_current_direction == 'left' and (abs(other_client.entity.state['y'] - client.entity.state['y']) <= 32 and
                                        other_client.entity.state['x'] < client.entity.state['x'] and abs(other_client.entity.state['x'] - client.entity.state['x']) <= 32):
                                        other_client.entity.hp -= 10
                                        logger.debug(f"Entity {other_client.entity.id} took damage from client {client_id}. New HP: {other_client.entity.hp}")
                                    elif client.entity.anim_current_direction == 'right' and (abs(other_client.entity.state['y'] - client.entity.state['y']) <= 32 and
                                        other_client.entity.state['x'] > client.entity.state['x'] and abs(other_client.entity.state['x'] - client.entity.state['x']) <= 32):
                                        other_client.entity.hp -= 10
                                        logger.debug(f"Entity {other_client.entity.id} took damage from client {client_id}. New HP: {other_client.entity.hp}")
                                
                            #elif client.entity.attack_type == 2:
            except Exception as e:
                logger.error(f"Error handling client {client_id}: {e}")
                break

        self.remove_client(client) # remove the client from the list of clients if the client disconnects
        conn.close() # close the connection with the client
        logger.info(f"Client {client_id} disconnected")

    def broadcast_entities(self):
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
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client.entity.id}: {e}")
                    self.remove_client(client)
            time.sleep(self.update_interval)

    def broadcast_maps(self):
        while True:
            if maps_update_required(self.maps):
                maps_load_config(self.maps)
                message = f"MAPS {json.dumps(self.maps.maps)};"
                for client in self.clients.values():
                    try:
                        client.conn.sendall(message.encode())
                    except Exception as e:
                        logger.error(f"Error broadcasting maps to client {client.entity.id}: {e}")
                        self.remove_client(client)

    def remove_client(self, client):
        with self.lock:
            if client.entity.id in self.clients:
                del self.clients[client.entity.id]
        client.conn.close()
        disconnect_message = f"DISCONNECT {client.entity.id};" # send a message to the client to inform him that he is disconnected
        for p in self.clients.values(): # send the message to all the clients
            try:
                p.conn.sendall(disconnect_message.encode())
            except Exception as e:
                logger.error(f"Error sending disconnect message to client {p.entity.id}: {e}")
        logger.info(f"Client {client.entity.id} removed")
