import json
from src.client_side.render.animation import Animation
import os
from loguru import logger

class Maps():
    def __init__(self):
        self.maps = {}
        self.maps_animations = {}

    def get_map(self, map_name):
        return self.maps.get(map_name, None)  # get the map by name with default None

    def update_maps(self, maps):
        self.maps = maps
        for map_name, assets in maps.items():
            if map_name not in self.maps_animations:
                self.maps_animations[map_name] = {}
                
            for asset, properties in assets.items():
                if asset not in self.maps_animations[map_name]:
                    self.maps_animations[map_name][asset] = Animation(
                        asset_path=properties.get('asset_path', ''),
                        frame_width=properties.get('width', 0),
                        frame_height=properties.get('height', 0),
                        scale_factor=properties.get('scale_factor', 1)
                    )
                else:
                    self.maps_animations[map_name][asset].frame_width = properties.get('width', 0)
                    self.maps_animations[map_name][asset].frame_height = properties.get('height', 0)
                    
            for asset in list(self.maps_animations[map_name].keys()):
                if asset not in assets:
                    del self.maps_animations[map_name][asset]

def maps_update_required(maps):
    if not maps.maps:
        return True
    else:
        for map_name in maps.maps.keys():
            if os.path.exists(f"src/maps/new_{map_name}.json"):
                return True
    return False

def maps_load_config(maps):
    maps_config = maps_get_config(maps)
    maps.maps = maps_config

def maps_get_config(maps):
    maps_name = ['world']
    maps_dic = {}
    for map_name in maps_name:
        new_map_path = f"src/maps/new_{map_name}.json"
        if os.path.exists(new_map_path):
            try:
                with open(new_map_path, 'r') as new_maps_file:
                    maps_dic[map_name] = json.load(new_maps_file)
                os.replace(new_map_path, f"src/maps/{map_name}.json")
            except Exception as e:
                logger.error(f"Error receiving updates: {e}")
                logger.debug(f"Exception details: {e}")
        else:
            try:
                with open(f"src/maps/{map_name}.json", 'r') as maps_file:
                    maps_dic[map_name] = json.load(maps_file)
            except Exception as e:
                logger.error(f"Error receiving updates: {e}")
                logger.debug(f"Exception details: {e}")
    return maps_dic
