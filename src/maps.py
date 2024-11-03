import json
from src.client_side.render.animation import Animation

class Maps():
    def __init__(self):
        self.maps = {}
        self.maps_animations = {}

    def get_map(self, map_name):
        return self.maps.get(map_name)  # get the map by name

    def update_maps(self, maps):
        self.maps = maps
        for map_name, assets in maps.items():
            if map_name not in self.maps_animations:
                self.maps_animations[map_name] = {}
                
            for asset, properties in assets.items():
                if asset not in self.maps_animations[map_name]:
                    self.maps_animations[map_name][asset] = Animation(asset_path=properties['asset_path'], frame_width=properties['width'], frame_height=properties['height'], scale_factor=1)
                else:
                    self.maps_animations[map_name][asset].frame_width = properties['width']
                    self.maps_animations[map_name][asset].frame_height = properties['height']
                    
            for asset in list(self.maps_animations[map_name].keys()):
                if asset not in assets:
                    del self.maps_animations[map_name][asset]

def maps_update_required(maps):
    return maps_get_config(maps) != maps.maps

def maps_load_config(maps):
    maps_config = maps_get_config(maps)
    maps.maps = maps_config

def maps_get_config(maps):
    maps_name = ['world']
    maps_dic = {}
    for map_name in maps_name:
        with open(f"src/maps/{map_name}.json", 'r') as maps_file:
            maps_dic[map_name] = json.load(maps_file)
    return maps_dic