import socket
import json
from src.entities.entity import Entity
from loguru import logger


class PlayerClient:
    def __init__(self, ip='127.0.0.1', port=65432):
        """
        class that represents a player client in the game. 
        """
        self.conn = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # socket creation
        self.conn.connect((ip, port))  # connection to the server
        self.position = [400, 300]  # initial position of the player in the map
        self.player_id = None  # player id will be assigned by the server
        self.player_uuid = None  # player uuid will be assigned by the server
        # players in the game (list of Player objects) fetched by handle_data
        self.players = {}
        self.player = None
        self.speed = 200  # speed of the player in pixels per second for the movement

    def send_position(self):
        """
        sends the position of the player to the server.
        """
        message = f"POSITION {int(self.position[0])} {int(self.position[1])} {self.player.anim_current_action} {self.player.anim_current_direction};"
        self.conn.sendall(message.encode())

    def receive_updates(self):
        buffer = ""
        while True:
            try:
                data = self.conn.recv(4096).decode()
                if not data:
                    break
                buffer += data

                while ";" in buffer:
                    message, buffer = buffer.split(";", 1)
                    self.handle_data(message)
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def handle_data(self, data):
        """
        manages the data received from the server. 
        """
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
                    render=True
                )
                self.players[self.player_id] = self.player
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
                                    position=(p['state']['x'],
                                              p['state']['y']),
                                    asset_path=p['asset_path'],
                                    type=1,
                                    render=True)

                        self.players[p['id']].hp = p['hp']
                        self.players[p['id']].name = p['name']
                        self.players[p['id']].type = p['type']
                        self.players[p['id']].uuid = p['uuid']
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
            elif message.startswith("DISCONNECT"):
                _, player_id = message.split()
                if int(player_id) in self.players:
                    del self.players[int(player_id)]

    def close(self):
        """
        kill the connection between client and the server.
        """
        self.conn.close()
