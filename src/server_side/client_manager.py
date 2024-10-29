from src.entities.entity import Entity
import uuid


class ClientManager:
    def __init__(self, conn, addr, client_id):
        """
        class to represent a client in the game (a client connected to the server)
        """
        self.conn = conn  # connection object to communicate with the client
        self.addr = addr  # address of the client
        self.entity = Entity(id=client_id, uuid=str(uuid.uuid4(
        )), name="Joueur", position=(0, 0), asset_path="assets/dev.png", type=1)
