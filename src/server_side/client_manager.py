from src.entities.entity import Entity
import uuid
from loguru import logger

class ClientManager:
    def __init__(self, conn, addr, client_id):
        self.conn = conn # connection object with the client
        self.addr = addr # address of the client
        logger.info(f"Initializing ClientManager for client {client_id} at address {addr}")
        
        try:
            self.entity = Entity(
                id=client_id,
                name=f"Player {client_id}",
                uuid=str(uuid.uuid4()),
                position=[400, 300],
                asset_path="player_skin_1",
                type=1, render=False, debug=False) # create a new entity for the client (but not render it)
            logger.info(f"Entity created for client {client_id} with UUID {self.entity.uuid}")
        except Exception as e:
            logger.error(f"Failed to create entity for client {client_id}: {e}")
