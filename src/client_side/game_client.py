import pygame
import json
import threading
from src.client_side.player_client import PlayerClient
from loguru import logger

class GameClient:
    def __init__(self, width, height, config_path, logo_path):
        self.width = width # window size
        self.height = height # window size
        self.config_path = config_path # path to the config file configs/host.json
        self.logo_path = logo_path # logo of the game
        self.screen = None # pygame screen obj
        self.font = None # pygame font obj
        self.client_logo = None # pygame image obj
        self.clock = None # pygame clock obj
        self.client = None # PlayerClient obj
        self.running = True 
        logger.info("GameClient initialized with width: {}, height: {}, config_path: {}, logo_path: {}", width, height, config_path, logo_path)

    def setup_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height)) # create the game window
        pygame.display.set_caption("Hungry Client DEV") # set the game window title
        logger.info("Screen setup with width: {}, height: {}", self.width, self.height)

    def load_assets(self):
        self.font = pygame.font.Font(None, 24) # load the font for the game
        self.client_logo = pygame.image.load(self.logo_path) # load the logo of the game
        pygame.display.set_icon(self.client_logo) # set the logo of the game    
        self.client_logo = pygame.transform.scale(self.client_logo, (128, 128)) # scale the logo if needed to 128x128
        logger.info("Assets loaded successfully")

    def read_config(self):
        # this will return the config of configs/host.json to relation between client - server
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info("Config read successfully from {}", self.config_path)
            return config.get('ip'), config.get('port') # return the ip and port of the server
        except Exception as e:
            logger.error("Failed to read config: {}", e)
            raise

    def start_client(self, ip, port):
        self.client = PlayerClient(ip=ip, port=port)
        threading.Thread(target=self.client.receive_updates, daemon=True).start() # start the thread to receive updates from the server 
        logger.info("Client started with IP: {}, Port: {}", ip, port)

    def handle_events(self):
        # handle the events of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                logger.info("Quit event detected, stopping the game")

    def update(self, dt):
        # manage the deplacement of your player (in client) and transmit to server
        # the new position of your player and the action / direction for animations
        keys = pygame.key.get_pressed()
        if self.client.player is None:
            return
        self.client.player.anim_current_action = "Idle"

        if keys[pygame.K_z] and keys[pygame.K_q]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "left_up"
            self.client.position[1] -= self.client.speed * dt
            self.client.position[0] -= self.client.speed * dt
        elif keys[pygame.K_z] and keys[pygame.K_d]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "right_up"
            self.client.position[1] -= self.client.speed * dt
            self.client.position[0] += self.client.speed * dt
        elif keys[pygame.K_s] and keys[pygame.K_q]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "left_down"
            self.client.position[1] += self.client.speed * dt
            self.client.position[0] -= self.client.speed * dt
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "right_down"
            self.client.position[1] += self.client.speed * dt
            self.client.position[0] += self.client.speed * dt
        elif keys[pygame.K_z]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "up"
            self.client.position[1] -= self.client.speed * dt
        elif keys[pygame.K_s]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "down"
            self.client.position[1] += self.client.speed * dt
        elif keys[pygame.K_q]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "left_down"
            self.client.position[0] -= self.client.speed * dt
        elif keys[pygame.K_d]:
            self.client.player.anim_current_action, self.client.player.anim_current_direction = "Walk", "right_down"
            self.client.position[0] += self.client.speed * dt

        self.client.send_position()
        logger.debug("Player position updated to: {}", self.client.position)

    def draw(self):
        # draw the entites of the game (using the tabs updated by handlers with server)
        self.screen.fill((255, 255, 255)) # fill the screen with white color (reset the screen)
        n_players = list(self.client.players.values())
        for player in n_players: # do this for every players in the game
            if player.id == self.client.player_id: 
                self.client.player = player # update the player in the client side if needed in other part of the code
            extra = True 
            if self.client.player is not None: 
                if (abs(player.position[0] - self.client.player.position[0])**2 + abs(player.position[1] - self.client.player.position[1])**2)**0.5 > 500:
                    extra = False # distance between the player and the other player is > 500 so we don't draw the other player extra infos
            player.draw(self.screen, self.font, (0, 0, 0), extra) # draw the player in the screen
        pygame.display.flip() # update the screen
        logger.debug("Screen drawn with {} players", len(n_players))

    def run(self):
        # run the game
        pygame.init()
        logger.info("Pygame initialized")
        self.setup_screen()
        self.load_assets()
        self.clock = pygame.time.Clock()
        ip, port = self.read_config() 
        self.start_client(ip, port)

        while self.running:
            dt = self.clock.tick(120) / 1000 # get the delta time between each frame (to have a smooth game)
            self.handle_events() # handle the events of the game
            self.update(dt) # update the game
            self.draw() # draw the game

        self.client.close() # close the connection with the server
        pygame.quit() # quit the game
        logger.info("Game closed")
