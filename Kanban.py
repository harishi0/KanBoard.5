import pygame
from pygame.locals import *
import random
import json

# Initialize Pygame
pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((0, 0), FULLSCREEN)

# Set the font properties
FONT_SIZE = 24
FONT_NAME = pygame.font.get_default_font()
font = pygame.font.Font(FONT_NAME, FONT_SIZE)

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

notes = []  # List to store notes

def draw_note(note):
    if note['selected']:
        pygame.draw.rect(screen, YELLOW, (note['x'] - 5, note['y'] - 5, note['width'] + 10, note['height'] + 10))
    pygame.draw.rect(screen, note['color'], (note['x'], note['y'], note['width'], note['height']))
    text_lines = note['text'].split('\n')
    for i, line in enumerate(text_lines):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (note['x'] + 10, note['y'] + 10 + (i * FONT_SIZE)))

def handle_event(note, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = pygame.mouse.get_pos()
        if event.button == 1:
            if note['selected']:
                note['selected'] = False
            elif note['x'] <= mouse_pos[0] <= note['x'] + note['width'] and note['y'] <= mouse_pos[1] <= note['y'] + note['height']:
                note['selected'] = True
                note['offset'] = (mouse_pos[0] - note['x'], mouse_pos[1] - note['y'])
        elif event.button == 3:
            if note['x'] <= mouse_pos[0] <= note['x'] + note['width'] and note['y'] <= mouse_pos[1] <= note['y'] + note['height']:
                note['color'] = random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA])
    elif event.type == pygame.KEYDOWN and note['selected']:
        if event.key == pygame.K_BACKSPACE:
            if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                notes.remove(note)
            else:
                note['text'] = note['text'][:-1]
        elif event.key == pygame.K_RETURN:
            note['text'] += '\n'
        else:
            note['text'] += event.unicode
    


def save_notes():
    data = []
    for note in notes:
        data.append({
            'x': note['x'],
            'y': note['y'],
            'text': note['text']
        })
    with open('notes.json', 'w') as file:
        json.dump(data, file)

def load_notes():
    try:
        with open('notes.json', 'r') as file:
            data = json.load(file)
            for note_data in data:
                note = {
                    'x': note_data['x'],
                    'y': note_data['y'],
                    'width': 200,
                    'height': 200,
                    'color': random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]),
                    'selected': False,
                    'text': note_data['text']
                }
                notes.append(note)
    except FileNotFoundError:
        pass
    
def create_note():
    note = {
        'x': random.randint(0, WIDTH - 200),
        'y': random.randint(0, HEIGHT - 200),
        'width': 200,
        'height': 200,
        'color': random.choice([RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]),
        'selected': False,
        'text': ""
    }
    notes.append(note)

def draw_button(x, y, width, height, color, text, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

def draw_kanban_board():
    num_columns = 3  # Number of Kanban board columns
    column_width = WIDTH // num_columns

    # Define the titles for each category
    titles = ["To Do", "In Progress", "Done"]

    for i in range(num_columns):
        x = i * column_width
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), 2)

        # Draw the title for the current category
        title_surface = font.render(titles[i], True, BLACK)
        title_x = x + (column_width - title_surface.get_width()) // 2
        title_y = 65
        screen.blit(title_surface, (title_x, title_y))


# Create the "Create Note" button
button_width = 150
button_height = 50
button_x = (WIDTH - button_width) // 2
button_y = 10
button_color = GRAY
button_text = "Create Note"
button_text_color = BLACK

# Calculate the spacing between buttons
button_spacing = 10

# Calculate the positions of the buttons
save_button_x = button_x - button_width - button_spacing
clear_button_x = button_x + button_width + button_spacing

# Create the "Save" button
save_button_width = 150
save_button_height = 50
save_button_y = button_y
save_button_color = GRAY
save_button_text = "Save"
save_button_text_color = BLACK

# Create the "Clear" button
clear_button_width = 150
clear_button_height = 50
clear_button_y = button_y
clear_button_color = GRAY
clear_button_text = "Clear"
clear_button_text_color = BLACK

# Calculate the position of the "Load" button
load_button_x = clear_button_x + clear_button_width + button_spacing

# Create the "Load" button
load_button_width = 150
load_button_height = 50
load_button_y = button_y
load_button_color = GRAY
load_button_text = "Load"
load_button_text_color = BLACK

load_notes()

def runkanban():
    # Main game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_notes()
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                        for note in notes:
                            if note['selected']:
                                notes.remove(note)

            for note in notes:
                handle_event(note, event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                        create_note()
                    elif save_button_x <= mouse_pos[0] <= save_button_x + save_button_width and save_button_y <= mouse_pos[1] <= save_button_y + save_button_height:
                        save_notes()
                    elif load_button_x <= mouse_pos[0] <= load_button_x + load_button_width and load_button_y <= mouse_pos[1] <= load_button_y + load_button_height:
                        load_notes()
                    elif clear_button_x <= mouse_pos[0] <= clear_button_x + clear_button_width and clear_button_y <= mouse_pos[1] <= clear_button_y + clear_button_height:
                        notes.clear()

            if event.type == pygame.MOUSEMOTION:
                for note in notes:
                    if note['selected']:
                        mouse_pos = pygame.mouse.get_pos()
                        note['x'] = mouse_pos[0] - note['offset'][0]
                        note['y'] = mouse_pos[1] - note['offset'][1]

        screen.fill(WHITE)
        draw_kanban_board()
        draw_button(button_x, button_y, button_width, button_height, button_color, button_text, button_text_color)
        draw_button(save_button_x, save_button_y, save_button_width, save_button_height, save_button_color, save_button_text, save_button_text_color)
        draw_button(load_button_x, load_button_y, load_button_width, load_button_height, load_button_color, load_button_text, load_button_text_color)
        draw_button(clear_button_x, clear_button_y, clear_button_width, clear_button_height, clear_button_color, clear_button_text, clear_button_text_color)
        for note in notes:
            draw_note(note)

        pygame.display.flip()

runkanban()
pygame.quit()
