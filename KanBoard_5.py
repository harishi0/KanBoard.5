import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tab System Example")

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)

# Define tab contents
tabs = {
    "Tab 1": "This is the content of Tab 1",
    "Tab 2": "This is the content of Tab 2",
    "Tab 3": "This is the content of Tab 3"
}
current_tab = "Tab 1"

# Function to draw the current tab content
def draw_tab_content():
    text = font.render(tabs[current_tab], True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    window.blit(text, text_rect)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tab = "Tab 1"

                BLACK = (0, 0, 0)
                BLUE = (0, 191, 255)
                WHITE = (255, 255, 255)
                background_color = WHITE

                class WhiteboardApp:
                    WIDTH = 0
                    HEIGHT = 0

                    def __init__(user):
                        user.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        user.clock = pygame.time.Clock()
                        user.drawing = False
                        user.last_pos = None
                        user.canvas = pygame.Surface((WhiteboardApp.WIDTH, WhiteboardApp.HEIGHT))
                        user.canvas.fill(background_color)
                        user.current_color = BLACK
                        pygame.font.init()  # Initialize the font module
                        user.button_font = pygame.font.SysFont("Arial", 20)

                        user.black_button_rect = pygame.Rect(10, 10, 100, 50)
                        user.blue_button_rect = pygame.Rect(120, 10, 100, 50)
                        user.clear_button_rect = pygame.Rect(230, 10, 100, 50)
                        user.save_button_rect = pygame.Rect(340, 10, 100, 50)
                        user.load_button_rect = pygame.Rect(450, 10, 100, 50)
                        user.eraser_button_rect = pygame.Rect(560, 10, 100, 50)

                        user.button_labels = {
                            "Black": (user.black_button_rect.x + 10, user.black_button_rect.y + 10),
                            "Blue": (user.blue_button_rect.x + 10, user.blue_button_rect.y + 10),
                            "Clear": (user.clear_button_rect.x + 10, user.clear_button_rect.y + 10),
                            "Save": (user.save_button_rect.x + 10, user.save_button_rect.y + 10),
                            "Load": (user.load_button_rect.x + 10, user.load_button_rect.y + 10),
                            "Eraser": (user.eraser_button_rect.x + 10, user.eraser_button_rect.y + 10)
                        }

                        user.button_selected = None
                        user.eraser_selected = False

                        user.slider_width_rect = pygame.Rect(680, 10, 200, 20)
                        user.slider_width_value = 10
                        user.slider_dragging = False

                    def run(user):
                        pygame.init()
                        screen_info = pygame.display.Info()
                        WhiteboardApp.WIDTH = screen_info.current_w
                        WhiteboardApp.HEIGHT = screen_info.current_h

                        user.screen = pygame.display.set_mode((WhiteboardApp.WIDTH, WhiteboardApp.HEIGHT), pygame.FULLSCREEN)

                        running = True
                        while running:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    running = False
                                elif event.type == pygame.MOUSEBUTTONDOWN:
                                    user.handle_mouse_button(event.pos)
                                elif event.type == pygame.MOUSEMOTION:
                                    user.handle_mouse_motion(event.pos)
                                elif event.type == pygame.MOUSEBUTTONUP:
                                    user.stop_drawing()
                                    user.stop_dragging()

                            user.screen.fill(BLUE)
                            user.screen.blit(user.canvas, (0, 0))

                            pygame.draw.rect(user.screen, BLACK, user.black_button_rect, 3 if user.button_selected == "Black" else 0)
                            pygame.draw.rect(user.screen, BLUE, user.blue_button_rect, 3 if user.button_selected == "Blue" else 0)
                            pygame.draw.rect(user.screen, BLACK, user.clear_button_rect, 3 if user.button_selected == "Clear" else 0)
                            pygame.draw.rect(user.screen, BLACK, user.save_button_rect, 3 if user.button_selected == "Save" else 0)
                            pygame.draw.rect(user.screen, BLACK, user.load_button_rect, 3 if user.button_selected == "Load" else 0)
                            pygame.draw.rect(user.screen, BLACK, user.eraser_button_rect, 3 if user.eraser_selected else 0)

                            for button, label_pos in user.button_labels.items():
                                user.screen.blit(user.button_font.render(button, True, WHITE), label_pos)

                            pygame.draw.rect(user.screen, BLACK, user.slider_width_rect, 3)
                            pygame.draw.circle(user.screen, BLACK,
                                            (user.slider_width_rect.left + user.slider_width_value * 10, user.slider_width_rect.centery),
                                            user.slider_width_value // 2)

                            pygame.display.flip()
                            user.clock.tick(60)

                        pygame.quit()

                    def handle_mouse_button(user, pos):
                        if user.black_button_rect.collidepoint(pos):
                            user.button_selected = "Black"
                            user.current_color = BLACK
                            user.eraser_selected = False
                        elif user.blue_button_rect.collidepoint(pos):
                            user.button_selected = "Blue"
                            user.current_color = BLUE
                            user.eraser_selected = False
                        elif user.clear_button_rect.collidepoint(pos):
                            user.button_selected = "Clear"
                            user.clear_canvas()
                            user.eraser_selected = False
                        elif user.save_button_rect.collidepoint(pos):
                            user.button_selected = "Save"
                            user.save_canvas()
                            user.eraser_selected = False
                        elif user.load_button_rect.collidepoint(pos):
                            user.button_selected = "Load"
                            user.load_canvas()
                            user.eraser_selected = False
                        elif user.eraser_button_rect.collidepoint(pos):
                            user.eraser_selected = True

                        if user.slider_width_rect.collidepoint(pos):
                            user.start_dragging(pos)

                        if user.canvas.get_rect().collidepoint(pos):
                            user.start_drawing(pos)

                    def handle_mouse_motion(user, pos):
                        if user.drawing:
                            user.draw(pos)
                        if user.slider_dragging:
                            user.update_slider_width(pos)

                    def start_drawing(user, pos):
                        if user.black_button_rect.collidepoint(pos) or user.blue_button_rect.collidepoint(pos) \
                                or user.clear_button_rect.collidepoint(pos) or user.save_button_rect.collidepoint(pos) \
                                or user.load_button_rect.collidepoint(pos) or user.slider_width_rect.collidepoint(pos) \
                                or user.eraser_button_rect.collidepoint(pos):
                            return

                        user.drawing = True
                        user.last_pos = pos

                    def draw(user, pos):
                        if user.drawing:
                            if user.eraser_selected:
                                color = background_color
                            else:
                                color = user.current_color

                            distance_x = pos[0] - user.last_pos[0]
                            distance_y = pos[1] - user.last_pos[1]
                            distance = max(abs(distance_x), abs(distance_y))
                            step_x = distance_x / distance if distance != 0 else 0
                            step_y = distance_y / distance if distance != 0 else 0

                            for i in range(distance):
                                x = int(user.last_pos[0] + i * step_x)
                                y = int(user.last_pos[1] + i * step_y)
                                pygame.draw.circle(user.canvas, color, (x, y), user.slider_width_value // 2)

                            user.last_pos = pos

                    def stop_drawing(user):
                        user.drawing = False

                    def start_dragging(user, pos):
                        user.slider_dragging = True
                        user.update_slider_width(pos)

                    def stop_dragging(user):
                        user.slider_dragging = False

                    def update_slider_width(user, pos):
                        if user.slider_dragging:
                            if user.slider_width_rect.left <= pos[0] <= user.slider_width_rect.right:
                                relative_pos = pos[0] - user.slider_width_rect.left
                                normalized_pos = relative_pos / user.slider_width_rect.width
                                user.slider_width_value = max(2, int(normalized_pos * 19) + 1)

                    def clear_canvas(user):
                        user.canvas.fill(background_color)

                    def save_canvas(user):
                        pygame.image.save(user.canvas, "canvas.png")

                    def load_canvas(user):
                        try:
                            user.canvas = pygame.image.load("canvas.png")
                        except pygame.error:
                            print("Unable to load image")


                if __name__ == "__main__":
                    pygame.init()  # Initialize Pygame
                    screen_info = pygame.display.Info()
                    WhiteboardApp.WIDTH = screen_info.current_w
                    WhiteboardApp.HEIGHT = screen_info.current_h

                    app = WhiteboardApp()
                    app.run()
            elif event.key == pygame.K_2:
                current_tab = "Tab 2"
                # Initialize Pygame
                pygame.init()

                # Board dimensions
                BOARD_WIDTH = 800
                BOARD_HEIGHT = 600

                # Colors
                BLACK = (0, 0, 0)
                WHITE = (255, 255, 255)
                GRAY = (200, 200, 200)
                RED = (255, 0, 0)
                BLUE = (0, 0, 255)
                GREEN = (0, 255, 0)

                # Sticky note dimensions
                NOTE_WIDTH = 100
                NOTE_HEIGHT = 100

                # Sticky note class
                class StickyNote:
                    def __init__(self, position, color, category):
                        self.position = position
                        self.color = color
                        self.category = category
                        self.text = ""  # Initialize an empty text content

                    def draw(self, screen):
                        pygame.draw.rect(screen, self.color, (*self.position, NOTE_WIDTH, NOTE_HEIGHT))
                        pygame.draw.rect(screen, BLACK, (*self.position, NOTE_WIDTH, NOTE_HEIGHT), 2)

                        font = pygame.font.SysFont(None, 18)
                        lines = self.text.split("\n")
                        for i, line in enumerate(lines):
                            text_surface = font.render(line, True, BLACK)
                            screen.blit(text_surface, (self.position[0] + 10, self.position[1] + 10 + i * 20))

                # Create the game window
                screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
                pygame.display.set_caption("Kanban Board")

                # List of sticky notes
                sticky_notes = []

                # Button dimensions
                BUTTON_WIDTH = 100
                BUTTON_HEIGHT = 40

                # Create the add button
                add_button_rect = pygame.Rect(20, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
                add_button_color = GREEN

                # Selected sticky note for dragging
                selected_note = None
                offset_x = 0
                offset_y = 0

                # Active sticky note for typing
                active_note = None

                # Main game loop
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False

                        # Handle mouse button events
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()

                            # Add a new sticky note when add button is clicked
                            if event.button == 1 and add_button_rect.collidepoint(mouse_pos):
                                new_note = StickyNote((50, 50), WHITE, "Backlog")
                                sticky_notes.append(new_note)

                            # Check if mouse is over a sticky note
                            for note in sticky_notes:
                                note_rect = pygame.Rect(*note.position, NOTE_WIDTH, NOTE_HEIGHT)
                                if note_rect.collidepoint(mouse_pos):
                                    selected_note = note
                                    offset_x = mouse_pos[0] - note.position[0]
                                    offset_y = mouse_pos[1] - note.position[1]
                                    active_note = note

                        elif event.type == pygame.MOUSEBUTTONUP:
                            if event.button == 1:
                                selected_note = None

                        elif event.type == pygame.MOUSEMOTION:
                            if selected_note is not None:
                                mouse_pos = pygame.mouse.get_pos()
                                selected_note.position = (mouse_pos[0] - offset_x, mouse_pos[1] - offset_y)

                        # Handle text input events
                        elif event.type == pygame.KEYDOWN:
                            if active_note is not None:
                                if event.key == pygame.K_BACKSPACE:
                                    active_note.text = active_note.text[:-1]  # Remove the last character
                                elif event.key == pygame.K_RETURN:
                                    active_note.text += "\n"  # Add a new line
                                else:
                                    active_note.text += event.unicode  # Append the typed character

                    # Clear the screen
                    screen.fill(WHITE)

                    BOARD_WIDTH = 1000

                    # Adjust the positions of existing columns
                    pygame.draw.rect(screen, GRAY, (50, 50, 200, BOARD_HEIGHT - 100))
                    pygame.draw.rect(screen, GRAY, (300, 50, 200, BOARD_HEIGHT - 100))
                    pygame.draw.rect(screen, GRAY, (550, 50, 200, BOARD_HEIGHT - 100))

                    # Add the new column
                    pygame.draw.rect(screen, GRAY, (800, 50, 200, BOARD_HEIGHT - 100))


                    # Draw the add button
                    pygame.draw.rect(screen, add_button_color, add_button_rect)
                    add_button_text = pygame.font.SysFont(None, 24).render("Add Note", True, BLACK)
                    screen.blit(add_button_text, (30, 30))

                    # Draw the sticky notes
                    for note in sticky_notes:
                        note.draw(screen)

                    # Update the screen
                    pygame.display.flip()

                # Quit the game
                pygame.quit()
            elif event.key == pygame.K_3:
                current_tab = "Tab 3"

    # Clear the screen
    window.fill(WHITE)

    # Draw the tab content
    draw_tab_content()

    # Draw the tab labels
    for i, tab_label in enumerate(tabs.keys()):
        text = font.render(tab_label, True, BLACK if tab_label == current_tab else WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2 + (i - 1) * 100, 50))
        pygame.draw.rect(window, BLACK if tab_label == current_tab else WHITE, text_rect, 2)
        window.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()