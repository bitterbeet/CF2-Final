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

    # Window setup
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("State Machine Sprite Animation")

    # Load your sprite sheets
    try:
        dance_sprite_sheet = load_image('Dancing.png')
        jump_sprite_sheet = load_image('Jumping.png')
        sleep_sprite_sheet = load_image('Sleeping.png')  # New sleeping sprite sheet
    except SystemExit:
        return  # Exit if there's an error loading the images

    # Load different backgrounds for each state
    try:
        background_dancing = load_image('DancingBackground.jpg')
        background_jumping = load_image('JumpingBackground.jpg')
        background_sleeping = load_image('SleepingBackground.jpg')  # New sleeping background
    except SystemExit:
        return  # Exit if there's an error loading the images

    # Frame dimensions
    FRAME_WIDTH = 30
    FRAME_HEIGHT = 30

    # Function to grab frames from the sprite sheet
    def get_frames(sheet, columns, rows):
        frames = []
        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface(
                    (col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
                )
                frames.append(frame)
        return frames

    # Get frames from each sprite sheet
    dance_frames = get_frames(dance_sprite_sheet, columns=3, rows=2)  # 3 columns, 2 rows for dancing
    jump_frames = get_frames(jump_sprite_sheet, columns=3, rows=2)    # 3 columns, 2 rows for jumping
    sleep_frames = get_frames(sleep_sprite_sheet, columns=3, rows=2)   # 3 columns, 2 rows for sleeping

    # Debugging: Print the number of frames loaded
    print(f"Number of frames loaded: {len(dance_frames)} (Dance), {len(jump_frames)} (Jump), {len(sleep_frames)} (Sleep)")

    # Different states
    IDLE = "Idle"
    DANCING = "Dancing"
    JUMPING = "Jumping"
    SLEEPING = "Sleeping"  # New sleeping state

    class StateMachineSprite:
        def __init__(self):
            self.state = IDLE
            self.idle_frames = [dance_frames[0]]  # Just show first frame when idle
            self.dance_frames = dance_frames
            self.jump_frames = jump_frames  # Frames for the jumping animation
            self.sleep_frames = sleep_frames  # Frames for the sleeping animation
            self.index = 0
            self.timer = 0
            self.scale_factor = 10  # Set scale factor to 10 for larger sprite
            # Define a fixed size for the sprite (to prevent size changes between states)
            self.fixed_width = 300  # Fixed width for scaling
            self.fixed_height = 300  # Fixed height for scaling
            self.x = (WIDTH - self.fixed_width) // 2  # Center horizontally
            self.y = (HEIGHT - self.fixed_height) // 2  # Center vertically

        def switch_state(self, new_state):
            if self.state != new_state:
                self.state = new_state
                self.index = 0
                self.timer = 0

        def update(self):
            self.timer += 1
            if self.state == DANCING:
                if self.timer % 10 == 0:  # Controls animation speed
                    self.index = (self.index + 1) % len(self.dance_frames)
            elif self.state == IDLE:
                if self.timer % 10 == 0:
                    self.index = (self.index + 1) % len(self.idle_frames)
            elif self.state == JUMPING:
                if self.timer % 5 == 0:  # Controls animation speed for jumping
                    self.index = (self.index + 1) % len(self.jump_frames)
            elif self.state == SLEEPING:
                if self.timer % 15 == 0:  # Controls animation speed for sleeping
                    self.index = (self.index + 1) % len(self.sleep_frames)

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
            else:  # Default IDLE state (plain background)
                frame = self.idle_frames[0]
                # Create a solid color surface for the idle background (light gray)
                background = pygame.Surface((WIDTH, HEIGHT))
                background.fill((200, 200, 200))

            # Scale the background to fit the window
            background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
            surface.blit(background_scaled, (0, 0))  # Draw the background

            # Scale the sprite to a fixed size (using self.fixed_width and self.fixed_height)
            scaled_frame = pygame.transform.scale(frame, (self.fixed_width, self.fixed_height))

            # Draw the sprite at the fixed position (center of the screen)
            surface.blit(scaled_frame, (self.x, self.y))

    # Set up font for displaying state and instructions
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

            # Handle key presses for switching state
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.switch_state(DANCING)
                if event.key == pygame.K_i:
                    player.switch_state(IDLE)
                if event.key == pygame.K_j:
                    player.switch_state(JUMPING)
                if event.key == pygame.K_s:  # Press 'S' to sleep
                    player.switch_state(SLEEPING)

        player.update()

        # Fill the screen with a background color
        screen.fill((50, 50, 50))

        # Draw the sprite
        player.draw(screen)

        # Draw the current state text
        draw_text(screen, f"Current State: {player.state}", 20, 20)

        # Draw instructions for the user
        draw_text(screen, "Press 'D' to Dance", 20, HEIGHT - 100, instruction_font)
        draw_text(screen, "Press 'I' to Idle", 20, HEIGHT - 60, instruction_font)
        draw_text(screen, "Press 'J' to Jump", 20, HEIGHT - 20, instruction_font)
        draw_text(screen, "Press 'S' to Sleep", 20, HEIGHT - 140, instruction_font)  # Instruction for Sleep state

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
