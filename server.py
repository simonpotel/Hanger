from src.server_side.game_server import GameServer


class ServerApp:
    def __init__(self, config_path, update_interval):
        self.config_path = config_path
        self.update_interval = update_interval
        self.game_server = None

    def start_server(self):
        self.game_server = GameServer(
            config_path=self.config_path, update_interval=self.update_interval)
        self.game_server.start_server()


if __name__ == "__main__":
    server_app = ServerApp(
        config_path='configs/host.json', update_interval=0.025)
    server_app.start_server()
