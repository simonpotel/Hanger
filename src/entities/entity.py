import pygame
from src.client_side.render.animation import Animation
from loguru import logger

class Entity():
    def __init__(self, id, name, uuid, position, asset_path, type, render):
        logger.info(f"Initializing Entity: id={id}, name={name}, uuid={uuid}, position={position}, asset_path={asset_path}, type={type}, render={render}")
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = type
        self.position = position
        self.hp = 100
        self.state = {'x': 0, 'y': 0}
        self.asset_path = asset_path
        self.anim_current_direction = "down"
        self.anim_current_action = "Idle"
        self.anim_animations = {}
        self.attack_type = 0

        if render:
            match type:
                case 1:
                    match asset_path:
                        case "player_skin_1":
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
                            logger.info("Loaded animations for player_skin_1")

    def update_position(self, new_position, anim_current_action, anim_current_direction):
        self.position = new_position
        self.anim_current_action = anim_current_action
        self.anim_current_direction = anim_current_direction


    def draw(self, screen, font, color, extra, draw_position):
        current_animation = self.anim_animations[self.anim_current_action][self.anim_current_direction]
        current_animation.update()

        screen.blit(current_animation.get_current_frame(),
                    (draw_position[0] - current_animation.frame_width * current_animation.scale_factor // 2,
                     draw_position[1] - current_animation.frame_height * current_animation.scale_factor // 2))

        current_animation.frames_hitboxs[current_animation.current_frame].draw(screen, current_animation.get_current_frame().get_rect(center=draw_position))

        if extra:
            id_text = font.render(f'ID: {self.id}', True, color)
            id_rect = id_text.get_rect(center=(draw_position[0]-20, draw_position[1] + 50))
            screen.blit(id_text, id_rect)

            hp_text = font.render(f'{self.hp}/100', True, color)
            hp_rect = hp_text.get_rect(midleft=(id_rect.right + 10, id_rect.centery))
            screen.blit(hp_text, hp_rect)

            heart_icon = pygame.image.load('assets/custom/heart.png')
            heart_icon = pygame.transform.scale(heart_icon, (20, 20))
            heart_rect = heart_icon.get_rect(midleft=(hp_rect.right + 5, hp_rect.centery))
            screen.blit(heart_icon, heart_rect)