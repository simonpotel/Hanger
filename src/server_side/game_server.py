import socket
import threading
import json
import time
from src.server_side.client_manager import ClientManager

class GameServer:
    def __init__(self, config_path, update_interval):
        self.update_interval = update_interval
        self.monsters = {}
        self.clients = {}
        self.lock = threading.Lock()
        self.next_entity_id = 1

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            self.ip = config.get('ip')
            self.port = config.get('port')

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(10)

        threading.Thread(target=self.broadcast, daemon=True).start()

        while True:
            client_socket, client_address = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def handle_client(self, conn, addr):
        client_id = self.next_entity_id
        self.next_entity_id += 1
        client = ClientManager(conn, addr, client_id)

        initial_message = f"ID {client_id} {client.entity.uuid} {client.entity.asset_path} {client.entity.type};"
        conn.sendall(initial_message.encode())

        with self.lock:
            self.clients[client_id] = client

        buffer = ""
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                buffer += data
                while ";" in buffer:
                    message, buffer = buffer.split(";", 1)
                    if message.startswith("POSITION"):
                        _, x, y, anim_current_action, anim_current_direction = message.split()
                        with self.lock:
                            client.entity.state['x'] = int(x)
                            client.entity.state['y'] = int(y)
                            client.entity.anim_current_action = anim_current_action
                            client.entity.anim_current_direction = anim_current_direction
            except Exception:
                break

        self.remove_client(client)
        conn.close()

    def broadcast(self):
        while True:
            entities_data = []
            clients_data = [{'id': p.entity.id, 'uuid': p.entity.uuid, 'state': p.entity.state, 'type': p.entity.type, 'name': p.entity.name, 'hp': p.entity.hp, 'asset_path': p.entity.asset_path, 'anim_current_action': p.entity.anim_current_action, 'anim_current_direction': p.entity.anim_current_direction}
                            for p in self.clients.values()]

            monsters_data = [{'id': e.entity.id, 'uuid': e.entity.uuid, 'state': e.entity.state, 'type': e.entity.type, 'name': e.entity.name, 'hp': e.entity.hp, 'asset_path': e.entity.asset_path, 'anim_current_action': e.entity.anim_current_action, 'anim_current_direction': e.entity.anim_current_direction}
                             for e in self.monsters.values()]
            entities_data.extend(clients_data)
            entities_data.extend(monsters_data)
            message = f"ENTITIES {json.dumps(entities_data)};"
            for client in self.clients.values():
                try:
                    client.conn.sendall(message.encode())
                except Exception:
                    self.remove_client(client)
            time.sleep(self.update_interval)

    def remove_client(self, client):
        with self.lock:
            if client.entity.id in self.clients:
                del self.clients[client.entity.id]
        client.conn.close()
        disconnect_message = f"DISCONNECT {client.entity.id};"
        for p in self.clients.values():
            try:
                p.conn.sendall(disconnect_message.encode())
            except Exception:
                pass
