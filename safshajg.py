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
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

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

load_notes()

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_notes()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                create_note()

        for note in notes:
            handle_event(note, event)

        if event.type == pygame.MOUSEMOTION:
            for note in notes:
                if note['selected']:
                    mouse_pos = pygame.mouse.get_pos()
                    note['x'] = mouse_pos[0] - note['offset'][0]
                    note['y'] = mouse_pos[1] - note['offset'][1]

    screen.fill(WHITE)
    for note in notes:
        draw_note(note)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
