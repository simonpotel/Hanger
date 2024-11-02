from src.client_side.game_client import GameClient

if __name__ == "__main__":
    game_client = GameClient(
        width=1280, # window size
        height=720, # window size
        config_path='configs/host.json', # path to the config file configs/host.json
        logo_path='assets/custom/vh.png') # logo of the game
    game_client.run() # run the game
