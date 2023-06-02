import pygame
from pygame.locals import *

def values():
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    WHITE = (255, 255, 255)
    background_color = WHITE
    return BLACK, BLUE, WHITE, background_color

class App:
    def __init__(self, BLACK, BLUE, WHITE, background_color):
        pygame.init()
        self.BLACK = BLACK
        self.BLUE = BLUE
        self.WHITE = WHITE
        self.background_color = background_color
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set display mode to fullscreen
        self.WIDTH, self.HEIGHT = self.screen.get_size()
        self.clock = pygame.time.Clock()

    def menu_button_action(self, label):
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

    def menu_buttons(self):
        button_width = 175
        button_height = 30
        button_margin = 20
        button_color = self.BLACK
        button_font = pygame.font.SysFont(None, 25)

        # Create buttons
        button_labels = ["Whiteboard", "Kanban Board", "Calendar", "Timer", "Exit"]
        total_buttons = len(button_labels)
        total_width = total_buttons * (button_width + button_margin) - button_margin
        start_x = (self.WIDTH - total_width) // 2
        start_y = self.HEIGHT - button_height - button_margin

        buttons = []
        for i, label in enumerate(button_labels):
            button_rect = pygame.Rect(start_x + (button_width + button_margin) * i, start_y, button_width, button_height)
            buttons.append((button_rect, label))

        # Create the text surface
        paragraph_font = pygame.font.SysFont(None, 50)
        max_width = self.WIDTH - 100  # Maximum width for the paragraph
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
                text_surface = paragraph_font.render(wrapped_line, True, self.BLACK)
                text_surfaces.append(text_surface)

        # Calculate the starting position for the paragraph to be centered on the screen
        total_height = sum(text_surface.get_height() + 10 for text_surface in text_surfaces)
        start_y = (self.HEIGHT - total_height) // 2

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == MOUSEBUTTONDOWN:
                    for button_rect, label in buttons:
                        if button_rect.collidepoint(event.pos):
                            self.menu_button_action(label)  # Call the corresponding button action function

            self.screen.fill(self.background_color)  # Clear the screen

            # Draw buttons
            for button_rect, label in buttons:
                pygame.draw.rect(self.screen, button_color, button_rect)
                text = button_font.render(label, True, self.WHITE)
                text_rect = text.get_rect(center=button_rect.center)
                self.screen.blit(text, text_rect)

            # Draw paragraph
            y = start_y
            for text_surface in text_surfaces:
                text_rect = text_surface.get_rect(left=50, top=y)  # Set left alignment and specify the top position
                self.screen.blit(text_surface, text_rect)
                y += text_surface.get_height() + 10  # Add spacing between lines

            pygame.display.flip()
            self.clock.tick(60)


    def run(self):
        pygame.display.set_caption("Button Example")  # Set window title
        self.menu_buttons()  # Call the menu_buttons method

        pygame.quit()

if __name__ == "__main__":
    BLACK, BLUE, WHITE, background_color = values()
    app = App(BLACK, BLUE, WHITE, background_color)
    app.run()
