import argparse
from src.client_side.game_client import GameClient
from loguru import logger


def main():
    parser = argparse.ArgumentParser(description='Client Application')
    parser.add_argument('--debug', action='store_true',
                        help='Activate debug mode')
    parser.add_argument('--window', action='store_true',
                        help='Start the game in windowed mode')
    args = parser.parse_args()

    window_game_size = (1280, 720)

    if args.debug:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''),
                   level="DEBUG", colorize=True)
        logger.debug("DEBUG MODE")
        window_game_size = (800, 400)
    else:
        logger.remove()
        logger.add(lambda msg: print(msg, end=''), level="INFO", colorize=True)
        logger.info("PRODUCTION MODE")

    logger.info("Starting the game client")
    try:
        game_client = GameClient(
            width=window_game_size[0],  # window size
            height=window_game_size[1],  # window size
            config_path='configs/host.json',  # path to the config file configs/host.json
            logo_path='assets\Custom\perso.png',  # logo of the game
            windowed=args.window 
        )
        logger.debug(f"GameClient initialized with width={window_game_size[0]}, height={window_game_size[1]}, windowed={args.window}")
        game_client.run(debug=args.debug)  # run the game
        logger.info("Game client is running")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        logger.debug(f"Exception (game client) details: {e}")


if __name__ == "__main__":
    main()
