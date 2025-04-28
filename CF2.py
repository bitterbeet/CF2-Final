import pygame

pygame.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("State Machine Sprite Animation")

# Load your sprite sheet
sprite_sheet = pygame.image.load('Dancing.png').convert_alpha()

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

# Get frames from sprite sheet
dance_frames = get_frames(sprite_sheet, columns=3, rows=2)

# Debugging: Print the number of frames loaded
print(f"Number of frames loaded: {len(dance_frames)}")

# Different states
IDLE = "Idle"
DANCING = "Dancing"

class StateMachineSprite:
    def __init__(self):
        self.state = IDLE
        self.idle_frames = [dance_frames[0]]  # Just show first frame when idle
        self.dance_frames = dance_frames
        self.index = 0
        self.timer = 0
        self.scale_factor = 10  # Change this value to control the size

    def switch_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.index = 0
            self.timer = 0

    def update(self):
        # Debugging: Print the current state to check if it's switching correctly
        print(f"Current state: {self.state}")
        self.timer += 1
        if self.state == DANCING:
            if self.timer % 10 == 0:  # Controls animation speed
                self.index = (self.index + 1) % len(self.dance_frames)  # Ensure correct frame cycling
        elif self.state == IDLE:
            if self.timer % 10 == 0:
                self.index = (self.index + 1) % len(self.idle_frames)

    def draw(self, surface):
        if self.state == IDLE:
            frame = self.idle_frames[self.index]
        elif self.state == DANCING:
            frame = self.dance_frames[self.index]

        # Scale the frame to make the sprite bigger
        scaled_frame = pygame.transform.scale(frame, (FRAME_WIDTH * self.scale_factor, FRAME_HEIGHT * self.scale_factor))

        # Center the sprite on the screen
        self.x = (WIDTH - scaled_frame.get_width()) // 2
        self.y = (HEIGHT - scaled_frame.get_height()) // 2

        surface.blit(scaled_frame, (self.x, self.y))

# Set up font for displaying state
font = pygame.font.SysFont(None, 48)

def draw_text(surface, text, x, y):
    img = font.render(text, True, (255, 255, 255))
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

        player.update()

        screen.fill((50, 50, 50))  # Dark background
        player.draw(screen)
        draw_text(screen, f"Current State: {player.state}", 20, 20)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
