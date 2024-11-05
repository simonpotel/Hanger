import pygame
from loguru import logger

class Animation:
    def __init__(self, asset_path, frame_width, frame_height, scale_factor=3):
        logger.info("Initializing Animation with asset_path: {}, frame_width: {}, frame_height: {}, scale_factor: {}", asset_path, frame_width, frame_height, scale_factor)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_factor = scale_factor
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.065
        self.animation_timer = 0

        try:
            self.sprite_sheet = pygame.image.load(asset_path).convert_alpha()
            logger.info("Sprite sheet loaded successfully from {}", asset_path)
        except pygame.error as e:
            logger.error("Failed to load sprite sheet from {}: {}", asset_path, e)
            raise

        self.num_frames = self.sprite_sheet.get_width() // self.frame_width
        logger.debug("Number of frames calculated: {}", self.num_frames)

        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(
                i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(
                frame, (frame_width * scale_factor, frame_height * scale_factor))
            self.frames.append(scaled_frame)
            logger.debug("Frame {} added to frames list", i)

    def update(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]
