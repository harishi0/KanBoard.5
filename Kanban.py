import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT =   screen_info.current_h
screen = pygame.display.set_mode((0,0),FULLSCREEN)

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set the font properties
FONT_SIZE = 24
FONT_NAME = pygame.font.get_default_font()

# Create a Note function
def create_note():
    x = random.randint(0, WIDTH - 200)
    y = random.randint(0, HEIGHT - 200)
    width = 200
    height = 200
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    text = ""
    selected = False
    dragging = False
    offset_x = 0
    offset_y = 0

    def draw(screen):
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_lines = text.split('\n')
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (x + 10, y + 10 + (i * FONT_SIZE)))

    def handle_event(event):
        nonlocal selected, dragging, x, y, offset_x, offset_y, text
        if event.type == pygame.KEYDOWN:
            if selected:
                if event.key == pygame.K_RETURN:
                    text += '\n'
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if x < event.pos[0] < x + width and y < event.pos[1] < y + height:
                    selected = True
                    dragging = True
                    offset_x = event.pos[0] - x
                    offset_y = event.pos[1] - y
                else:
                    selected = False
                    dragging = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                x = event.pos[0] - offset_x
                y = event.pos[1] - offset_y

    def update():
        if selected:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

    return {
        'draw': draw,
        'handle_event': handle_event,
        'update': update
    }


# Create a Button function
def create_button(x, y, width, height, color, text, text_color):
    def draw(screen):
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = font.render(text, True, text_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return x < event.pos[0] < x + width and y < event.pos[1] < y + height
        return False

    return {
        'draw': draw,
        'is_clicked': is_clicked
    }


# Create the screen
pygame.display.set_caption("Sticky Notes App")

# Create the font
font = pygame.font.Font(FONT_NAME, FONT_SIZE)

# Create a list to store notes
notes = []

# Create the "Create Note" button
button_width = 150
button_height = 50
button_x = (WIDTH - button_width) // 2
button_y = 20
button_color = GRAY
button_text = "Create Note"
button_text_color = BLACK
create_button = create_button(button_x, button_y, button_width, button_height, button_color, button_text, button_text_color)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            # Handle events for each note
            for note in notes:
                note['handle_event'](event)

            # Check if the "Create Note" button is clicked
            if create_button['is_clicked'](event):
                new_note = create_note()
                notes.append(new_note)

    # Clear the screen
    screen.fill(WHITE)

    # Draw notes
    for note in notes:
        note['draw'](screen)
        note['update']()

    # Draw the "Create Note" button
    create_button['draw'](screen)

    # Update the display
    pygame.display.flip()

# Quit the application
pygame.quit()
