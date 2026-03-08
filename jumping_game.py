import pygame
import random
from sys import exit

# Game constants
GAME_WIDTH = 360
GAME_HEIGHT = 640

CHARACTER_X = GAME_WIDTH / 9
CHARACTER_Y = GAME_HEIGHT / 3
CHARACTER_WIDTH = 55   # bigger size for man character
CHARACTER_HEIGHT = 42

PIPE_X = GAME_WIDTH
PIPE_Y = 0
PIPE_WIDTH = 64
PIPE_HEIGHT = 512


class Character(pygame.Rect):
    """Main player character (man)."""
    def __init__(self, img):
        super().__init__(CHARACTER_X, CHARACTER_Y, CHARACTER_WIDTH, CHARACTER_HEIGHT)
        self.img = img


class Pipe(pygame.Rect):
    """Obstacle pipes."""
    def __init__(self, img):
        super().__init__(PIPE_X, PIPE_Y, PIPE_WIDTH, PIPE_HEIGHT)
        self.img = img
        self.passed = False


# Game images (filenames unchanged so they load correctly)
background_image = pygame.image.load("flappybirdbg.png")
character_image = pygame.image.load("pixel-character.gif")
character_image = pygame.transform.scale(character_image, (CHARACTER_WIDTH, CHARACTER_HEIGHT))

top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))


# Game state
player = Character(character_image)
pipes = []
velocity_x = -2   # pipe movement speed
velocity_y = 0    # character vertical speed
gravity = 0.4
score = 0
game_over = False


def draw(window):
    """Render all game elements."""
    window.blit(background_image, (0, 0))
    window.blit(player.img, player)

    for pipe in pipes:
        window.blit(pipe.img, pipe)

    text_str = str(int(score))
    if game_over:
        text_str = f"Game Over: {text_str}"

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str, True, "white")
    window.blit(text_render, (5, 0))


def move():
    """Update character and pipe positions, check collisions."""
    global velocity_y, score, game_over

    velocity_y += gravity
    player.y += velocity_y
    player.y = max(player.y, 0)

    if player.y > GAME_HEIGHT:
        game_over = True
        return

    for pipe in pipes:
        pipe.x += velocity_x

        if not pipe.passed and player.x > pipe.x + pipe.width:
            score += 0.5  # two pipes per set → 1 point total
            pipe.passed = True

        if player.colliderect(pipe):
            game_over = True
            return

    while pipes and pipes[0].x < -PIPE_WIDTH:
        pipes.pop(0)


def create_pipes():
    """Generate a new pair of pipes with random gap position."""
    random_pipe_y = PIPE_Y - PIPE_HEIGHT / 4 - random.random() * (PIPE_HEIGHT / 2)
    opening_space = GAME_HEIGHT / 4

    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)


def main():
    """Main game loop."""
    global velocity_y, score, game_over

    pygame.init()
    window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    pygame.display.set_caption("Jumping Game")   # updated title
    clock = pygame.time.Clock()

    create_pipes_timer = pygame.USEREVENT + 0
    pygame.time.set_timer(create_pipes_timer, 1500)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == create_pipes_timer and not game_over:
                create_pipes()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    velocity_y = -6

                    if game_over:
                        player.y = CHARACTER_Y
                        pipes.clear()
                        score = 0
                        game_over = False

        if not game_over:
            move()
            draw(window)
            pygame.display.update()
            clock.tick(60)


if __name__ == "__main__":
    main()











