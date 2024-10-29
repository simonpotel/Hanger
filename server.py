from server_side.game_server import GameServer

game_server = GameServer(
    config_path='configs/host.json', update_interval=0.025)
game_server.start_server()
