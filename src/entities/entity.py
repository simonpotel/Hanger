import pygame
import random


class Entity():
    def __init__(self, id, name, uuid, position, asset_path, type):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = type  # 0 = None, 1 = Player, 2 = Enemy, 3 = NPC, 4 = Item, 5 = Obstacle
        self.position = position
        self.render = pygame.image.load(asset_path)
        self.hp = 100  # 100 %
        self.render = pygame.transform.scale(self.render, (128, 128))
        self.state = {'x': 0, 'y': 0}
        self.asset_path = asset_path

    def update_position(self, new_position):
        """
        updates the position of the entity.
        """
        self.position = new_position

    def draw(self, screen, font, color, extra):
        """
        Draw the entity on the screen.
        """
        screen.blit(
            self.render, self.position)  # draw the entity image on the screen

        # render the name of the entity
        name_text = font.render(self.name, True, color)
        # set the position of the name text
        name_rect = name_text.get_rect(
            center=(self.position[0] + 20, self.position[1] - 10))
        screen.blit(name_text, name_rect)  # draw the name text on the screen

        if extra:
            # render the ID of the entity
            id_text = font.render(f'ID: {self.id}', True, color)
            # set the position of the ID text
            id_rect = id_text.get_rect(
                center=(self.position[0] + 64, self.position[1] + 138))
            screen.blit(id_text, id_rect)  # draw the ID text on the screen

            # render the HP of the entity
            hp_text = font.render(f'{self.hp}/100', True, color)
            # set the position of the HP text next to the name
            hp_rect = hp_text.get_rect(
                midleft=(name_rect.right + 10, name_rect.centery))
            screen.blit(hp_text, hp_rect)  # draw the HP text on the screen

            # load and draw the heart icon next to the HP text
            heart_icon = pygame.image.load('assets/heart.png')
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
