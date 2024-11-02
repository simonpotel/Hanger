import pygame
import random
from src.client_side.animation import Animation


class Entity():
    def __init__(self, id, name, uuid, position, asset_path, type, render):
        self.id = id # id of the entity (unique to each ID and attribued by the server)
        self.name = name # name of the entity
        self.uuid = uuid # uuid of the entity (unique to each ID and attribued by the server)
        self.type = type # type of the entity (1 for player, 2 for monster, 3 for npc)
        self.position = position # position of the entity (x, y)
        self.hp = 100 # health points of the entity
        self.state = {'x': 0, 'y': 0} # state of the entity (x, y)
        self.asset_path = asset_path # asset path of the entity
        self.anim_current_direction = "down" # current direction of the entity (down, left_down, left_up, right_down, right_up, up)
        self.anim_current_action = "Idle" # current action of the entity (Idle, Walk, Run, Attack, Die, ...)
        self.anim_animations = {} # animations of the entity (objects of Animation class for each animation) 

        if render: # we dont render the entity on server_side (only on client_side)
            match type: # match the type of the entity to load the correct animations
                case 1: # player
                    match asset_path: # match the asset path to load the correct animations
                        # we can implement here later some others skins for the player or others entities
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

    def update_position(self, new_position, anim_current_action, anim_current_direction):
        # update the position of the entity and the current action and direction
        self.position = new_position
        self.anim_current_action = anim_current_action
        self.anim_current_direction = anim_current_direction

    def draw(self, screen, font, color, extra):
        # draw the entity on the screen with the extra infos if needed
        current_animation = self.anim_animations[self.anim_current_action][self.anim_current_direction] # get the current animation
        current_animation.update() # update the current animation

        screen.blit(current_animation.get_current_frame(),
                    (self.position[0] - current_animation.frame_width * current_animation.scale_factor // 2,
                     self.position[1] - current_animation.frame_height * current_animation.scale_factor // 2)) # draw the current frame of the animation

        if extra: # draw the extra infos if needed 
            id_text = font.render(f'ID: {self.id}', True, color) # render the id of the entity
            id_rect = id_text.get_rect(center=(self.position[0]-20, self.position[1] + 50)) # get the rect of the id text
            screen.blit(id_text, id_rect) # draw the id text

            hp_text = font.render(f'{self.hp}/100', True, color) # render the hp of the entity
            hp_rect = hp_text.get_rect(midleft=(id_rect.right + 10, id_rect.centery)) # get the rect of the hp text
            screen.blit(hp_text, hp_rect) # draw the hp text

            heart_icon = pygame.image.load('assets/custom/heart.png') # load the heart icon
            heart_icon = pygame.transform.scale(heart_icon, (20, 20)) # scale the heart icon
            heart_rect = heart_icon.get_rect(midleft=(hp_rect.right + 5, hp_rect.centery)) # get the rect of the heart icon
            screen.blit(heart_icon, heart_rect) # draw the heart icon

