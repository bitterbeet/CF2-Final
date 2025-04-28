import pygame

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("State Machine Sprite Animation")

# Load your sprite sheets
dance_sprite_sheet = pygame.image.load('Dancing.png').convert_alpha()
jump_sprite_sheet = pygame.image.load('Jumping.png').convert_alpha()

# Load different backgrounds for each state
background_dancing = pygame.image.load('DancingBackground.jpg').convert()
background_jumping = pygame.image.load('JumpingBackground.jpg').convert()

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

# Debugging: Print the number of frames loaded
print(f"Number of frames loaded: {len(dance_frames)} (Dance), {len(jump_frames)} (Jump)")

# Different states
IDLE = "Idle"
DANCING = "Dancing"
JUMPING = "Jumping"

class StateMachineSprite:
    def __init__(self):
        self.state = IDLE
        self.idle_frames = [dance_frames[0]]  # Just show first frame when idle
        self.dance_frames = dance_frames
        self.jump_frames = jump_frames  # Frames for the jumping animation
        self.index = 0
        self.timer = 0
        self.scale_factor = 10  # Set scale factor to 10 for larger sprite
        self.y = HEIGHT - 100  # Initial vertical position (on the ground)

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
            # Here we could add jump logic for vertical movement if needed

    def draw(self, surface):
        if self.state == IDLE:
            frame = self.idle_frames[self.index]
            # Use a plain color for the idle state background (e.g., gray)
            surface.fill((169, 169, 169))  # Light gray color for idle background
        elif self.state == DANCING:
            frame = self.dance_frames[self.index]
            # Set background for dancing state
            background = background_dancing
            # Scale the background to fit the window
            background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
            surface.blit(background_scaled, (0, 0))  # Draw the dancing background
        elif self.state == JUMPING:
            frame = self.jump_frames[self.index]
            # Set background for jumping state
            background = background_jumping
            # Scale the background to fit the window
            background_scaled = pygame.transform.scale(background, (WIDTH, HEIGHT))
            surface.blit(background_scaled, (0, 0))  # Draw the jumping background

        # Scale the sprite to make it 10x bigger
        scaled_frame = pygame.transform.scale(frame, (FRAME_WIDTH * self.scale_factor, FRAME_HEIGHT * self.scale_factor))

        # Center the sprite on the screen
        self.x = (WIDTH - scaled_frame.get_width()) // 2
        self.y = (HEIGHT - scaled_frame.get_height()) // 2

        surface.blit(scaled_frame, (self.x, self.y))

# Set up font for displaying state and instructions
font = pygame.font.SysFont(None, 48)
instruction_font = pygame.font.SysFont(None, 36)

def draw_text(surface, text, x, y, font_type=font):
    img = font_type.render(text, True, (255, 255, 255))
    surface.blit(img, (x, y))

def main():
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

        player.update()

        # Draw the sprite
        player.draw(screen)

        # Draw the current state text
        draw_text(screen, f"Current State: {player.state}", 20, 20)

        # Draw instructions for the user
        draw_text(screen, "Press 'D' to Dance", 20, HEIGHT - 100, instruction_font)
        draw_text(screen, "Press 'I' to Idle", 20, HEIGHT - 60, instruction_font)
        draw_text(screen, "Press 'J' to Jump", 20, HEIGHT - 20, instruction_font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
