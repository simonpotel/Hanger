import pygame


class Entity():
    def __init__(self, id, name, uuid, position, asset_path, type):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.type = type # 0 = None, 1 = Player, 2 = Enemy, 3 = NPC, 4 = Item, 5 = Obstacle
        self.position = position
        self.render = pygame.image.load(asset_path)
        self.hp = 100 # 100 %
        self.render = pygame.transform.scale(self.render, (128, 128))
        self.state = {'x': 0, 'y': 0}

    def update_position(self, new_position):
        """
        updates the position of the entity.
        """
        self.position = new_position

    def draw(self, screen, font, color):
        """
        draw the entity in the screen.
        """
        screen.blit(
            self.render, self.position)  # draw the entity image in the screen
        # render the uuid of the entity
        name_text = font.render(self.name, True, color)
        # set the position of the name text
        text_rect = name_text.get_rect(
            center=(self.position[0] + 64, self.position[1] - 10))
        screen.blit(name_text, text_rect)  # draw the name text in the screen
