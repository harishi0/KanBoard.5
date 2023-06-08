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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
background_color = WHITE

screen = pygame.display.set_mode((0, 0), FULLSCREEN)

#Whiteboard Section

def mouse_button_action(pos, button_choice, username):
    button_choice["black"] = button_choice["black_button_rect"].collidepoint(pos)
    button_choice["blue"] = button_choice["blue_button_rect"].collidepoint(pos)
    button_choice["eraser"] = button_choice["eraser_button_rect"].collidepoint(pos)
    button_choice["clear"] = button_choice["clear_button_rect"].collidepoint(pos)
    button_choice["slider"] = button_choice["slider_width_rect"].collidepoint(pos)
    button_choice["rgb_picker"] = button_choice["rgb_picker_rect"].collidepoint(pos)
    button_choice["save"] = button_choice["save_button_rect"].collidepoint(pos)
    button_choice["load"] = button_choice["load_button_rect"].collidepoint(pos)
    button_choice["back"] = button_choice["back_button_rect"].collidepoint(pos)

    if button_choice["whiteboard_rect"].collidepoint(pos):
        drawing(pos, button_choice)

    if button_choice["black"]:
        button_choice["color"] = BLACK
    elif button_choice["blue"]:
        button_choice["color"] = BLUE
    elif button_choice["eraser"]:
        button_choice["color"] = background_color
    elif button_choice["clear"]:
        clear_whiteboard(button_choice["whiteboard"])
    elif button_choice["save"]:
        save_whiteboard(button_choice["whiteboard"], username)
    elif button_choice["load"]:
        load_whiteboard(button_choice, username)
    elif button_choice["back"]:
        back_button_action(username)

    if button_choice["rgb_picker"]:
        button_choice["color"] = choose_color()

def back_button_action(username):
    menu_buttons(username)
    # Add your code here to handle the action when the "Back" button is clicked

def drawing(pos, button_choice):
    button_choice["drawing"] = True
    button_choice["last_pos"] = pos

def slider_motion(pos, button_choice):
    if button_choice["drag_slider"]:
        update_slider_width(pos, button_choice)

    if button_choice["drawing"]:
        draw(pos, button_choice)

