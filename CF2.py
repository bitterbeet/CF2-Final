import pygame
import sys

def load_image(image_path):
    try:
        return pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")
        sys.exit()

def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("State Machine Sprite Animation")

    # Load sprite sheets
    try:
        dance_sprite_sheet = load_image('Dancing.png')
        jump_sprite_sheet = load_image('Jumping.png')
        sleep_sprite_sheet = load_image('Sleeping.png')
        celebrate_sprite_sheet = load_image('Celebrating.png')
    except SystemExit:
        return 

    # Load backgrounds
    try:
        background_dancing = load_image('DancingBackground.jpg')
        background_jumping = load_image('JumpingBackground.jpg')
        background_sleeping = load_image('SleepingBackground2.jpg')
        background_celebrating = load_image('newnew.jpg')  # Make sure you have this!
    except SystemExit:
        return  

    FRAME_WIDTH = 30
    FRAME_HEIGHT = 30

    def get_frames(sheet, columns, rows):
        frames = []
        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface(
                    (col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
                )
                frames.append(frame)
        return frames

    # Get frames
    dance_frames = get_frames(dance_sprite_sheet, columns=3, rows=2)  
    jump_frames = get_frames(jump_sprite_sheet, columns=3, rows=2)   
    sleep_frames = get_frames(sleep_sprite_sheet, columns=3, rows=2) 
    celebrate_frames = get_frames(celebrate_sprite_sheet, columns=3, rows=2)

    print(f"Number of frames loaded: {len(dance_frames)} (Dance), {len(jump_frames)} (Jump), {len(sleep_frames)} (Sleep), {len(celebrate_frames)} (Celebrate)")

    # State constants
    IDLE = "Idle"
    DANCING = "Dancing"
    JUMPING = "Jumping"
    SLEEPING = "Sleeping"
    CELEBRATING = "Celebrating"

    class StateMachineSprite:
        def __init__(self):
            self.state = IDLE
            self.idle_frames = [dance_frames[0]]  
            self.dance_frames = dance_frames
            self.jump_frames = jump_frames
            self.sleep_frames = sleep_frames
            self.celebrate_frames = celebrate_frames  
            self.index = 0
            self.timer = 0
            self.scale_factor = 10
            self.fixed_width = 300
            self.fixed_height = 300
            self.x = (WIDTH - self.fixed_width) // 2
            self.y = (HEIGHT - self.fixed_height) // 2

        def switch_state(self, new_state):
            if self.state != new_state:
                self.state = new_state
                self.index = 0
                self.timer = 0

        def update(self):
            self.timer += 1
            if self.state == DANCING:
                if self.timer % 15 == 0:
                    self.index = (self.index + 1) % len(self.dance_frames)
            elif self.state == IDLE:
                if self.timer % 10 == 0:
                    self.index = (self.index + 1) % len(self.idle_frames)
            elif self.state == JUMPING:
                if self.timer % 9 == 0:
                    self.index = (self.index + 1) % len(self.jump_frames)
            elif self.state == SLEEPING:
                if self.timer % 100 == 0:
                    self.index = (self.index + 1) % len(self.sleep_frames)
            elif self.state == CELEBRATING:
                if self.timer % 10 == 0:  # 
                    self.index = (self.index + 1) % len(self.celebrate_frames)

        def draw(self, surface):
            if self.state == DANCING:
                frame = self.dance_frames[self.index]
                background = background_dancing
            elif self.state == JUMPING:
                frame = self.jump_frames[self.index]
                background = background_jumping
            elif self.state == SLEEPING:
                frame = self.sleep_frames[self.index]
                background = background_sleeping
            elif self.state == CELEBRATING:
                frame = self.celebrate_frames[self.index]
                background = background_celebrating
            else:  # Idle
                frame = self.idle_frames[0]
                background = pygame.Surface((WIDTH, HEIGHT))
                background.fill((200, 200, 200))

            background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
            surface.blit(background_scaled, (0, 0))

            scaled_frame = pygame.transform.scale(frame, (self.fixed_width, self.fixed_height))
            surface.blit(scaled_frame, (self.x, self.y))

    # Setup fonts
    font = pygame.font.SysFont(None, 48)
    instruction_font = pygame.font.SysFont(None, 36)

    def draw_text(surface, text, x, y, font_type=font):
        img = font_type.render(text, True, (255, 255, 255))
        surface.blit(img, (x, y))

    clock = pygame.time.Clock()
    running = True
    player = StateMachineSprite()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.switch_state(DANCING)
                if event.key == pygame.K_i:
                    player.switch_state(IDLE)
                if event.key == pygame.K_j:
                    player.switch_state(JUMPING)
                if event.key == pygame.K_s:
                    player.switch_state(SLEEPING)
                if event.key == pygame.K_c:  
                    player.switch_state(CELEBRATING)

        player.update()
        screen.fill((50, 50, 50))
        player.draw(screen)

        draw_text(screen, f"Current State: {player.state}", 20, 20)
        draw_text(screen, "Press 'D' to Dance", 20, HEIGHT - 180, instruction_font)
        draw_text(screen, "Press 'I' to Idle", 20, HEIGHT - 140, instruction_font)
        draw_text(screen, "Press 'J' to Jump", 20, HEIGHT - 100, instruction_font)
        draw_text(screen, "Press 'S' to Sleep", 20, HEIGHT - 60, instruction_font)
        draw_text(screen, "Press 'C' to Celebrate", 20, HEIGHT - 20, instruction_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
