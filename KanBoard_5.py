import pygame
from pygame.locals import *
import os
import csv
import sys
import tkinter as tk
from tkinter import colorchooser

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 191, 255)
GREY = (220, 220, 220)
background_color = WHITE

#Whiteboard Section

def handle_mouse_button(pos, button_states):
    button_states["black"] = button_states["black_button_rect"].collidepoint(pos)
    button_states["blue"] = button_states["blue_button_rect"].collidepoint(pos)
    button_states["eraser"] = button_states["eraser_button_rect"].collidepoint(pos)
    button_states["clear"] = button_states["clear_button_rect"].collidepoint(pos)
    button_states["slider"] = button_states["slider_width_rect"].collidepoint(pos)
    button_states["color_picker"] = button_states["color_picker_rect"].collidepoint(pos)
    button_states["save"] = button_states["save_button_rect"].collidepoint(pos)
    button_states["load"] = button_states["load_button_rect"].collidepoint(pos)
    button_states["back"] = button_states["back_button_rect"].collidepoint(pos)

    if button_states["whiteboard_rect"].collidepoint(pos):
        start_drawing(pos, button_states)

    if button_states["black"]:
        button_states["color"] = BLACK
    elif button_states["blue"]:
        button_states["color"] = BLUE
    elif button_states["eraser"]:
        button_states["color"] = background_color
    elif button_states["clear"]:
        clear_whiteboard(button_states["whiteboard"])
    elif button_states["save"]:
        save_whiteboard(button_states["whiteboard"])
    elif button_states["load"]:
        load_whiteboard(button_states)
    elif button_states["back"]:
        back_button_action()

    if button_states["color_picker"]:
        button_states["color"] = choose_color()

def back_button_action():
    menu_buttons()
    # Add your code here to handle the action when the "Back" button is clicked

def start_drawing(pos, button_states):
    button_states["drawing"] = True
    button_states["last_pos"] = pos

def handle_mouse_motion(pos, button_states):
    if button_states["dragging"]:
        update_slider_width(pos, button_states)

    if button_states["drawing"]:
        draw(pos, button_states)

