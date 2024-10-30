import pygame
import json
import threading
from src.client_side.player_client import PlayerClient

class GameClient:
    def __init__(self, width, height, config_path, logo_path):
        self.width = width
        self.height = height
        self.config_path = config_path
        self.logo_path = logo_path
        self.screen = None
        self.font = None
        self.client_logo = None
        self.clock = None
        self.client = None
        self.running = True

    def setup_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Hungry Client DEV")

    def load_assets(self):
        self.font = pygame.font.Font(None, 24)
        self.client_logo = pygame.image.load(self.logo_path)
        pygame.display.set_icon(self.client_logo)
        self.client_logo = pygame.transform.scale(self.client_logo, (128, 128))

    def read_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config.get('ip'), config.get('port')

    def start_client(self, ip, port):
        self.client = PlayerClient(ip=ip, port=port)
        threading.Thread(target=self.client.receive_updates, daemon=True).start()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.client.position[1] -= self.client.speed * dt
        if keys[pygame.K_s]:
            self.client.position[1] += self.client.speed * dt
        if keys[pygame.K_q]:
            self.client.position[0] -= self.client.speed * dt
        if keys[pygame.K_d]:
            self.client.position[0] += self.client.speed * dt
        self.client.send_position()

    def draw(self):
        self.screen.fill((255, 255, 255))
        n_players = list(self.client.players.values()) 
        for player in n_players:
            if player.entity.id == self.client.player_id:
                self.client.player = player
            extra = True
            if self.client.player is not None: 
                if (abs(player.entity.position[0] - self.client.player.entity.position[0])**2 + abs(player.entity.position[1] - self.client.player.entity.position[1])**2)**0.5 > 500:
                    extra = False 
            player.entity.draw(self.screen, self.font, (0, 0, 0), extra)
        pygame.display.flip()

    def run(self):
        pygame.init()
        self.setup_screen()
        self.load_assets()
        self.clock = pygame.time.Clock()
        ip, port = self.read_config()
        self.start_client(ip, port)

        while self.running:
            dt = self.clock.tick(120) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
            #print(self.client.players)

        self.client.close()
        pygame.quit()

if __name__ == "__main__":
    game_client = GameClient(width=1280, height=720, config_path='configs/host.json', logo_path='assets/server.png')
    game_client.run()   