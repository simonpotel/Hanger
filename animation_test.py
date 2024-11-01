import pygame


class Animation:
    def __init__(self, asset_path, frame_width, frame_height, scale_factor=3):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_factor = scale_factor
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.05
        self.animation_timer = 0
        self.sprite_sheet = pygame.image.load(asset_path).convert_alpha()
        self.num_frames = self.sprite_sheet.get_width() // self.frame_width
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
            scaled_frame = pygame.transform.scale(frame, (frame_width * scale_factor, frame_height * scale_factor))
            self.frames.append(scaled_frame)

    def update(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def get_current_frame(self):
        return self.frames[self.current_frame]


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player_x = 400
        self.player_y = 300
        self.player_speed = 3
        self.current_action = "Idle"
        self.current_direction = "down"
        self.animations = self.load_animations()
        self.running = True

    def load_animations(self):
        return {
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

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.current_action = "Idle"
        if keys[pygame.K_z] and keys[pygame.K_q]:
            self.current_action, self.current_direction = "Walk", "left_up"
            self.player_y -= self.player_speed
            self.player_x -= self.player_speed
        elif keys[pygame.K_z] and keys[pygame.K_d]:
            self.current_action, self.current_direction = "Walk", "right_up"
            self.player_y -= self.player_speed
            self.player_x += self.player_speed
        elif keys[pygame.K_s] and keys[pygame.K_q]:
            self.current_action, self.current_direction = "Walk", "left_down"
            self.player_y += self.player_speed
            self.player_x -= self.player_speed
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            self.current_action, self.current_direction = "Walk", "right_down"
            self.player_y += self.player_speed
            self.player_x += self.player_speed
        elif keys[pygame.K_z]:
            self.current_action, self.current_direction = "Walk", "up"
            self.player_y -= self.player_speed
        elif keys[pygame.K_s]:
            self.current_action, self.current_direction = "Walk", "down"
            self.player_y += self.player_speed
        elif keys[pygame.K_q]:
            self.current_action, self.current_direction = "Walk", "left_down"
            self.player_x -= self.player_speed
        elif keys[pygame.K_d]:
            self.current_action, self.current_direction = "Walk", "right_down"
            self.player_x += self.player_speed

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.handle_input()
            current_animation = self.animations[self.current_action][self.current_direction]
            current_animation.update()
            self.screen.fill((255, 255, 255))
            self.screen.blit(current_animation.get_current_frame(),
                             (self.player_x - current_animation.frame_width * current_animation.scale_factor // 2,
                              self.player_y - current_animation.frame_height * current_animation.scale_factor // 2))
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()