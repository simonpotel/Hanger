from src.entities.entity import Entity

class Monster:
    def __init__(self, monster_id, monster_uuid, name, position, asset_path):
        self.entity = Entity(id=monster_id, uuid=monster_uuid,
                             name=name,
                             position=position, asset_path=asset_path,
                             type=2)