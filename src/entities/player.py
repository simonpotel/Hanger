from src.entities.entity import Entity

class Player:
    def __init__(self, player_id, player_uuid, position, asset_path):
        self.entity = Entity(id=player_id, uuid=player_uuid,
                             name="Joueur",
                             position=position, asset_path=asset_path,
                             type=1)
