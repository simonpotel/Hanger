from src.entities.entity import Entity
import uuid

class ClientManager:
    def __init__(self, conn, addr, client_id):
        self.conn = conn # connection object with the client
        self.addr = addr # address of the client
        self.entity = Entity(
            id=client_id,
            name=f"Player {client_id}",
            uuid=str(uuid.uuid4()),
            position=[400, 300],
            asset_path="player_skin_1",
            type=1, render=False) # create a new entity for the client (but not render it)
