import pygame
from pygame.locals import *

def values():
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    WHITE = (255, 255, 255)
    background_color = WHITE
    return BLACK, BLUE, WHITE, background_color

def menu_button_action(label):
    if label == "Whiteboard":
        print("Whiteboard button clicked")
    elif label == "Kanban Board":
        print("Kanban Board button clicked")
        # Add code for the action of the Kanban Board button
    elif label == "Calendar":
        print("Calendar button clicked")
        # Add code for the action of the Calendar button
    elif label == "Timer":
        print("Timer button clicked")
        # Add code for the action of the Timer button
    elif label == "Exit":
        exit()

def menu_buttons():
    BLACK, BLUE, WHITE, background_color = values()
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set display mode to fullscreen
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    button_width = 175
    button_height = 30
    button_margin = 20
    button_color = BLACK
    button_font = pygame.font.SysFont(None, 25)

    # Create buttons
    button_labels = ["Whiteboard", "Kanban Board", "Calendar", "Timer", "Exit"]
    total_buttons = len(button_labels)
    total_width = total_buttons * (button_width + button_margin) - button_margin
    start_x = (WIDTH - total_width) // 2
    start_y = HEIGHT - button_height - button_margin

    buttons = []
    for i, label in enumerate(button_labels):
        button_rect = pygame.Rect(start_x + (button_width + button_margin) * i, start_y, button_width, button_height)
        buttons.append((button_rect, label))

    # Create the text surface
    paragraph_font = pygame.font.SysFont(None, 50)
    max_width = WIDTH - 100  # Maximum width for the paragraph
    text_lines = ["This application is a multi-purpose organizational tool for students and employees. This app has a Kanban Board for planning your steps, a Whiteboard to unleash your creativity, a Calendar to schedule your projects, and a Timer to ensure specific timings."]
    
    # Render the paragraph as wrapped text
    text_surfaces = []
    for line in text_lines:
        words = line.split()
        wrapped_lines = []
        current_line = ""
        for word in words:
            if paragraph_font.size(current_line + " " + word)[0] <= max_width:
                current_line += " " + word if current_line else word
            else:
                wrapped_lines.append(current_line)
                current_line = word
        wrapped_lines.append(current_line)
        
        for wrapped_line in wrapped_lines:
            text_surface = paragraph_font.render(wrapped_line, True, BLACK)
            text_surfaces.append(text_surface)

    # Calculate the starting position for the paragraph to be centered on the screen
    total_height = sum(text_surface.get_height() + 10 for text_surface in text_surfaces)
    start_y = (HEIGHT - total_height) // 2

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN:
                for button_rect, label in buttons:
                    if button_rect.collidepoint(event.pos):
                        menu_button_action(label)  # Call the corresponding button action function

        screen.fill(background_color)  # Clear the screen

        # Draw buttons
        for button_rect, label in buttons:
            pygame.draw.rect(screen, button_color, button_rect)
            text = button_font.render(label, True, WHITE)
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)

        # Draw paragraph
        y = start_y
        for text_surface in text_surfaces:
            text_rect = text_surface.get_rect(left=50, top=y)  # Set left alignment and specify the top position
            screen.blit(text_surface, text_rect)
            y += text_surface.get_height() + 10  # Add spacing between lines

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    menu_buttons()
    pygame.quit()