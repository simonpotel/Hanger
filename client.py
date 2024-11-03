import argparse
from src.client_side.game_client import GameClient
from loguru import logger

def main():
    parser = argparse.ArgumentParser(description='Client Application')
    parser.add_argument('--debug', action='store_true', help='Activer le mode debug')
    args = parser.parse_args()

    window_game_size = (1280, 720)

    if args.debug:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level="DEBUG", colorize=True)
        logger.debug("DEBUG MODE")
        window_game_size = (500, 500)
    else:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level="INFO", colorize=True)
        logger.info("PRODUCTION MODE")


    logger.info("Starting the game client")
    try:
        game_client = GameClient(
            width=window_game_size[0], # window size
            height=window_game_size[1], # window size
            config_path='configs/host.json', # path to the config file configs/host.json
            logo_path='assets/custom/vh.png') # logo of the game
        logger.debug("GameClient initialized with width=1280, height=720, config_path='configs/host.json', logo_path='assets/custom/vh.png'")
        game_client.run() # run the game
        logger.info("Game client is running")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.debug(f"Exception details: {e}")

if __name__ == "__main__":
    main()