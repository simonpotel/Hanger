from src.entities.entity import Entity
import uuid

class ClientManager:
    def __init__(self, conn, addr, client_id):
        self.conn = conn
        self.addr = addr
        self.entity = Entity(
            id=client_id,
            name=f"Player {client_id}",
            uuid=str(uuid.uuid4()),
            position=[400, 300],
            asset_path="player_skin_1",
            type=1, render=False)
