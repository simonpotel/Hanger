import pygame


class Player:
    def __init__(self, player_id, player_uuid, position):
        """
        class to represent a player in the game. construict by handle_data
        each players will have an object of this class.
        """
        self.id = player_id  # player id in the game
        self.uuid = player_uuid  # player uuid in the game
        self.position = position  # position of the player in the game
        self.image = pygame.image.load("assets/dev.png")  # image of the player
        self.image = pygame.transform.scale(
            self.image, (128, 128))  # scale the image

    def update_position(self, new_position):
        """
        updates the position of the player.
        """
        self.position = new_position

    def draw(self, screen, font, color):
        """
        draw the player in the screen.
        """
        screen.blit(
            self.image, self.position)  # draw the player image in the screen
        # render the uuid of the player
        uuid_text = font.render(self.uuid, True, color)
        # set the position of the uuid text
        text_rect = uuid_text.get_rect(
            center=(self.position[0] + 64, self.position[1] - 10))
        screen.blit(uuid_text, text_rect)  # draw the uuid text in the screen
