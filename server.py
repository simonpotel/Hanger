import argparse
from src.server_side.game_server import GameServer
from loguru import logger

def main():
    parser = argparse.ArgumentParser(description='Server Application')
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    args = parser.parse_args()

    if args.debug:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level="DEBUG", colorize=True)
        logger.debug("DEBUG MODE")
    else:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level="INFO", colorize=True)
        logger.info("PRODUCTION MODE")

    class ServerApp:
        def __init__(self, config_path, update_interval):
            self.config_path = config_path # configs/host.json
            self.update_interval = update_interval # 0.025 seconds
            self.game_server = None 
            logger.info(f"ServerApp initialized with config_path: {config_path} and update_interval: {update_interval}")
            logger.debug(f"ServerApp __init__ called with config_path={config_path}, update_interval={update_interval}")

        def start_server(self):
            try:
                logger.info("Starting the game server...")
                self.game_server = GameServer(
                    config_path=self.config_path, update_interval=self.update_interval) # create a new GameServer instance
                self.game_server.start_server() # restart the server if it crashes
                logger.info("Game server started successfully.")
            except Exception as e:
                logger.error(f"Failed to start the game server: {e}")
                logger.debug(f"Exception details: {e}")

    logger.info("Initializing ServerApp...")
    server_app = ServerApp( 
        config_path='configs/host.json', update_interval=0.025) # create a new ServerApp instance
    logger.debug("ServerApp instance created")
    server_app.start_server() # start the server

if __name__ == "__main__":
    main()