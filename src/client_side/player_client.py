import socket
import json
from src.entities.entity import Entity
from loguru import logger 
from src.maps import Maps

class PlayerClient:
    def __init__(self, ip='127.0.0.1', port=65432, debug=False):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the client side 
        self.conn.connect((ip, port)) # connect to the server
        self.debug = debug 
        self.position = [400, 300] # position of the player
        self.player_id = None # id of the player
        self.player_uuid = None # uuid of the player
        self.players = {} # list of players
        self.maps = Maps() # maps object
        self.player = None # player class object
        self.speed = 200 # speed of the player (200 pixels per second)
        logger.info(f"Connected to server at {ip}:{port}")

    def send_position(self):
        message = f"POSITION {int(self.position[0])} {int(self.position[1])} {self.player.anim_current_action} {self.player.anim_current_direction};"
        self.conn.sendall(message.encode()) # send the message to the server

    def receive_updates(self):
        # receive the updates from the server
        buffer = ""
        while True:
            try:
                data = self.conn.recv(4096).decode()
                if not data:
                    logger.info("No more data received from server.")
                    break
                buffer += data

                while ";" in buffer:
                    message, buffer = buffer.split(";", 1)
                    self.handle_data(message) # handle the data received
            except Exception as e:
                logger.error(f"Error receiving updates: {e}")
                break

    def handle_data(self, data):
        messages = data.split(";")
        for message in messages:
            if message.startswith("ID"): 
                _, player_id, player_uuid, player_asset_path, player_type = message.split()
                self.player_id = int(player_id)
                self.player_uuid = player_uuid
                self.player = Entity(
                    id=self.player_id,
                    name="Player",
                    uuid=self.player_uuid,
                    position=self.position,
                    asset_path=player_asset_path,
                    type=int(player_type),
                    render=True,
                    debug=self.debug
                )
                self.players[self.player_id] = self.player
                logger.info(f"Received ID: {self.player_id}, UUID: {self.player_uuid}")
            elif message.startswith("ENTITIES"):
                _, entities_data = message.split(" ", 1)
                try:
                    entities_data = json.loads(entities_data)
                    for p in entities_data:
                        if p['id'] != self.player_id:
                            if p['id'] in self.players:
                                player = self.players[p['id']]
                                if 'x' in p['state'] and 'y' in p['state']:
                                    player.update_position(
                                        (p['state']['x'], p['state']['y']), p['anim_current_action'], p['anim_current_direction'])
                            else:
                                self.players[p['id']] = Entity(
                                    id=p['id'],
                                    name="Player",
                                    uuid=p['uuid'],
                                    position=(p['state']['x'], p['state']['y']),
                                    asset_path=p['asset_path'],
                                    type=1,
                                    render=True,
                                    debug=self.debug)
                        self.players[p['id']].hp = p['hp']
                        self.players[p['id']].name = p['name']
                        self.players[p['id']].type = p['type']
                        self.players[p['id']].uuid = p['uuid']
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
            elif message.startswith("MAPS"):
                _, maps_data = message.split(" ", 1)
                try:
                    self.maps.update_maps(json.loads(maps_data))
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")
                except ValueError as e:
                    logger.error(f"Value error: {e}")
            elif message.startswith("DISCONNECT"):
                _, player_id = message.split()
                if int(player_id) in self.players:
                    del self.players[int(player_id)]
                    logger.info(f"Player {player_id} disconnected")

    def close(self):
        self.conn.close()
        logger.info("Connection closed")
