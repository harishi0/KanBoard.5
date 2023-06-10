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

max_length_login_signup = 12

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
        drawing_distance_x = pos[0] - last_pos[0]
        drawing_distance_y = pos[1] - last_pos[1]
        drawing_distance = max(abs(drawing_distance_x), abs(drawing_distance_y))
        step_x = drawing_distance_x / drawing_distance if drawing_distance != 0 else 0
        step_y = drawing_distance_y / drawing_distance if drawing_distance != 0 else 0

        for i in range(drawing_distance):
            x = int(last_pos[0] + i * step_x)
            y = int(last_pos[1] + i * step_y)
            
            # Check if the point is within the whiteboard boundary
            if button_choice["whiteboard_rect"].collidepoint(x, y):
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
                        button_choice["slider_width_rect"])
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
    screen.blit(confirm_save_text, confirm_save_text_rect, screen.fill(WHITE))
    pygame.display.flip()
    pygame.time.wait(1 * 1000)

def load_whiteboard(button_choice, username):
    folder_path = os.path.join("user_data", username)  # Create a folder path based on the username
    file_name = os.path.join(folder_path, f"{username}_whiteboard.png")  # Use the folder path to create the file_name
    try:
        if os.path.exists(file_name):
            button_choice["whiteboard"] = pygame.image.load(file_name).convert()
            confirm_load_font = pygame.font.Font(None, 36)
            confirm_load_text = confirm_load_font.render("Whiteboard loaded", True, GREEN)
            confirm_load_text_rect = confirm_load_text.get_rect(center=screen.get_rect().center)
            screen.blit(confirm_load_text, confirm_load_text_rect, screen.fill(WHITE))
            pygame.display.flip()
            pygame.time.wait(1 * 1000)
        else:
            load_error_font = pygame.font.Font(None, 36)
            load_error_text = load_error_font.render("Whiteboard not found", True, RED)
            load_error_text_rect = load_error_text.get_rect(center=screen.get_rect().center)
            screen.blit(load_error_text, load_error_text_rect, screen.fill(WHITE))
            pygame.display.flip()
            pygame.time.wait(1 * 1000)

    except pygame.error:
        print(f"Could not load whiteboard from {file_name}")

def choose_color():
    root = tk.Tk()
    root.withdraw()
    color = colorchooser.askcolor()
    if color[0] is not None:
        return tuple(int(c) for c in color[0])
    else:
        # Handle the case where no color was selected
        # You can choose to return a default color or handle it differently
        return BLACK  # Returning black color as an example

