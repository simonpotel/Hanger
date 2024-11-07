import pygame
import json
import threading
from src.client_side.player_client import PlayerClient
from src.entities.entity import Entity  # Import Entity class
from loguru import logger


class GameClient:
    def __init__(self, width, height, config_path, logo_path):
        self.width = width  # window size
        self.height = height  # window size
        self.config_path = config_path  # path to the config file configs/host.json
        self.logo_path = logo_path  # logo of the game
        self.screen = None  # pygame screen obj
        self.font = None  # pygame font obj
        self.client_logo = None  # pygame image obj
        self.clock = None  # pygame clock obj
        self.client = None  # PlayerClient obj
<<<<<<< Updated upstream
        self.attacking = False
        self.attack_frame = 0
        self.attack_ani_R = []  # Define attack_ani_R as an empty list or load the actual animation frames
        self.attack_ani_L = []  # Define attack_ani_L as an empty list or load the actual animation frames
        self.entity = Entity(id=0, name="default", uuid="0000", position=(0, 0), asset_path="", type="default", render=True)  # Ensure entity is defined
=======
        self.attack_type = 0 # attack type of the player
>>>>>>> Stashed changes
        self.running = True
        self.debug = False
        logger.info("GameClient initialized with width: {}, height: {}, config_path: {}, logo_path: {}",
                    width, height, config_path, logo_path)

    def setup_screen(self):
        self.screen = pygame.display.set_mode(
            (self.width, self.height))  # create the game window
        # set the game window title
        caption = "Hanger Client (Debug)" if self.debug else "Hanger Client"
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)  # hide the default mouse cursor
        logger.info("Screen setup with width: {}, height: {}",
                    self.width, self.height)

    def load_assets(self):
        self.font = pygame.font.Font(None, 24)  # load the font for the game
        self.client_logo = pygame.image.load(
            self.logo_path)  # load the logo of the game
        pygame.display.set_icon(self.client_logo)  # set the logo of the game
        self.client_logo = pygame.transform.scale(
            # scale the logo if needed to 128x128
            self.client_logo, (128, 128))
        logger.info("Assets loaded successfully")

    def read_config(self):
        # this will return the config of configs/host.json to relation between client - server
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            logger.info("Config read successfully from {}", self.config_path)
            # return the ip and port of the server
            return config.get('ip'), config.get('port')
        except Exception as e:
            logger.error("Failed to read config: {}", e)
            raise

    def start_client(self, ip, port):
        self.client = PlayerClient(ip=ip, port=port)
        # start the thread to receive updates from the server
        threading.Thread(target=self.client.receive_updates,
                         daemon=True).start()
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

        if keys[pygame.K_r] or keys[pygame.K_t]:
            #self.client.player.anim_current_action = "Attack"
            #self.attack_test()
            if keys[pygame.K_r]:
                self.attack_type = 1
            elif keys[pygame.K_t]:
                self.attack_type = 2


        self.client.send_position()
        logger.debug("Player position updated to: {}", self.client.position)

    def attack(self):
        if self.attacking:
            if self.attack_frame >= len(self.attack_ani_R):
                self.attack_frame = 0
                self.attacking = False
            else:
                if self.client.player.anim_current_direction in ["right", "right_up", "right_down"]:
                    self.client.player.image = self.attack_ani_R[self.attack_frame]
                else:
                    self.client.player.image = self.attack_ani_L[self.attack_frame]
                
                # Check for nearby entities to apply damage
                for player in self.client.players.values():
                    if player.id != self.client.player_id:
                        distance = ((player.position[0] - self.client.player.position[0]) ** 2 + (player.position[1] - self.client.player.position[1]) ** 2) ** 0.5
                        if distance < self.client.player.attack_range:
                            if hasattr(player, 'entity') and hasattr(player.entity, 'hp'):
                                player.entity.hp -= self.client.player.attack_damage
                                logger.info("Player {} attacked Player {}. New health: {}", self.client.player.id, player.id, player.entity.hp)
                            else:
                                logger.warning("Player {} does not have a valid entity or hp attribute", player.id)
                self.client.broadcast_entities()
                self.attack_frame += 1
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.attacking = True
                self.attack_frame = 0
                self.client.player.anim_current_action = "Attack"
                self.client.send_action("Attack")

    def draw(self):
        # draw the entities of the game (using the tabs updated by handlers with server)
        # fill the screen with white color (reset the screen)
        if self.client.player is None:
            return
        self.screen.fill((255, 255, 255))
        n_players = list(self.client.players.values())

        # manage the camera offset to follow the player (your own) in center of the game window
        # camera offset x center
        camera_offset_x = self.client.player.position[0] - self.width // 2
        # camera offset y center
        camera_offset_y = self.client.player.position[1] - self.height // 2

        for map_name, assets in self.client.maps.maps_animations.items():
            for asset_name, animation in assets.items():
                animation.update()  # update the animation
                frame = animation.get_current_frame()  # get the current frame of the animation
                asset_properties = self.client.maps.maps[map_name][asset_name]
                position = (
                    asset_properties['x'] - camera_offset_x, asset_properties['y'] - camera_offset_y)
                # draw the animation at the specified position
                self.screen.blit(frame, position)

        for player in n_players:  # do this for every player in the game
            if player.id == self.client.player_id:
                # update the player in the client side if needed in other part of the code
                self.client.player = player
            extra = True
            if self.client.player is not None:
                if (abs(player.position[0] - self.client.player.position[0])**2 + abs(player.position[1] - self.client.player.position[1])**2)**0.5 > 500:
                    extra = False  # distance between the player and the other player is > 500 so we don't draw the other player extra infos
            # position of the player on the screen (centered)
            draw_position = (
                player.position[0] - camera_offset_x, player.position[1] - camera_offset_y)
            # draw the player on the screen
            # write the player on the screen with the correct position (with offset)
            player.draw(self.screen, self.font,
                        (0, 0, 0), extra, draw_position)

        if pygame.mouse.get_focused():  # if the mouse is focused on the game window
            cursor_image = pygame.image.load(
                'assets/Tiny Swords/UI/Pointers/01.png')  # load the cursor image
            cursor_image = pygame.transform.scale(
                cursor_image, (64, 64))  # scale the cursor image
            # get the position of the mouse on the screen
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(cursor_image, (mouse_x - cursor_image.get_width() // 2,
                             mouse_y - cursor_image.get_height() // 2))  # draw the cursor on the screen

        if self.attack_type == 1:
            #self.attack_type = 0
            self.attack_test()

        pygame.display.flip()  # update the screen
        logger.debug("Screen drawn with {} players", len(n_players))


    def attack_test(self):

        try:
            objetanim = self.client.player.anim_animations[self.client.player.anim_current_action][self.client.player.anim_current_direction]
            width = objetanim.frame_width
            height = objetanim.frame_height

            x, y = self.client.player.position[0], self.client.player.position[1]

            attacking_rect = pygame.Rect(x - width // 2, y - height // 2, 2 * width, height)
            pygame.draw.rect(self.screen, (255, 0, 0), attacking_rect)
        except Exception as e:
            logger.error("Error in attack_test: {}", e)

    def run(self, debug=False):
        # run the game
        self.debug = debug
        pygame.init()
        logger.info("Pygame initialized")
        self.setup_screen()
        self.load_assets()
        self.clock = pygame.time.Clock()
        ip, port = self.read_config()
        self.start_client(ip, port)

        while self.running:
            # get the delta time between each frame (to have a smooth game)
            cloak = self.clock.tick(120)
            dt = cloak/1000
            self.handle_events()  # handle the events of the game
            self.update(dt)  # update the game
            self.draw()  # draw the game

        self.client.close()  # close the connection with the server
        pygame.quit()  # quit the game
        logger.info("Game closed")
