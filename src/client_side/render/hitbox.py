import pygame

class Hitbox:
    def __init__(self, frame, visible=True):
        self.visible = visible
        self.update(frame)

    def update(self, frame):
        bounding_rect = frame.get_bounding_rect()
        self.width, self.height = bounding_rect.width, bounding_rect.height
        self.x_offset, self.y_offset = bounding_rect.topleft

    def draw(self, window, frame_rect):
        if self.visible:
            hitbox_x = frame_rect.x + self.x_offset
            hitbox_y = frame_rect.y + self.y_offset
            pygame.draw.rect(window, (255, 0, 0), (hitbox_x, hitbox_y, self.width, self.height), 1)

    def get_coordinates(self, frame_rect):
        hitbox_x = frame_rect.x + self.x_offset
        hitbox_y = frame_rect.y + self.y_offset
        return hitbox_x, hitbox_y, self.width, self.height

    def set_visibility(self, visible):
        self.visible = visible