def draw(pos, button_choice):
    if button_choice["drawing"]:
        color = button_choice["color"]
        last_pos = button_choice["last_pos"]
        distance_x = pos[0] - last_pos[0]
        distance_y = pos[1] - last_pos[1]
        distance = max(abs(distance_x), abs(distance_y))
        step_x = distance_x / distance if distance != 0 else 0
        step_y = distance_y / distance if distance != 0 else 0

        for i in range(distance):
            x = int(last_pos[0] + i * step_x)
            y = int(last_pos[1] + i * step_y)
            pygame.draw.circle(button_choice["whiteboard"], color, (x, y), button_choice["slider_width"] // 2)

        button_choice["last_pos"] = pos

def clear_whiteboard(whiteboard):
    whiteboard.fill(background_color)

def update_slider_width(pos, button_choice):
    if button_choice["drag_slider"]:
        if button_choice["slider_width_rect"].left <= pos[0] <= button_choice["slider_width_rect"].right:
            # Calculate the new slider width based on the mouse position
            slider_width = int((pos[0] - button_choice["slider_width_rect"].left) / button_choice["slider_width_rect"].width * 19) + 1
            # Limit the slider width to a minimum value of 1
            slider_width = max(slider_width, 5)
            # Limit the slider width to a maximum value of 20 (optional)
            slider_width = min(slider_width, 20)

            # Update the slider width and position
            button_choice["slider_width"] = slider_width
            slider_pos = (button_choice["slider_width_rect"].left + int((button_choice["slider_width"] - 1) / 19 * button_choice["slider_width_rect"].width),
                        button_choice["slider_width_rect"].centery)
            button_choice["slider_pos"] = slider_pos

            # Perform any additional actions based on the updated slider width

def save_whiteboard(whiteboard, username):
    folder_path = os.path.join("user_data", username)  # Create a folder path based on the username
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
    file_name = os.path.join(folder_path, f"{username}_whiteboard.png")  # Use the folder path to create the file_name
    pygame.image.save(whiteboard, file_name)
    confirm_save_font = pygame.font.Font(None, 36)
    confirm_save_text = confirm_save_font.render("Whiteboard saved", True, GREEN)
    confirm_save_text_rect = confirm_save_text.get_rect(center=screen.get_rect().center)
    screen.blit(confirm_save_text, confirm_save_text_rect)
    pygame.display.flip()
    pygame.time.wait(1 * 1000)

def load_whiteboard(button_choice, username):
    folder_path = os.path.join("user_data", username)  # Create a folder path based on the username
    file_name = os.path.join(folder_path, f"{username}_whiteboard.png")  # Use the folder path to create the file_name
    try:
        if os.path.exists(file_name):
            button_choice["whiteboard"] = pygame.image.load(file_name).convert()
        else:
            load_error_font = pygame.font.Font(None, 36)
            load_error_text = load_error_font.render("Whiteboard not found", True, RED)
            load_error_text_rect = load_error_text.get_rect(center=screen.get_rect().center)
            screen.blit(load_error_text, load_error_text_rect)
            pygame.display.flip()
            pygame.time.wait(1 * 1000)

    except pygame.error:
        print(f"Could not load whiteboard from {file_name}")

def choose_color():
    root = tk.Tk()
    root.withdraw()
    color = colorchooser.askcolor()[0]
    return tuple(int(c) for c in color)

def run(username):
    pygame.init()
    info = pygame.display.Info()
    #screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    whiteboard = pygame.Surface((info.current_w, info.current_h))
    whiteboard.fill(background_color)

    # Button properties
    button_choice = {
        "whiteboard": whiteboard,
        "whiteboard_rect": pygame.Rect(0, 0, info.current_w, info.current_h),
        "black_button_rect": pygame.Rect(10, 10, 100, 50),
        "blue_button_rect": pygame.Rect(120, 10, 100, 50),
        "rgb_picker_rect": pygame.Rect(230, 10, 100, 50),  # Added rgb_picker_rect
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
        "drag_slider": False,
        "black": False,
        "blue": False,
        "eraser": False,
        "clear": False,
        "slider": False,
        "rgb_picker": False,
        "back": False
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_action(event.pos, button_choice, username)  # Pass the username here
                if event.button == 1 and button_choice["slider"]:
                    button_choice["drag_slider"] = True
                elif event.button == 1 and button_choice["rgb_picker"]:
                    button_choice["color"] = choose_color()
            elif event.type == pygame.MOUSEMOTION:
                slider_motion(event.pos, button_choice)
            elif event.type == pygame.MOUSEBUTTONUP:
                button_choice["drawing"] = False
                button_choice["drag_slider"] = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                back_button_action(username)  # Trigger back button action on Backspace key press

        screen.blit(button_choice["whiteboard"], (0, 0))
        
        

        # Draw the buttons
        pygame.draw.rect(screen, BLACK, button_choice["black_button_rect"])
        pygame.draw.rect(screen, BLUE, button_choice["blue_button_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["rgb_picker_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["eraser_button_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["clear_button_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["save_button_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["load_button_rect"])
        pygame.draw.rect(screen, button_choice["color"], button_choice["color_choice_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["back_button_rect"])

        # Draw the button labels
        button_font = pygame.font.SysFont("Arial", 20)
        screen.blit(button_font.render("Black", True, WHITE), (button_choice["black_button_rect"].x + 10, button_choice["black_button_rect"].y + 10))
        screen.blit(button_font.render("Blue", True, WHITE), (button_choice["blue_button_rect"].x + 20, button_choice["blue_button_rect"].y + 10))
        screen.blit(button_font.render("Eraser", True, WHITE), (button_choice["eraser_button_rect"].x + 10, button_choice["eraser_button_rect"].y + 10))
        screen.blit(button_font.render("Clear", True, WHITE), (button_choice["clear_button_rect"].x + 20, button_choice["clear_button_rect"].y + 10))
        screen.blit(button_font.render("Save", True, WHITE), (button_choice["save_button_rect"].x + 25, button_choice["save_button_rect"].y + 10))
        screen.blit(button_font.render("Load", True, WHITE), (button_choice["load_button_rect"].x + 25, button_choice["load_button_rect"].y + 10))
        screen.blit(button_font.render("Back", True, WHITE), (button_choice["back_button_rect"].x + 25, button_choice["back_button_rect"].y + 10))
        screen.blit(button_font.render("RGB", True, WHITE), (button_choice["rgb_picker_rect"].x + 30, button_choice["rgb_picker_rect"].y + 5))
        screen.blit(button_font.render("Selector", True, WHITE), (button_choice["rgb_picker_rect"].x + 20, button_choice["rgb_picker_rect"].y + 25))

        # Draw the slider
        pygame.draw.rect(screen, GREY, button_choice["slider_width_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["slider_width_rect"], 2)
        slider_pos = (button_choice["slider_width_rect"].left + int((button_choice["slider_width"] - 1) / 19 * button_choice["slider_width_rect"].width), button_choice["slider_width_rect"].centery)
        pygame.draw.circle(screen, BLACK, slider_pos, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#Menu Section

def menu_button_action(label, username):
    if label == "Whiteboard":
        run(username)
        
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

def menu_buttons(username):
    pygame.init()
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
                            menu_button_action(label, username)
                        

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
            pygame.draw.rect(screen, WHITE, button_rect, 3)

            button_text = button_font.render(label, True, button_text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            screen.blit(button_text, text_rect)

        pygame.display.flip()
        clock.tick(30)

#Login Section

def login():
    pygame.init()

    # Set up the screen
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
    login_button = pygame.Rect(screen_width // 2 - 50, password_y + 80, 100, 30)
    signup_button = pygame.Rect(screen_width // 2 - 50, password_y + 120, 100, 30)
    button_color = BLACK
    login_button_text = "Log In"
    signup_button_text = "Sign up"

    # Invalid Login message variables
    invalid_login_text = ""
    invalid_login_font = pygame.font.Font(None, 24)
    invalid_login_rect = pygame.Rect(screen_width // 2 - 100, password_y + 170, 200, 30)

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
                elif login_button.collidepoint(mouse_pos):
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        login_validity = False 
                        for line in reader:
                            if username == "" or password == "":
                                invalid_login_text = "Invalid Login"
                            elif username == line[0] and password == line[1]:
                                print("Credentials Matched")
                                login_validity = True
                                invalid_login_text = ""
                                user_folder = os.path.join("user_data", username)
                                if not os.path.exists(user_folder):
                                    os.makedirs(user_folder)
                                menu_buttons(username)
                            if not login_validity:
                                invalid_login_text = "Invalid Login"
                elif signup_button.collidepoint(mouse_pos):
                    signup()

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

        # Draw Log in button
        pygame.draw.rect(screen, button_color, login_button)
        button_font = pygame.font.Font(None, 24)
        button_text_rendered = button_font.render(login_button_text, True, WHITE)
        button_text_rect = button_text_rendered.get_rect(center=login_button.center)
        screen.blit(button_text_rendered, button_text_rect)
        
        # Draw sign up button
        pygame.draw.rect(screen, button_color, signup_button)
        button_font = pygame.font.Font(None, 24)
        button_text_rendered = button_font.render(signup_button_text, True, WHITE)
        button_text_rect = button_text_rendered.get_rect(center=signup_button.center)
        screen.blit(button_text_rendered, button_text_rect)

        # Draw invalid login message
        invalid_login_rendered = invalid_login_font.render(invalid_login_text, True, RED)
        screen.blit(invalid_login_rendered, invalid_login_rect)
        
        pygame.display.flip()
        clock.tick(60)

def signup():
    pygame.init()

    # Set up the screen
    screen_width, screen_height = pygame.display.get_surface().get_size()

    clock = pygame.time.Clock()
    running = True

    # Text input variables
    signup_username = ""
    signup_password = ""
    signup_active_field = "signup_username"  # To keep track of the active text input field
    signup_username_outline_color = BLACK  # Outline color for username input box
    signup_password_outline_color = BLACK

    # Calculate vertical positions for username and password
    signup_username_y = screen_height // 2 - 50
    signup_password_y = signup_username_y + 100

    # Button variables
    signup_button = pygame.Rect(screen_width // 2 - 50, signup_password_y + 80, 100, 30)
    signup_back_button = pygame.Rect(screen_width // 2 - 50, signup_password_y + 80, 100, 30)
    signup_button_color = BLACK
    signup_button_text = "Sign Up"

    # Invalid Login message variables
    invalid_signup_text = ""
    invalid_signup_font = pygame.font.Font(None, 24)
    invalid_signup_rect = pygame.Rect(screen_width // 2 - 100, signup_password_y + 120, 200, 30)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if signup_active_field == "signup_username":
                        signup_username = signup_username[:-1]
                    elif signup_active_field == "signup_password":
                        signup_password = signup_password[:-1]
                else:
                    if signup_active_field == "signup_username":
                        signup_username += event.unicode
                    elif signup_active_field == "signup_password":
                        signup_password += event.unicode
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if signup_username_rect.collidepoint(mouse_pos):
                    signup_active_field = "signup_username"
                    signup_username_outline_color = GREY
                    signup_password_outline_color = BLACK
                elif signup_password_rect.collidepoint(mouse_pos):
                    signup_active_field = "signup_password"
                    signup_username_outline_color = BLACK
                    signup_password_outline_color = GREY
                elif signup_button.collidepoint(mouse_pos):
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file)
                        for row in reader:
                            if signup_username == "" or signup_password == "":
                                invalid_signup_text = "Invalid username or password"
                                break  # Exit the loop if username is invalid
                            elif signup_username in row:
                                invalid_signup_text = "Username already taken"
                                break  # Exit the loop if username is taken
                        else:
                            # Append the new username and password on a new row
                            with open(file_name, "a", newline="") as csv_file:
                                writer = csv.writer(csv_file)
                                csv_file.write('\n')
                                writer.writerow([signup_username, signup_password])
                            login()
            # Clear the screen
        screen.fill(WHITE)

        # Draw title
        font = pygame.font.Font(None, 48)
        signup_title_text = font.render("Sign up for KanBoard.5", True, BLACK)
        signup_title_text_rect = signup_title_text.get_rect(center=(screen_width // 2, 350))
        screen.blit(signup_title_text, signup_title_text_rect)

        # Draw username label and input box
        signup_font = pygame.font.Font(None, 36)
        signup_username_label = signup_font.render("New Username:", True, BLACK)
        signup_username_label_rect = signup_username_label.get_rect(center=(screen_width // 2, signup_username_y))
        screen.blit(signup_username_label, signup_username_label_rect)

        signup_username_rect = pygame.Rect(screen_width // 2 - 100, signup_username_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, signup_username_rect)
        pygame.draw.rect(screen, signup_username_outline_color, signup_username_rect, 2)  # Use username_outline_color for the outline

        signup_username_text = signup_font.render(signup_username, True, BLACK)
        signup_username_text_rect = signup_username_text.get_rect(center=signup_username_rect.center)
        screen.blit(signup_username_text, signup_username_text_rect)

        # Draw password label and input box
        signup_password_label = signup_font.render("New Password:", True, BLACK)
        signup_password_label_rect = signup_password_label.get_rect(center=(screen_width // 2, signup_password_y))
        screen.blit(signup_password_label, signup_password_label_rect)

        signup_password_rect = pygame.Rect(screen_width // 2 - 100, signup_password_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, signup_password_rect)
        pygame.draw.rect(screen, signup_password_outline_color, signup_password_rect, 2)

        signup_password_text = signup_font.render("*" * len(signup_password), True, BLACK)
        signup_password_text_rect = signup_password_text.get_rect(center=signup_password_rect.center)
        screen.blit(signup_password_text, signup_password_text_rect)

        # Draw sign up button
        pygame.draw.rect(screen, signup_button_color, signup_button)
        signup_button_font = pygame.font.Font(None, 24)
        signup_button_text_rendered = signup_button_font.render(signup_button_text, True, WHITE)
        signup_button_text_rect = signup_button_text_rendered.get_rect(center=signup_button.center)
        screen.blit(signup_button_text_rendered, signup_button_text_rect)

        # Draw invalid login message
        invalid_signup_rendered = invalid_signup_font.render(invalid_signup_text, True, RED)
        screen.blit(invalid_signup_rendered, invalid_signup_rect)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    login()
    
    
    
    
