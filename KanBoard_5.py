import pygame
from pygame.locals import *

def values():
    WIDTH = 0
    HEIGHT = 0
    BLACK = (0, 0, 0)
    BLUE = (0, 191, 255)
    WHITE = (255, 255, 255)
    background_color = WHITE
    return WIDTH, HEIGHT, BLACK, BLUE, WHITE, background_color

class Menu:
    def __init__(self, background_color):
        self.background_color = background_color
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.font.init()

    def create_buttons(self):
        # Define the buttons
        button_width = 100
        button_height = 30
        button_margin = 10

        total_width = 4 * button_width + 3 * button_margin
        start_x = (Menu.WIDTH - total_width) // 2
        tab_y = button_margin

        self.tab1 = pygame.Rect(start_x, tab_y, button_width, button_height)
        self.tab2 = pygame.Rect(start_x + button_width + button_margin, tab_y, button_width, button_height)
        self.tab3 = pygame.Rect(start_x + 2 * (button_width + button_margin), tab_y, button_width, button_height)
        self.tab4 = pygame.Rect(start_x + 3 * (button_width + button_margin), tab_y, button_width, button_height)

        pygame.draw.rect(self.screen, values()[2], self.tab1)  # Draw the button with the BLACK color
        pygame.draw.rect(self.screen, values()[2], self.tab2)
        pygame.draw.rect(self.screen, values()[2], self.tab3)
        pygame.draw.rect(self.screen, values()[2], self.tab4)

        button_font = pygame.font.SysFont("Arial", 15)
        text1 = button_font.render("Kanban Board", True, values()[4])
        text2 = button_font.render("Whiteboard", True, values()[4])
        text3 = button_font.render("Calendar", True, values()[4])
        text4 = button_font.render("Timer", True, values()[4])

        text1_rect = text1.get_rect(center=self.tab1.center)
        text2_rect = text2.get_rect(center=self.tab2.center)
        text3_rect = text3.get_rect(center=self.tab3.center)
        text4_rect = text4.get_rect(center=self.tab4.center)

        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(text3, text3_rect)
        self.screen.blit(text4, text4_rect)

    def kanban_board_function(self):
        print("Kanban Board functionality")

    def whiteboard_function(self, WIDTH, HEIGHT, BLACK, BLUE, WHITE, background_color):
        class WhiteboardApp:
            def __init__(self):
                pygame.init()
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Set display mode to fullscreen
                self.clock = pygame.time.Clock()
                self.drawing = False
                self.last_pos = None
                self.canvas = pygame.Surface((WIDTH, HEIGHT))
                self.canvas.fill(background_color)

                # Button properties
                self.black_button_rect = pygame.Rect(10, 10, 100, 50)
                self.blue_button_rect = pygame.Rect(120, 10, 100, 50)
                self.eraser_button_rect = pygame.Rect(230, 10, 100, 50)
                self.clear_button_rect = pygame.Rect(340, 10, 100, 50)
                self.save_button_rect = pygame.Rect(450, 10, 100, 50)
                self.load_button_rect = pygame.Rect(560, 10, 100, 50)
                self.black_button_selected = False
                self.blue_button_selected = False
                self.eraser_button_selected = False
                self.clear_button_selected = False

                # Button labels
                self.button_font = pygame.font.SysFont("Arial", 20)

                # Slider properties
                self.slider_width_rect = pygame.Rect(680, 10, 200, 20)
                self.slider_width_value = 5
                self.slider_dragging = False  # Indicates if the slider is being dragged

            def run(self):
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.handle_mouse_button(event.pos)
                        elif event.type == pygame.MOUSEMOTION:
                            self.handle_mouse_motion(event.pos)
                        elif event.type == pygame.MOUSEBUTTONUP:
                            self.stop_drawing()
                            self.stop_dragging()

                    self.screen.fill(BLUE)
                    self.screen.blit(self.canvas, (0, 0))
                    self.create_buttons()

                    # Draw the buttons
                    pygame.draw.rect(self.screen, BLACK, self.black_button_rect, 3 if self.black_button_selected else 0)
                    pygame.draw.rect(self.screen, BLUE, self.blue_button_rect, 3 if self.blue_button_selected else 0)
                    pygame.draw.rect(self.screen, BLACK, self.eraser_button_rect, 3 if self.eraser_button_selected else 0)
                    pygame.draw.rect(self.screen, BLACK, self.clear_button_rect, 3 if self.clear_button_selected else 0)
                    pygame.draw.rect(self.screen, BLACK, self.save_button_rect)
                    pygame.draw.rect(self.screen, BLACK, self.load_button_rect)

                    # Draw the button labels
                    self.screen.blit(self.button_font.render("Black", True, WHITE), (self.black_button_rect.x + 10, self.black_button_rect.y + 10))
                    self.screen.blit(self.button_font.render("Blue", True, WHITE), (self.blue_button_rect.x + 10, self.blue_button_rect.y + 10))
                    self.screen.blit(self.button_font.render("Eraser", True, WHITE), (self.eraser_button_rect.x + 10, self.eraser_button_rect.y + 10))
                    self.screen.blit(self.button_font.render("Clear", True, WHITE), (self.clear_button_rect.x + 10, self.clear_button_rect.y + 10))
                    self.screen.blit(self.button_font.render("Save", True, WHITE), (self.save_button_rect.x + 10, self.save_button_rect.y + 10))
                    self.screen.blit(self.button_font.render("Load", True, WHITE), (self.load_button_rect.x + 10, self.load_button_rect.y + 10))

                    # Draw the slider
                    pygame.draw.rect(self.screen, BLACK, self.slider_width_rect, 2)
                    slider_pos = self.slider_width_rect.x + int((self.slider_width_value - 1) / 19 * self.slider_width_rect.width)
                    pygame.draw.circle(self.screen, BLACK, (slider_pos, self.slider_width_rect.centery), 9)

                    pygame.display.flip()
                    self.clock.tick(60)

                pygame.quit()

            def handle_mouse_button(self, pos):
                if self.black_button_rect.collidepoint(pos):
                    # Black button is clicked, change marker color to black
                    self.black_button_selected = True
                    self.blue_button_selected = False
                    self.eraser_button_selected = False
                    self.clear_button_selected = False
                elif self.blue_button_rect.collidepoint(pos):
                    # Blue button is clicked, change marker color to blue
                    self.black_button_selected = False
                    self.blue_button_selected = True
                    self.eraser_button_selected = False
                    self.clear_button_selected = False
                elif self.eraser_button_rect.collidepoint(pos):
                    # Eraser button is clicked, change marker color to white
                    self.black_button_selected = False
                    self.blue_button_selected = False
                    self.eraser_button_selected = True
                    self.clear_button_selected = False
                elif self.clear_button_rect.collidepoint(pos):
                    # Clear button is clicked, clear the canvas
                    self.canvas.fill(background_color)
                    self.black_button_selected = False
                    self.blue_button_selected = False
                    self.eraser_button_selected = False
                    self.clear_button_selected = True
                elif self.save_button_rect.collidepoint(pos):
                    # Save button is clicked, save the canvas
                    self.save_canvas()
                elif self.load_button_rect.collidepoint(pos):
                    # Load button is clicked, load the canvas
                    self.load_canvas()
                elif self.slider_width_rect.collidepoint(pos):
                    # Slider is clicked, start dragging the slider
                    self.start_dragging(pos)

                if self.canvas.get_rect().collidepoint(pos):
                    # Mouse is clicked inside the canvas area, start drawing
                    self.start_drawing(pos)

            def handle_mouse_motion(self, pos):
                if self.drawing:
                    self.draw(pos)
                if self.slider_dragging:
                    self.update_slider_width(pos)

            def start_drawing(self, pos):
                self.drawing = True
                self.last_pos = pos

            def draw(self, pos):
                if self.drawing:
                    if self.eraser_button_selected:
                        color = background_color
                    else:
                        color = BLACK if self.black_button_selected else BLUE

                    # Calculate the distance and direction between current and last position
                    distance_x = pos[0] - self.last_pos[0]
                    distance_y = pos[1] - self.last_pos[1]
                    distance = max(abs(distance_x), abs(distance_y))
                    step_x = distance_x / distance if distance != 0 else 0
                    step_y = distance_y / distance if distance != 0 else 0

                    # Interpolate and draw points between current and last position
                    for i in range(distance):
                        x = int(self.last_pos[0] + i * step_x)
                        y = int(self.last_pos[1] + i * step_y)
                        pygame.draw.circle(self.canvas, color, (x, y), self.slider_width_value // 2)

                    self.last_pos = pos

            def stop_drawing(self):
                self.drawing = False

            def start_dragging(self, pos):
                self.slider_dragging = True
                self.update_slider_width(pos)

            def stop_dragging(self):
                self.slider_dragging = False

            def update_slider_width(self, pos):
                if self.slider_dragging:
                    if self.slider_width_rect.left <= pos[0] <= self.slider_width_rect.right:
                        self.slider_width_value = int((pos[0] - self.slider_width_rect.left) / self.slider_width_rect.width * 19) + 1

            def save_canvas(self):
                pygame.image.save(self.canvas, "whiteboard.png")
                print("Canvas saved as whiteboard.png")

            def load_canvas(self):
                try:
                    self.canvas = pygame.image.load("whiteboard.png").convert()
                    print("Canvas loaded from whiteboard.png")
                except pygame.error:
                    print("Could not load canvas from whiteboard.png")

        if __name__ == "__main__":
            app = WhiteboardApp()
            app.run()
        
    def calendar_function(self):
        print("Calendar functionality")

    def timer_function(self):
        print("Timer functionality")

    def handle_event(self, event):
        if event.type == QUIT:
            return False
        elif event.type == MOUSEBUTTONDOWN:
            if self.tab1.collidepoint(event.pos):
                self.kanban_board_function()
            elif self.tab2.collidepoint(event.pos):
                self.whiteboard_function()
            elif self.tab3.collidepoint(event.pos):
                self.calendar_function()
            elif self.tab4.collidepoint(event.pos):
                self.timer_function()
        return True

    def run(self):
        screen_info = pygame.display.Info()
        Menu.WIDTH = screen_info.current_w
        Menu.HEIGHT = screen_info.current_h
        self.screen = pygame.display.set_mode((Menu.WIDTH, Menu.HEIGHT), pygame.FULLSCREEN)
        running = True
        while running:
            for event in pygame.event.get():
                running = self.handle_event(event)

            self.screen.fill(self.background_color)  # Fill the screen with the background color

            self.create_buttons()

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame
    screen_info = pygame.display.Info()
    Menu.WIDTH = screen_info.current_w
    Menu.HEIGHT = screen_info.current_h

    app = Menu(values()[-1])  # Pass the background_color from values()
    app.run()  # Call the run method