def run_whiteboard(username):
    pygame.init()
    info = pygame.display.Info()
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
        "whiteboard_menu_border": pygame.Rect(0, 65, 1450, 2),
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
        pygame.draw.rect(screen, BLACK, button_choice["whiteboard_menu_border"])

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
        run_whiteboard(username)
        
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
    login_username = ""
    login_password = ""
    active_field = "login_username"  # To keep track of the active text input field
    login_username_outline_color = GREY  # Outline color for username input box
    login_password_outline_color = GREY

    # Calculate vertical positions for username and password
    login_username_y = screen_height // 2 - 50
    login_password_y = login_username_y + 100

    # Button variables
    login_button = pygame.Rect(screen_width // 2 - 50, login_password_y + 80, 100, 30)
    signup_button = pygame.Rect(screen_width // 2 - 50, login_password_y + 120, 100, 30)
    exit_login_button = pygame.Rect(screen_width // 2 - 50, login_password_y + 160, 100, 30)
    login_buttons_color = BLACK
    login_button_text = "Log In"
    signup_button_text = "Sign up"
    exit_login_text = "Exit"

    # Invalid Login message variables
    invalid_login_text = ""
    invalid_login_font = pygame.font.Font(None, 24)
    invalid_login_rect = pygame.Rect(screen_width // 2 - 100, login_password_y + 200, 200, 30)

    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    if active_field == "login_username":
                        login_username = login_username[:-1]
                    elif active_field == "login_password":
                        login_password = login_password[:-1]
                elif event.key == K_TAB:
                    pass
                elif event.key == K_RETURN:
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        login_validity = False 
                        for line in reader:
                            if login_username == "" or login_password == "":
                                invalid_login_text = "Invalid Login"
                            elif login_username == line[0] and login_password == line[1]:
                                login_validity = True
                                invalid_login_text = ""
                                user_folder = os.path.join("user_data", login_username)
                                if not os.path.exists(user_folder):
                                    os.makedirs(user_folder)
                                menu_buttons(login_username)
                            if not login_validity:
                                invalid_login_text = "Invalid Login"
                else:
                    if active_field == "login_username":
                        if len(login_username) < max_length_login_signup:
                            login_username += event.unicode[:max_length_login_signup - len(login_username)]
                    elif active_field == "login_password":
                        if len(login_password) < max_length_login_signup:
                            login_password += event.unicode[:max_length_login_signup - len(login_password)]
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if login_username_rect.collidepoint(mouse_pos):
                    active_field = "login_username"
                    login_username_outline_color = BLACK
                    login_password_outline_color = GREY
                elif login_password_rect.collidepoint(mouse_pos):
                    active_field = "login_password"
                    login_username_outline_color = GREY
                    login_password_outline_color = BLACK
                elif login_button.collidepoint(mouse_pos):
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        login_validity = False 
                        for line in reader:
                            if login_username == "" or login_password == "":
                                invalid_login_text = "Invalid Login"
                            elif login_username == line[0] and login_password == line[1]:
                                print("Credentials Matched")
                                login_validity = True
                                invalid_login_text = ""
                                user_folder = os.path.join("user_data", login_username)
                                if not os.path.exists(user_folder):
                                    os.makedirs(user_folder)
                                menu_buttons(login_username)
                            if not login_validity:
                                invalid_login_text = "Invalid Login"
                elif signup_button.collidepoint(mouse_pos):
                    signup()
                elif exit_login_button.collidepoint(mouse_pos):
                    exit()

        # Clear the screen
        screen.fill(WHITE)

        # Draw title
        login_title_font = pygame.font.Font(None, 48)
        login_title_text = login_title_font.render("Log into KanBoard.5", True, BLACK)
        login_title_text_rect = login_title_text.get_rect(center=(screen_width // 2, 350))
        screen.blit(login_title_text, login_title_text_rect)

        # Draw username label and input box
        login_label_font = pygame.font.Font(None, 36)
        login_username_label = login_label_font.render("Username:", True, BLACK)
        login_username_label_rect = login_username_label.get_rect(center=(screen_width // 2, login_username_y))
        screen.blit(login_username_label, login_username_label_rect)

        login_username_rect = pygame.Rect(screen_width // 2 - 100, login_username_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, login_username_rect)
        pygame.draw.rect(screen, login_username_outline_color, login_username_rect, 2)  # Use username_outline_color for the outline

        login_username_text = login_label_font.render(login_username, True, BLACK)
        login_username_text_rect = login_username_text.get_rect(center=login_username_rect.center)
        screen.blit(login_username_text, login_username_text_rect)

        # Draw password label and input box
        login_password_label = login_label_font.render("Password:", True, BLACK)
        login_password_label_rect = login_password_label.get_rect(center=(screen_width // 2, login_password_y))
        screen.blit(login_password_label, login_password_label_rect)

        login_password_rect = pygame.Rect(screen_width // 2 - 100, login_password_y + 30, 200, 30)
        pygame.draw.rect(screen, WHITE, login_password_rect)
        pygame.draw.rect(screen, login_password_outline_color, login_password_rect, 2)

        login_password_text = login_label_font.render("*" * len(login_password), True, BLACK)
        login_password_text_rect = login_password_text.get_rect(center=login_password_rect.center)
        screen.blit(login_password_text, login_password_text_rect)

        # Draw Log in button
        pygame.draw.rect(screen, login_buttons_color, login_button)
        login_button_font = pygame.font.Font(None, 24)
        login_button_text_rendered = login_button_font.render(login_button_text, True, WHITE)
        login_button_text_rect = login_button_text_rendered.get_rect(center=login_button.center)
        screen.blit(login_button_text_rendered, login_button_text_rect)
        
        # Draw sign up button
        pygame.draw.rect(screen, login_buttons_color, signup_button)
        signup_button_font = pygame.font.Font(None, 24)
        signup_button_text_rendered = signup_button_font.render(signup_button_text, True, WHITE)
        signup_button_text_rect = signup_button_text_rendered.get_rect(center=signup_button.center)
        screen.blit(signup_button_text_rendered, signup_button_text_rect)
        
        # Draw Exit up button
        pygame.draw.rect(screen, login_buttons_color, exit_login_button)
        exit_login_button_font = pygame.font.Font(None, 24)
        exit_login_button_text_rendered = exit_login_button_font.render(exit_login_text, True, WHITE)
        exit_login_button_text_rect = exit_login_button_text_rendered.get_rect(center=exit_login_button.center)
        screen.blit(exit_login_button_text_rendered, exit_login_button_text_rect)
        
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
    signup_username_outline_color = GREY  # Outline color for username input box
    signup_password_outline_color = GREY

    # Calculate vertical positions for username and password
    signup_username_y = screen_height // 2 - 50
    signup_password_y = signup_username_y + 100

    # Button variables
    signup_button = pygame.Rect(screen_width // 2 - 50, signup_password_y + 80, 100, 30)
    back_signup_button = pygame.Rect(screen_width // 2 - 50, signup_password_y + 120, 100, 30)
    signup_button_color = BLACK
    back_signup_button_color = BLACK
    signup_button_text = "Sign Up"
    back_signup_button_text = "Back"

    # Invalid Login message variables
    invalid_signup_text = ""
    invalid_signup_font = pygame.font.Font(None, 24)
    invalid_signup_rect = pygame.Rect(screen_width // 2 - 100, signup_password_y + 160, 200, 30)
    
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
                elif event.key == K_TAB:
                    pass
                elif event.key == K_RETURN:
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file, delimiter=',')
                        login_validity = False 
                        for line in reader:
                            if signup_username == "" or signup_password == "":
                                invalid_signup_text = "Invalid username or password"
                            elif signup_username == line[0] and signup_password == line[1]:
                                print("Account Created")
                                login_validity = True
                                invalid_signup_text = ""
                                user_folder = os.path.join("user_data")
                                if not os.path.exists(user_folder):
                                    os.makedirs(user_folder)
                                menu_buttons(signup_username)
                            if not login_validity:
                                invalid_signup_text = "Invalid username or password"
                else:
                    if signup_active_field == "signup_username":
                        if len(signup_username) < max_length_login_signup:
                                signup_username += event.unicode[:max_length_login_signup- len(signup_username)]
                    elif signup_active_field == "signup_password":
                        if len(signup_password) < max_length_login_signup:
                            signup_password += event.unicode[:max_length_login_signup - len(signup_password)]
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if signup_username_rect.collidepoint(mouse_pos):
                    signup_active_field = "signup_username"
                    signup_username_outline_color = BLACK
                    signup_password_outline_color = GREY
                elif signup_password_rect.collidepoint(mouse_pos):
                    signup_active_field = "signup_password"
                    signup_username_outline_color = GREY
                    signup_password_outline_color = BLACK
                elif signup_button.collidepoint(mouse_pos):
                    folder = os.getcwd()
                    file_name = folder + "\\accounts.csv"
                    with open(file_name, "r") as csv_file:
                        reader = csv.reader(csv_file)
                        for row in reader:
                            if signup_username == "" or signup_password == "":
                                invalid_signup_text = "Invalid username or password"
                                break
                            elif signup_username in row:
                                invalid_signup_text = "Username already taken"
                                break
                            else:
                                # Append the new username and password on a new row
                                with open(file_name, "a", newline="") as csv_file:
                                    csv_file.write("\n" + signup_username + "," + signup_password)
                                confirm_signup_font = pygame.font.Font(None, 36)
                                confirm_signup_text = confirm_signup_font.render("Account created", True, GREEN)
                                confirm_signup_text_rect = confirm_signup_text.get_rect(center=screen.get_rect().center)
                                screen.blit(confirm_signup_text, confirm_signup_text_rect, screen.fill(WHITE))
                                pygame.display.flip()
                                pygame.time.wait(1 * 1000)
                                login()
                elif back_signup_button.collidepoint(mouse_pos):
                    login()
                    
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
        
        #Draw back button 
        pygame.draw.rect(screen, back_signup_button_color, back_signup_button)
        back_signup_button_font = pygame.font.Font(None, 24)
        back_signup_button_text_rendered = back_signup_button_font.render(back_signup_button_text, True, WHITE)
        back_signup_button_text_rect = back_signup_button_text_rendered.get_rect(center=back_signup_button.center)
        screen.blit(back_signup_button_text_rendered, back_signup_button_text_rect)
        

        # Draw invalid login message
        invalid_signup_rendered = invalid_signup_font.render(invalid_signup_text, True, RED)
        screen.blit(invalid_signup_rendered, invalid_signup_rect)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    login()
