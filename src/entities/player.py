from src.entities.entity import Entity

class Player:
    def __init__(self, player_id, player_uuid, position):
        self.entity = Entity(id=player_id, uuid=player_uuid,
                             name="Joueur",
                             position=position, asset_path="assets/dev.png",
                             type=1)
