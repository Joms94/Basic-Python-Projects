import pygame
pygame.init()

# Creates a game window. Parameters are width and height.
screen = 500
win = pygame.display.set_mode((screen, 480))

# Changes the name of the display
pygame.display.set_caption("First Game")

# Images and sprites
walk_right = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walk_left = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

# Character attributes
x = 50
y = 400
width = 64
height = 64
velocity = 5
# Is the character jumping?
is_jump = False
jump_count = 10
left = False
right = False
walk_count = 0


def redraw_game_window():
    global walk_count
    # .blit is useful whenever you want to put a picture on the screen.
    win.blit(bg, (0, 0))
    # Drawing the character (window, colour, rect(x, y, width, height)
    # If were to use greater than 27, we'd hit an index error because there are 9 sprites, each being displayed for
    # 3 seconds. Given 27 fps we can't go over.
    if walk_count + 1 >= 27:
        walk_count = 0
    if left:
        win.blit(walk_left[walk_count//3], (x, y))
        walk_count += 1
    elif right:
        win.blit(walk_right[walk_count//3], (x, y))
        walk_count += 1
    else:
        win.blit(char, (x, y))
    # Pygame needs to be prodded to display new things, such as our character.
    pygame.display.update()


# Main loop. A game always needs one of these to check for key presses and other events.
run = True
while run:
    # Time in milliseconds. We're using 27 frames per second because we're constrained by the number of sprites!
    clock.tick(27)
    # "For every event in the game, where an 'event' is a keyboard press or mouse movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    # Checking for inputs and whether or not they're single pressed or held.
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > velocity:
        x -= velocity
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < screen - width - velocity:
        x += velocity
        left = False
        right = True
    else:
        left = False
        right = False
        walk_count = 0

    if not is_jump:
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] and y > velocity:
            is_jump = True
            right = False
            left = False
            walk_count = 0
    else:
        if jump_count >= -10:
            neg = 1
            # This clause changes the trajectory of the jump.
            if jump_count < 0:
                neg = -1
            y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 10
    redraw_game_window()

pygame.quit()