def draw(pos, button_states):
    if button_states["drawing"]:
        color = button_states["color"]
        last_pos = button_states["last_pos"]
        distance_x = pos[0] - last_pos[0]
        distance_y = pos[1] - last_pos[1]
        distance = max(abs(distance_x), abs(distance_y))
        step_x = distance_x / distance if distance != 0 else 0
        step_y = distance_y / distance if distance != 0 else 0

        for i in range(distance):
            x = int(last_pos[0] + i * step_x)
            y = int(last_pos[1] + i * step_y)
            pygame.draw.circle(button_states["whiteboard"], color, (x, y), button_states["slider_width"] // 2)

        button_states["last_pos"] = pos

def clear_whiteboard(whiteboard):
    whiteboard.fill(background_color)

def update_slider_width(pos, button_states):
    if button_states["dragging"]:
        if button_states["slider_width_rect"].left <= pos[0] <= button_states["slider_width_rect"].right:
            # Calculate the new slider width based on the mouse position
            slider_width = int((pos[0] - button_states["slider_width_rect"].left) / button_states["slider_width_rect"].width * 19) + 1
            # Limit the slider width to a minimum value of 1
            slider_width = max(slider_width, 5)
            # Limit the slider width to a maximum value of 20 (optional)
            slider_width = min(slider_width, 20)

            # Update the slider width and position
            button_states["slider_width"] = slider_width
            slider_pos = (button_states["slider_width_rect"].left + int((button_states["slider_width"] - 1) / 19 * button_states["slider_width_rect"].width),
                        button_states["slider_width_rect"].centery)
            button_states["slider_pos"] = slider_pos

            # Perform any additional actions based on the updated slider width

def save_whiteboard(whiteboard):
    pygame.image.save(whiteboard, "whiteboard.png")
    print("whiteboard saved as whiteboard.png")

def load_whiteboard(button_states):
    try:
        button_states["whiteboard"] = pygame.image.load("whiteboard.png").convert()
        print("whiteboard loaded from whiteboard.png")
    except pygame.error:
        print("Could not load whiteboard from whiteboard.png")

def choose_color():
    root = tk.Tk()
    root.withdraw()
    color = colorchooser.askcolor()[0]
    return tuple(int(c) for c in color)

def run():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    whiteboard = pygame.Surface((info.current_w, info.current_h))
    whiteboard.fill(background_color)

    # Button properties
    button_states = {
        "whiteboard": whiteboard,
        "whiteboard_rect": pygame.Rect(0, 0, info.current_w, info.current_h),
        "black_button_rect": pygame.Rect(10, 10, 100, 50),
        "blue_button_rect": pygame.Rect(120, 10, 100, 50),
        "color_picker_rect": pygame.Rect(230, 10, 100, 50),  # Added color_picker_rect
        "color_choice_rect": pygame.Rect(340, 10, 100, 50),
        "eraser_button_rect": pygame.Rect(450, 10, 100, 50),
        "clear_button_rect": pygame.Rect(560, 10, 100, 50),
        "save_button_rect": pygame.Rect(670, 10, 100, 50),
        "load_button_rect": pygame.Rect(780, 10, 100, 50),        
        "slider_width_rect": pygame.Rect(890, 10, 200, 20),
        "back_button_rect": pygame.Rect((info.current_w - 100) // 2, info.current_h - 60, 100, 50),
        "drawing": False,
        "last_pos": None,
        "color": BLACK,
        "slider_width": 5,
        "dragging": False,
        "black": False,
        "blue": False,
        "eraser": False,
        "clear": False,
        "slider": False,
        "color_picker": False,
        "back": False
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_button(event.pos, button_states)
                if event.button == 1 and button_states["slider"]:
                    button_states["dragging"] = True
                elif event.button == 1 and button_states["color_picker"]:
                    button_states["color"] = choose_color()
            elif event.type == pygame.MOUSEMOTION:
                handle_mouse_motion(event.pos, button_states)
            elif event.type == pygame.MOUSEBUTTONUP:
                button_states["drawing"] = False
                button_states["dragging"] = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                back_button_action()  # Trigger back button action on Backspace key press

        screen.blit(button_states["whiteboard"], (0, 0))

        # Draw the buttons
        pygame.draw.rect(screen, BLACK, button_states["black_button_rect"])
        pygame.draw.rect(screen, BLUE, button_states["blue_button_rect"])
        pygame.draw.rect(screen, BLACK, button_states["color_picker_rect"])
        pygame.draw.rect(screen, BLACK, button_states["eraser_button_rect"])
        pygame.draw.rect(screen, BLACK, button_states["clear_button_rect"])
        pygame.draw.rect(screen, BLACK, button_states["save_button_rect"])
        pygame.draw.rect(screen, BLACK, button_states["load_button_rect"])
        pygame.draw.rect(screen, button_states["color"], button_states["color_choice_rect"])
        pygame.draw.rect(screen, BLACK, button_states["back_button_rect"])

        # Draw the button labels
        button_font = pygame.font.SysFont("Arial", 20)
        screen.blit(button_font.render("Black", True, WHITE), (button_states["black_button_rect"].x + 10, button_states["black_button_rect"].y + 10))
        screen.blit(button_font.render("Blue", True, WHITE), (button_states["blue_button_rect"].x + 20, button_states["blue_button_rect"].y + 10))
        screen.blit(button_font.render("Eraser", True, WHITE), (button_states["eraser_button_rect"].x + 10, button_states["eraser_button_rect"].y + 10))
        screen.blit(button_font.render("Clear", True, WHITE), (button_states["clear_button_rect"].x + 20, button_states["clear_button_rect"].y + 10))
        screen.blit(button_font.render("Save", True, WHITE), (button_states["save_button_rect"].x + 25, button_states["save_button_rect"].y + 10))
        screen.blit(button_font.render("Load", True, WHITE), (button_states["load_button_rect"].x + 25, button_states["load_button_rect"].y + 10))
        screen.blit(button_font.render("Back", True, WHITE), (button_states["back_button_rect"].x + 25, button_states["back_button_rect"].y + 10))
        screen.blit(button_font.render("RGB", True, WHITE), (button_states["color_picker_rect"].x + 30, button_states["color_picker_rect"].y + 5))
        screen.blit(button_font.render("Selector", True, WHITE), (button_states["color_picker_rect"].x + 20, button_states["color_picker_rect"].y + 25))

        # Draw the slider
        pygame.draw.rect(screen, GREY, button_states["slider_width_rect"])
        pygame.draw.rect(screen, BLACK, button_states["slider_width_rect"], 2)
        slider_pos = (button_states["slider_width_rect"].left + int((button_states["slider_width"] - 1) / 19 * button_states["slider_width_rect"].width),
                    button_states["slider_width_rect"].centery)
        pygame.draw.circle(screen, BLACK, slider_pos, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#Menu Section

def menu_button_action(label):
    if label == "Whiteboard":
        run()
        
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
        pygame.quit()
        sys.exit()

def menu_buttons():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    button_labels = ["Whiteboard", "Kanban Board", "Calendar", "Timer", "Exit"]
    button_width = 200
    button_height = 50
    button_spacing = 20
    button_font = pygame.font.Font(None, 24)
    button_color = (0, 0, 0)
    button_text_color = (255, 255, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    for i, label in enumerate(button_labels):
                        button_rect = pygame.Rect(
                            (screen.get_width() - button_width) // 2,
                            (screen.get_height() - (button_height + button_spacing) * len(button_labels)) // 2
                            + i * (button_height + button_spacing),
                            button_width,
                            button_height
                        )
                        if button_rect.collidepoint(mouse_pos):
                            menu_button_action(label)

        screen.fill((255, 255, 255))

        for i, label in enumerate(button_labels):
            button_rect = pygame.Rect(
                (screen.get_width() - button_width) // 2,
                (screen.get_height() - (button_height + button_spacing) * len(button_labels)) // 2
                + i * (button_height + button_spacing),
                button_width,
                button_height
            )

            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, 3)

            button_text = button_font.render(label, True, button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(30)

#Login Section

def login():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0), FULLSCREEN)
    pygame.display.set_caption("Log into KanBoard.5")
    screen_width, screen_height = pygame.display.get_surface().get_size()

    clock = pygame.time.Clock()
    running = True

    # Text input variables
    username = ""
    password = ""
    active_field = "username"  # To keep track of the active text input field
    username_outline_color = BLACK  # Outline color for username input box
    password_outline_color = BLACK

    # Calculate vertical positions for username and password
    username_y = screen_height // 2 - 50
    password_y = username_y + 100

    # Button variables
    button_signup = pygame.Rect(screen_width // 2 - 50, password_y + 80, 100, 30)
    button_color = BLACK
    button_text = "Sign Up"

    # Invalid Login message variables
    invalid_login_text = ""
    invalid_login_font = pygame.font.Font(None, 24)
    invalid_login_color = (255, 0, 0)
    invalid_login_rect = pygame.Rect(screen_width // 2 - 100, password_y + 120, 200, 30)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if active_field == "username":
                        username = username[:-1]
                    elif active_field == "password":
                        password = password[:-1]
                else:
                    if active_field == "username":
                        username += event.unicode
                    elif active_field == "password":
                        password += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if username_rect.collidepoint(mouse_pos):
                    active_field = "username"
                    username_outline_color = GREY
                    password_outline_color = BLACK
                elif password_rect.collidepoint(mouse_pos):
                    active_field = "password"
                    username_outline_color = BLACK
                    password_outline_color = GREY
                elif button_signup.collidepoint(mouse_pos):
                    folder = os.getcwd()
                    fileName = folder + "\\accounts.csv"
                    with open(fileName, "r") as csvFile:
                        reader = csv.reader(csvFile, delimiter=',')
                        login_validity = False 
                        for line in reader:
                            if username == line[0] and password == line[1]:
                                print("Credentials Matched")
                                login_validity = True
                                invalid_login_text = ""
                                menu_buttons()
    
                            if not login_validity:
                                invalid_login_text = "Invalid Login"

        # Clear the screen
        screen.fill(WHITE)

        # Draw title
        font = pygame.font.Font(None, 48)
        title_text = font.render("Log into KanBoard.5", True, BLACK)
        title_text_rect = title_text.get_rect(center=(screen_width // 2, 350))
        screen.blit(title_text, title_text_rect)

        # Draw username label and input box
        font = pygame.font.Font(None, 36)
        username_label = font.render("Username:", True, BLACK)
        username_label_rect = username_label.get_rect(center=(screen_width // 2, username_y))
        screen.blit(username_label, username_label_rect)

        username_rect = pygame.Rect(screen_width // 2 - 100, username_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, username_rect)
        pygame.draw.rect(screen, username_outline_color, username_rect, 2)  # Use username_outline_color for the outline

        username_text = font.render(username, True, BLACK)
        username_text_rect = username_text.get_rect(center=username_rect.center)
        screen.blit(username_text, username_text_rect)

        # Draw password label and input box
        password_label = font.render("Password:", True, BLACK)
        password_label_rect = password_label.get_rect(center=(screen_width // 2, password_y))
        screen.blit(password_label, password_label_rect)

        password_rect = pygame.Rect(screen_width // 2 - 100, password_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, password_rect)
        pygame.draw.rect(screen, password_outline_color, password_rect, 2)

        password_text = font.render("*" * len(password), True, BLACK)
        password_text_rect = password_text.get_rect(center=password_rect.center)
        screen.blit(password_text, password_text_rect)

        # Draw sign up button
        pygame.draw.rect(screen, button_color, button_signup)
        button_font = pygame.font.Font(None, 24)
        button_text_rendered = button_font.render(button_text, True, WHITE)
        button_text_rect = button_text_rendered.get_rect(center=button_signup.center)
        screen.blit(button_text_rendered, button_text_rect)

        # Draw invalid login message
        invalid_login_rendered = invalid_login_font.render(invalid_login_text, True, invalid_login_color)
        screen.blit(invalid_login_rendered, invalid_login_rect)
        
        pygame.display.flip()
        clock.tick(60)
        

    pygame.quit()


if __name__ == '__main__':
    login()
    
    
    
    
