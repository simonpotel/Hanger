import socket
import json
from src.entities.entity import Entity

class PlayerClient:
    def __init__(self, ip='127.0.0.1', port=65432):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object for the client side 
        self.conn.connect((ip, port)) # connect to the server
        self.position = [400, 300] # position of the player
        self.player_id = None # id of the player
        self.player_uuid = None # uuid of the player
        self.players = {} # list of players
        self.player = None # player class object
        self.speed = 200 # speed of the player (200 pixels per second)

    def send_position(self):
        message = f"POSITION {int(self.position[0])} {int(self.position[1])} {self.player.anim_current_action} {self.player.anim_current_direction};"
        self.conn.sendall(message.encode()) # send the message to the server

    def receive_updates(self):
        # receive the updates from the server
        buffer = ""
        while True:
            try:
                # implemented the buffer to avoid the loss of data if the message is too long
                # with TCP, the message can be cut in multiple parts
                data = self.conn.recv(4096).decode()
                if not data:
                    break
                buffer += data

                while ";" in buffer:
                    message, buffer = buffer.split(";", 1)
                    self.handle_data(message) # handle the data received
            except Exception:
                break

    def handle_data(self, data):
        messages = data.split(";")
        for message in messages:
            # ID is used when you connect to the server to get your id, uuid, asset path and type
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
                    render=True
                )
                self.players[self.player_id] = self.player
            # ENTITIES is used to update the position of the entities (players for now)
            elif message.startswith("ENTITIES"):
                _, entities_data = message.split(" ", 1)
                try:
                    entities_data = json.loads(entities_data)
                    for p in entities_data:
                        if p['id'] != self.player_id:
                            # update the position of the player if the player is in the list
                            if p['id'] in self.players:
                                player = self.players[p['id']]
                                if 'x' in p['state'] and 'y' in p['state']:
                                    player.update_position(
                                        (p['state']['x'], p['state']['y']), p['anim_current_action'], p['anim_current_direction'])
                            else:
                                # create a new player if the player is not in the list
                                self.players[p['id']] = Entity(
                                    id=p['id'],
                                    name="Player",
                                    uuid=p['uuid'],
                                    position=(p['state']['x'], p['state']['y']),
                                    asset_path=p['asset_path'],
                                    type=1,
                                    render=True)

                        self.players[p['id']].hp = p['hp']
                        self.players[p['id']].name = p['name']
                        self.players[p['id']].type = p['type']
                        self.players[p['id']].uuid = p['uuid']
                except json.JSONDecodeError:
                    pass
            # DISCONNECT is used to remove the player from the list if the player disconnect
            elif message.startswith("DISCONNECT"):
                _, player_id = message.split()
                if int(player_id) in self.players:
                    del self.players[int(player_id)]

    def close(self):
        self.conn.close()
