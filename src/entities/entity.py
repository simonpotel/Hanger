import pygame
import random
from loguru import logger
from src.client_side.animation import Animation


class Entity():
    def __init__(self, id, name, uuid, position, asset_path, type, render):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = type  # 0 = None, 1 = Player, 2 = Enemy, 3 = NPC, 4 = Item, 5 = Obstacle
        self.position = position
        self.hp = 100  # 100 %
        self.state = {'x': 0, 'y': 0}
        self.asset_path = asset_path

        if render == True:
            match asset_path:
                case "player_skin_1":  # player
                    self.anim_current_action = "Idle"
                    self.anim_current_direction = "down"
                    self.anim_animations = {
                        "Idle": {
                            "down": Animation("assets/character/Idle/idle_down.png", 48, 64),
                            "left_down": Animation("assets/character/Idle/idle_left_down.png", 48, 64),
                            "left_up": Animation("assets/character/Idle/idle_left_up.png", 48, 64),
                            "right_down": Animation("assets/character/Idle/idle_right_down.png", 48, 64),
                            "right_up": Animation("assets/character/Idle/idle_right_up.png", 48, 64),
                            "up": Animation("assets/character/Idle/idle_up.png", 48, 64),
                        },
                        "Walk": {
                            "down": Animation("assets/character/Walk/walk_down.png", 48, 64),
                            "left_down": Animation("assets/character/Walk/walk_left_down.png", 48, 64),
                            "left_up": Animation("assets/character/Walk/walk_left_up.png", 48, 64),
                            "right_down": Animation("assets/character/Walk/walk_right_down.png", 48, 64),
                            "right_up": Animation("assets/character/Walk/walk_right_up.png", 48, 64),
                            "up": Animation("assets/character/Walk/walk_up.png", 48, 64),
                        }
                    }

    def update_position(self, new_position):
        """
        updates the position of the entity.
        """
        self.position = new_position

    def draw(self, screen, font, color, extra):
        """
        Draw the entity on the screen.
        """
        current_animation = self.anim_animations[self.anim_current_action][self.anim_current_direction]
        current_animation.update()  

        screen.blit(current_animation.get_current_frame(),
                    (self.position[0] - current_animation.frame_width * current_animation.scale_factor // 2,
                     self.position[1] - current_animation.frame_height * current_animation.scale_factor // 2))

        if extra:
            # render the ID of the entity
            id_text = font.render(f'ID: {self.id}', True, color)
            # set the position of the ID text
            id_rect = id_text.get_rect(
                center=(self.position[0]-20, self.position[1] + 50))
            screen.blit(id_text, id_rect)  # draw the ID text on the screen

            # render the HP of the entity
            hp_text = font.render(f'{self.hp}/100', True, color)
            # set the position of the HP text next to the name
            hp_rect = hp_text.get_rect(
                midleft=(id_rect.right + 10, id_rect.centery))
            screen.blit(hp_text, hp_rect)  # draw the HP text on the screen

            # load and draw the heart icon next to the HP text
            heart_icon = pygame.image.load('assets/custom/heart.png')
            heart_icon = pygame.transform.scale(heart_icon, (20, 20))
            heart_rect = heart_icon.get_rect(
                midleft=(hp_rect.right + 5, hp_rect.centery))
            # draw the heart icon on the screen
            screen.blit(heart_icon, heart_rect)

    def reduce_hp_randomly(self):
        """
        Reduces the HP of the entity by a random value between 1 and 100.
        """
        self.hp = random.randint(1, 100)
        print(self.id, self.hp)
