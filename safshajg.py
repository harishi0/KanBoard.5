import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()
pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((0,0),FULLSCREEN)

# Set the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Set the font properties
FONT_SIZE = 24
FONT_NAME = pygame.font.get_default_font()

# Create a Note class
class Note:
    pass
    # Rest of the code...

# Create a Button class
class Button:
    def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 200
            self.height = 200
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.text = ""
            self.selected = False
            self.dragging = False
            self.offset_x = 0
            self.offset_y = 0

    def createNote(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_lines = self.text.split('\n')
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (self.x + 10, self.y + 10 + (i * FONT_SIZE)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:   
            if self.selected:
                if event.key == pygame.K_RETURN:
                    self.text += '\n'
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.x < event.pos[0] < self.x + self.width and self.y < event.pos[1] < self.y + self.height:
                    self.selected = True
                    self.dragging = True
                    self.offset_x = event.pos[0] - self.x
                    self.offset_y = event.pos[1] - self.y
                else:
                    self.selected = False
                    self.dragging = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.x = event.pos[0] - self.offset_x
                self.y = event.pos[1] - self.offset_y

    def update(self):
        if self.selected:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

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
create_button = Button(button_x, button_y, button_width, button_height, button_color, button_text, button_text_color)

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
                note.handle_event(event)

            # Check if the "Create Note" button is clicked
            if create_button.is_clicked(event):
                new_note = Note(random.randint(0, WIDTH - 200), random.randint(0, HEIGHT - 200))
                notes.append(new_note)

    # Clear the screen
    screen.fill(WHITE)

    # Draw notes
    for note in notes:
        note.draw(screen)
        note.update()

    # Draw the "Create Note" button
    create_button.draw(screen)

    # Update the display
    pygame.display.flip()

# Save the current state
save_data = {
    'notes': notes
}
with open('save_file.txt', 'w') as file:
    file.write(str(save_data))
# Load the saved state
with open('save_file.txt', 'r') as file:
    saved_data = file.read()
    if saved_data:
        save_data = eval(saved_data)
        notes = save_data['notes']

# Quit the application
pygame.quit()
