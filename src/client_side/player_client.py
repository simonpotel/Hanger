import socket
import json
from src.entities.entity import Entity

class PlayerClient:
    def __init__(self, ip='127.0.0.1', port=65432):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((ip, port))
        self.position = [400, 300]
        self.player_id = None
        self.player_uuid = None
        self.players = {}
        self.player = None
        self.speed = 200

    def send_position(self):
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
            except Exception:
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
            elif message.startswith("DISCONNECT"):
                _, player_id = message.split()
                if int(player_id) in self.players:
                    del self.players[int(player_id)]

    def close(self):
        self.conn.close()
