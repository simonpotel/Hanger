import pygame

class Animation:
    def __init__(self, asset_path, frame_width, frame_height, scale_factor=3):
        self.frame_width = frame_width # frame of the sprite
        self.frame_height = frame_height # frame of the sprite
        self.scale_factor = scale_factor # scale factor (to up the size if needed of the sprite)
        self.frames = [] # list of frames for this animation
        self.current_frame = 0 # current frame
        self.animation_speed = 0.025 # speed of the animation (time between each frame)
        self.animation_timer = 0 # timer for the animation
        self.sprite_sheet = pygame.image.load(asset_path).convert_alpha() # load the sprite sheet
        self.num_frames = self.sprite_sheet.get_width() // self.frame_width # define number of frames depends width

        # append the frames to the list 
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(
                i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(
                frame, (frame_width * scale_factor, frame_height * scale_factor))
            self.frames.append(scaled_frame)

    def update(self):
        self.animation_timer += self.animation_speed # update the timer for the animation 
        if self.animation_timer >= 1: # max time of the animation
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames) # update the current frame

    def get_current_frame(self):
        return self.frames[self.current_frame] # return the current frame
