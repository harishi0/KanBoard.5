#Whiteboard done by Ishaan Patel
#Kanban Board done by Harish Buvanendran 
#Calendar done by Zhiqian Zou
#Timer done by Isa Jamal


#Imports

import pygame
from pygame.locals import *
import os
import csv
import sys
import tkinter as tk
from tkinter import colorchooser
from button import Button
import subprocess
import calendar
import random
import json


#Initialize pygame

pygame.init()

#Set caption of the pygame application

pygame.display.set_caption('KanBoard.5')

#Set color values as tuple

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 191, 255)
GREY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
background_color = WHITE

#Set the screen variable to full screen to be used throughout the code

screen = pygame.display.set_mode((0, 0), FULLSCREEN)


#Whiteboard Section

def mouse_button_action(pos, button_choice, username):
    '''
        Functionality for what every button press does in the whiteboard.
        Parameter: pos gets the cursor position on the whiteboard
        Parameter: button_choice is a dictionary called which has the current states of the buttons that are controlled by the position of the mouse
        Parameter: username is to determine which user is using the whiteboard
        Return: N/A
    '''
    
    #Updates the button functionality based on cursor position
    button_choice["black"] = button_choice["black_button_rect"].collidepoint(pos)
    button_choice["blue"] = button_choice["blue_button_rect"].collidepoint(pos)
    button_choice["eraser"] = button_choice["eraser_button_rect"].collidepoint(pos)
    button_choice["clear"] = button_choice["clear_button_rect"].collidepoint(pos)
    button_choice["slider"] = button_choice["slider_width_rect"].collidepoint(pos)
    button_choice["rgb_picker"] = button_choice["rgb_picker_rect"].collidepoint(pos)
    button_choice["save"] = button_choice["save_button_rect"].collidepoint(pos)
    button_choice["load"] = button_choice["load_button_rect"].collidepoint(pos)
    button_choice["back"] = button_choice["back_button_rect"].collidepoint(pos)
    
    #Calls function to set up drawing on whiteboard
    drawing(pos, button_choice)
    
    #If statements determining whiteboard functionality based on what button is selected
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
        whiteboard_back_button_action(username)
    elif button_choice["rgb_picker"]:
        button_choice["color"] = choose_color()

def whiteboard_back_button_action(username):
    '''
    Functionality for back button on whiteboard screen to return to the menu page.
    Parameter: username is to determine which user is using the whiteboard
    Return: N/A
    '''
    
    #Call menu button screen
    menu_buttons(username)

def drawing(pos, button_choice):
    '''
    Set up the drawing portion of the whiteboard before the actual drawing commences by getting the starting position of the cursor.
    Parameter: pos gets the starting cursor position of the whiteboard
    Parameter: button_choice determines which button is selected 
    Return: N/A
    '''
    
    button_choice["drawing"] = True
    button_choice["last_pos"] = pos

def slider_motion(pos, button_choice):
    '''
    Set slider motion so that when it gets dragged, the function to change the width of the drawing gets called and when using slider, drawing cannot happen.
    Parameter: pos gets cursor position of the whiteboard
    Parameter: button_choice gets which button is selected 
    Return: N/A
    '''
    
    #If statements for whether the slider is dragging or not
    if button_choice["drag_slider"]:
        update_slider_width(pos, button_choice)
    if button_choice["drawing"] and not button_choice["drag_slider"]:  
        draw(pos, button_choice)

def draw(pos, button_choice):
    '''
    Uses mouse cursor positions to and drawing distance to calculate drawing x and y points and using circles to iterate the drawing for smoother lines. Function first checks whether drawing is selected 
    and if so, it proceeds to calculate drawing. Then the for loop iterates it as many times as the drawing distance.
    Parameter: pos gets cursor position to calculate x and y coordinates to draw on whiteboard
    Parameter: button_choice to select color or tool when drawing
    Return: N/A
    '''
    
    #Calculate drawing x and y coordinates
    if button_choice["drawing"]:
        color = button_choice["color"]
        last_pos = button_choice["last_pos"]
        drawing_distance_x = pos[0] - last_pos[0]
        drawing_distance_y = pos[1] - last_pos[1]
        drawing_distance = max(abs(drawing_distance_x), abs(drawing_distance_y))
        step_x = drawing_distance_x / drawing_distance if drawing_distance != 0 else 0
        step_y = drawing_distance_y / drawing_distance if drawing_distance != 0 else 0

        #Iterate the drawing through a for loop
        for i in range(drawing_distance):
            x = int(last_pos[0] + i * step_x)
            y = int(last_pos[1] + i * step_y)
            pygame.draw.circle(button_choice["whiteboard"], color, (x, y), button_choice["slider_width"] // 2)

        button_choice["last_pos"] = pos

def clear_whiteboard(whiteboard):
    '''
    Clear functionality which resets whiteboard background to what ever the background color is.
    Parameter: whiteboard is the screen display which is set to full screen
    Return: N/A
    '''
    whiteboard.fill(background_color)

def update_slider_width(pos, button_choice):
    '''
    Updates slider width so that thickness of drawing changes based on users slider selection. Maximum slider with is 20 while minimum is 5.
    Parameter: pos gets cursor position of the white board to see if the slider is being dragged
    Parameter: button_choice gets button functionality when buttons are selected
    Return: N/A
    '''
    
    #Checks if slider is being dragged
    if button_choice["drag_slider"]:
        #Checks if the cursor is in the confines of the slider
        if button_choice["slider_width_rect"].left <= pos[0] <= button_choice["slider_width_rect"].right:
            # Calculate the new slider width based on the mouse position
            slider_width = int((pos[0] - button_choice["slider_width_rect"].left) / button_choice["slider_width_rect"].width * 19) + 1
            #Limit the slider width to a minimum value of 5
            slider_width = max(slider_width, 5)
            #Limit the slider width to a maximum value of 20 
            slider_width = min(slider_width, 20)
            #Update the slider width and position after drag
            button_choice["slider_width"] = slider_width
            slider_pos = (button_choice["slider_width_rect"].left + int((button_choice["slider_width"] - 1) / 19 * button_choice["slider_width_rect"].width),button_choice["slider_width_rect"])
            button_choice["slider_pos"] = slider_pos

def save_whiteboard(whiteboard, username):
    '''
    Saves the white board as a png while to the folder user_data where the png gets saved to a file name of the username with the png named after the username.
    The folder user_data has to be checked if it's in use and based on that it may or may not created the folder. A text is set with a timer so that it only displays
    for a short period of time. 
    Parameter: whiteboard is the display of the white board application
    Parameter: username is the username that the user used to login which is used to create a file and folder personalized to them
    Return: N/A
    '''
    
    #Create the user_data folder with username folder if it doesn't exist
    folder_path = os.path.join("user_data", username)  
    os.makedirs(folder_path, exist_ok=True) 
    #Use the folder path to create the file_name with the username
    file_name = os.path.join(folder_path, f"{username}_whiteboard.png") 
    #Pygame save images to the folder
    pygame.image.save(whiteboard, file_name)
    #Confirm save white board displays for a limited amount of time
    confirm_save_font = pygame.font.Font(None, 36)
    confirm_save_text = confirm_save_font.render("Whiteboard saved", True, GREEN)
    confirm_save_text_rect = confirm_save_text.get_rect(center=screen.get_rect().center)
    screen.blit(confirm_save_text, confirm_save_text_rect, screen.fill(WHITE))
    pygame.display.flip()
    pygame.time.wait(1 * 1000)

def load_whiteboard(button_choice, username):
    '''
    Loads the white board as a png from the username specific folder located in the user_data folder. Try and except used so that if a 
    white board has not already been saved, an error message occurs that displays for few seconds.
    Parameter: button_choice for when the load button is selected
    Parameter: username to load white board png from the user name specific file 
    Return: N/A
    '''
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
    '''
    Used tkinter to open a pop up rgb selector window. This window allows the user to select a color and return it as a tuple.
    If no color was selected from the rgb picker, the color is automatically set to black. 
    Parameter: N/A
    Return: Return tuple(int(c) for c in color[0]) to that the tuple can be used as a color for drawing
    Return: Return BLACK if nothing is selected
    '''
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
    '''
    Run function for the white board runs the entire GUI of the whiteboard. All the buttons, labels and texts are defined in this function.
    Also a dictionary is used to store all the properties of the buttons and draw them. A while loop is set to iterate the GUI and deal
    with any key down or mouse button down inputs.
    Parameter: username to run the white board with the username file 
    Return: N/A
    '''
    
    #Set display of white board
    info = pygame.display.Info()
    clock = pygame.time.Clock()
    whiteboard = pygame.Surface((info.current_w, info.current_h))
    whiteboard.fill(background_color)

    # Button properties in dictionary
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

    #White board loop to run GUI
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #For all mouse button down button inputs
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_button_action(event.pos, button_choice, username)  # Pass the username here
                if event.button == 1 and button_choice["slider"]:
                    button_choice["drag_slider"] = True
                elif event.button == 1 and button_choice["rgb_picker"]:
                    button_choice["color"] = choose_color()
            #For all mouse motion inputs
            elif event.type == pygame.MOUSEMOTION:
                slider_motion(event.pos, button_choice)
            #For all mouse button up inputs
            elif event.type == pygame.MOUSEBUTTONUP:
                button_choice["drawing"] = False
                button_choice["drag_slider"] = False
            #For all button key inputs
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                whiteboard_back_button_action(username)  # Trigger back button action on Backspace key press

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

        # Draw the RGB picker text
        rgb_ok_text = "*Press OK twice"
        rgb_ok_text_rect = button_font.render(rgb_ok_text, True, BLACK).get_rect()
        rgb_ok_text_rect.midtop = (button_choice["rgb_picker_rect"].centerx, button_choice["rgb_picker_rect"].bottom + 5)
        screen.blit(button_font.render(rgb_ok_text, True, BLACK), rgb_ok_text_rect)
        
        # Draw the slider
        pygame.draw.rect(screen, GREY, button_choice["slider_width_rect"])
        pygame.draw.rect(screen, BLACK, button_choice["slider_width_rect"], 2)
        slider_pos = (button_choice["slider_width_rect"].left + int((button_choice["slider_width"] - 1) / 19 * button_choice["slider_width_rect"].width), button_choice["slider_width_rect"].centery)
        pygame.draw.circle(screen, BLACK, slider_pos, 10)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#Kanban Section

def run_kanban_main(username):
    """
    Runs the main Kanban application.

    """
    # Initialize Pygame
    screen_info = pygame.display.Info()
    WIDTH = screen_info.current_w
    HEIGHT = screen_info.current_h

    # Set the font properties
    FONT_SIZE = 24
    FONT_NAME = pygame.font.get_default_font()
    font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    notes = []  # List to store notes

    def draw_note(note):
        '''
        Draws a note on the screen

           perameters(note[]) The note dictionary containing its properties.
        '''
        
        if note['selected']:
            pygame.draw.rect(screen, YELLOW, (note['x'] - 5, note['y'] - 5, note['width'] + 10, note['height'] + 10))
        pygame.draw.rect(screen, note['color'], (note['x'], note['y'], note['width'], note['height']))

        lines = note['text'].split('\n')
        text_lines = []

# prevent typing to go outside the borders of the sticky note
        for line in lines:
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + word + ' '
                if font.size(test_line)[0] <= note['width'] - 20:
                    current_line = test_line
                else:
                    if current_line:
                        text_lines.append(current_line)
                    current_line = word + ' '
            if current_line:
                text_lines.append(current_line)

        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, BLACK)
            text_x = note['x'] + 10
            text_y = note['y'] + 10 + (i * FONT_SIZE)

            if text_y + FONT_SIZE <= note['y'] + note['height'] - 10:
                screen.blit(text_surface, (text_x, text_y))
            else:
                break


    def events_note(note, event):
        """
        Handles events for the notes.

        Args:
            note (dict): The note dictionary.
            event (pygame.event.Event): The event object.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 1:
                if note['selected']:
                    note['selected'] = False
                elif pygame.Rect(note['x'], note['y'], note['width'], note['height']).collidepoint(mouse_pos):
                    note['selected'] = True
                    note['offset'] = (mouse_pos[0] - note['x'], mouse_pos[1] - note['y'])
            elif event.button == 3:
                if pygame.Rect(note['x'], note['y'], note['width'], note['height']).collidepoint(mouse_pos):
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


    def save_notes(username):
        """
        Saves the notes to a JSON file for the given username.
        username (str): The username associated with the notes.

        """
        data = []
        for note in notes:
            data.append({
                'x': note['x'],
                'y': note['y'],
                'text': note['text']
            })

        # Create the "user_data" folder if it doesn't exist
        folder_path = "user_data"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Save the notes to a JSON file
        file_path = os.path.join(folder_path, f"{username}_kanban.json")
        with open(file_path, 'w') as file:
            json.dump(data, file)


    def load_notes(username):
        """
            Loads the notes from a JSON file for the given username.

            perameter username (str): The username of the acount the user is signed into.
            used to name the specific file so that it can be used to load the data for each seperate user

            """
        file_path = os.path.join('user_data', f'{username}_kanban.json')
        try:
            with open(file_path, 'r') as file:
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
        """
        Creates a new note.
        """

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


    def draw_kanban_button(x, y, width, height, color, text, text_color):
        '''
        Draws a button on the screen.

    perameters:
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        color (tuple): The color of the button (RGB format).
        text (str): The text displayed on the button.
        text_color (tuple): The color of the text (RGB format).
        '''
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = font.render(text, True, text_color)
        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))


    def draw_kanban_board():
        """
        Draws the Kanban board categories on the screen. 
        by gettting the number of columns/categories and dividing it by the width of the screen
        to get the column width and placing the titles the top center of each categorie.
        """
        num_columns = 4  # Number of Kanban board columns
        column_width = WIDTH // num_columns

        # Define the titles for each category
        titles = ["To Do", "In Progress","Testing", "Done"]

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
    button_color = GREY
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
    save_button_color = GREY
    save_button_text = "Save"
    save_button_text_color = BLACK

    # Create the "Clear" button
    clear_button_width = 150
    clear_button_height = 50
    clear_button_y = button_y
    clear_button_color = GREY
    clear_button_text = "Clear"
    clear_button_text_color = BLACK

    # Calculate the position of the "Load" button
    load_button_x = clear_button_x + clear_button_width + button_spacing

    # Create the "Load" button
    load_button_width = 150
    load_button_height = 50
    load_button_y = button_y
    load_button_color = GREY
    load_button_text = "Load"
    load_button_text_color = BLACK

    # Draw back button
    BACK_BUTTON_WIDTH = 100
    BACK_BUTTON_HEIGHT = 40
    back_button_x = (WIDTH - BACK_BUTTON_WIDTH) // 2
    back_button_y = HEIGHT - BACK_BUTTON_HEIGHT - 10
    back_button_rect = pygame.Rect(back_button_x, back_button_y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
    back_button_color = BLACK
    pygame.draw.rect(screen, back_button_color, back_button_rect)
    back_button_font = pygame.font.Font(None, 24)
    back_button_text_rendered = back_button_font.render("Back", True, WHITE)
    back_button_text_rect = back_button_text_rendered.get_rect(center=back_button_rect.center)
    screen.blit(back_button_text_rendered, back_button_text_rect)
        
    def runkanban(username):
        # Main game loop
        """
        Runs the Kanban board application.
        """
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
                    events_note(note, event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_pos):
                            create_note()
                        elif pygame.Rect(save_button_x, save_button_y, save_button_width, save_button_height).collidepoint(
                                mouse_pos):
                            save_notes(username)
                        elif pygame.Rect(load_button_x, load_button_y, load_button_width, load_button_height).collidepoint(
                                mouse_pos):
                            load_notes(username)
                        elif pygame.Rect(clear_button_x, clear_button_y, clear_button_width, clear_button_height).collidepoint(
                                mouse_pos):
                            notes.clear()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            # Check if the click is inside the calendar grid
                            if back_button_rect.collidepoint(event.pos):
                                menu_buttons(username) 

                elif event.type == pygame.MOUSEMOTION:
                    for note in notes:
                        if note['selected']:
                            mouse_pos = pygame.mouse.get_pos()
                            note['x'] = mouse_pos[0] - note['offset'][0]
                            note['y'] = mouse_pos[1] - note['offset'][1]

            screen.fill(WHITE)
            draw_kanban_board()
            draw_kanban_button(button_x, button_y, button_width, button_height, button_color, button_text, button_text_color)
            draw_kanban_button(save_button_x, save_button_y, save_button_width, save_button_height, save_button_color,save_button_text, save_button_text_color)
            draw_kanban_button(load_button_x, load_button_y, load_button_width, load_button_height, load_button_color,load_button_text, load_button_text_color)
            draw_kanban_button(clear_button_x, clear_button_y, clear_button_width, clear_button_height, clear_button_color,clear_button_text, clear_button_text_color)
            for note in notes:
                draw_note(note)
            
            # Draw the back button
            pygame.draw.rect(screen, back_button_color, back_button_rect)
            screen.blit(back_button_text_rendered, back_button_text_rect)

            # Define the text properties
            how_delete_note_font = pygame.font.Font(None, 20)
            how_delete_note_text = how_delete_note_font.render("Press Control + Backspace to delete a note", True, BLACK)
            how_delete_note_rect = how_delete_note_text.get_rect(top=10, left=10)

            # Blit the text onto the screen
            screen.blit(how_delete_note_text, how_delete_note_rect)

            pygame.display.flip()
            clock.tick(60)
    load_notes(username)
    runkanban(username)

    
# Calendar Section

# Function to save the calendar edition
def save_calendar(username, notes):
    '''
    Save the calendar edition to a file.
    perameter username (str): The username of the calendar owner.
    perameter notes (dict): A dictionary containing the notes for each day.

    Returns:
        None
    '''
    try:
        folder_path = os.path.join("user_data", username)  # Create a folder path based on the username
        os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist
        file_name = os.path.join(folder_path, f"{username}_calendar_notes.txt")  # Use the folder path to create the file_name
        with open(file_name, "a") as file:
            for date, note in notes.items():
                file.write(f"{date[0]},{date[1]},{date[2]}:{note}\n")
        print("Calendar edition saved successfully.")
    except IOError:
        print("Error occurred while saving the calendar edition.")

def load_calendar(username):
    '''
    Load the calendar dates/edits from a file.
    perameter username (str): The username of the calendar owner./ acounnt that the user is logged on to
    
    Returns:
        a dictionary containg the notes for each day using 
        notes = {}
    
    '''
    notes = {}  # Initialize the dictionary
    try:
        folder_path = os.path.join("user_data", username)  # Create a folder path based on the username
        file_name = os.path.join(folder_path, f"{username}_calendar_notes.txt")  # Use the folder path to create the file_name
        
        with open(file_name, "r") as file:
            for line in file:
                parts = line.strip().split(":")
                date_parts = parts[0].split(",")
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
                note = ":".join(parts[1:])
                notes[(year, month, day)] = note
                
        print("Calendar edition loaded successfully.")
    except FileNotFoundError:
        print("Calendar edition file not found.")
    except IOError:
        print("Error occurred while loading the calendar edition.")
    
    return notes  # Return the notes dictionary

def run_calendar(username):
    """
    Runs the calendar application.
    
    parameters username (str): The username of the account that the user is currently logged onto.
    """
    WIDTH, HEIGHT = screen.get_size()

    # Set font
    FONT_SIZE = 24
    font = pygame.font.Font(None, FONT_SIZE)

    # Create a calendar
    cal = calendar.Calendar()

    # Current date
    current_year = pygame.time.get_ticks() // (1000 * 60 * 60 * 24 * 365) + 2023
    current_month = (pygame.time.get_ticks() // (1000 * 60 * 60 * 24 * 30)) % 12 + 1
    current_day = pygame.time.get_ticks() // (1000 * 60 * 60 * 24) % 30 + 1

    # Calculate the position of the calendar grid
    grid_x = 0
    grid_y = FONT_SIZE + 10
    cell_width = WIDTH // 7
    cell_height = (HEIGHT - grid_y) // 7

    # Create a notes dictionary to store notes for each day
    notes = {}

    # Variable to track the text input state
    input_active = False
    input_text = ""
    
    notes = load_calendar(username)

    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for arrow key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_month -= 1
                    if current_month == 0:
                        current_month = 12
                        current_year -= 1
                elif event.key == pygame.K_RIGHT:
                    current_month += 1
                    if current_month == 13:
                        current_month = 1
                        current_year += 1
                elif event.key == pygame.K_RETURN:
                    # Save note for the current day
                    if input_text != "":
                        notes[(current_year, current_month, current_day)] = input_text
                        input_text = ""
                        save_calendar(username, notes)
                elif event.key == pygame.K_ESCAPE:
                    pass

                # Handle text input events
                if input_active:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove last character from input text
                        input_text = input_text[:-1]
                    else:
                        # Add typed character to input text
                        input_text += event.unicode

            # Check for mouse button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if the click is inside the calendar grid
                if back_button_rect.collidepoint(event.pos):
                    menu_buttons(username) 
                mouse_x, mouse_y = event.pos
                if mouse_y > grid_y:
                    row = (mouse_y - grid_y) // cell_height
                    col = mouse_x // cell_width
                    print("Row:", row)
                    print("Col:", col)

                    # Get the clicked day
                    cal_data = cal.monthdayscalendar(current_year, current_month)
                    print("cal_data:", cal_data)

                    if row < len(cal_data) and col < len(cal_data[row]):
                        day = cal_data[row][col]
                        print("Clicked day:", day)
                        
                        if day != 0:
                            current_day = day

                            # Enable text input for the clicked day
                            input_active = True
                            input_text = ""
                    else:
                        pass

        # Clear the screen
        screen.fill(WHITE)

        # Render the calendar
        cal_data = cal.monthdayscalendar(current_year, current_month)

        # Display the current month
        year_text = font.render(str(current_year), True, BLACK)
        year_text_width = year_text.get_width()
        year_text_x = (WIDTH - year_text_width) // 1
        screen.blit(year_text, (year_text_x, grid_y - FONT_SIZE - 5))

        # Display the current month
        month_name = calendar.month_name[current_month]
        month_text = font.render(month_name, True, BLACK)
        month_text_width = month_text.get_width()
        month_text_x = (WIDTH - month_text_width) // 2
        screen.blit(month_text, (month_text_x, grid_y - FONT_SIZE - 5))

        # Display the days of the week
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            text_surface = font.render(day, True, BLACK)
            screen.blit(text_surface, (i * cell_width, grid_y - FONT_SIZE + 10))

        # Display the calendar days
        for i, week in enumerate(cal_data):
            for j, day in enumerate(week):
                if day != 0:
                    text_surface = font.render(str(day), True, BLACK)

                    # Highlight the current day
                    if day == current_day:
                        pygame.draw.rect(screen, RED, (j * cell_width, grid_y + i * cell_height, cell_width, cell_height))

                    screen.blit(text_surface, (j * cell_width, grid_y + i * cell_height))

                    # Display saved notes for each day
                    if (current_year, current_month, day) in notes:
                        note_text = notes[(current_year, current_month, day)]
                        note_surface = font.render(note_text, True, GREEN)
                        screen.blit(note_surface, (j * cell_width, grid_y + i * cell_height + FONT_SIZE))

        # Display the input text
        input_surface = font.render(input_text, True, BLACK)
        screen.blit(input_surface, (cell_width, HEIGHT - FONT_SIZE))
        
        # Draw back button
        BACK_BUTTON_WIDTH = 100
        BACK_BUTTON_HEIGHT = 40
        back_button_x = (WIDTH - BACK_BUTTON_WIDTH) // 2
        back_button_y = HEIGHT - BACK_BUTTON_HEIGHT - 10
        back_button_rect = pygame.Rect(back_button_x, back_button_y, BACK_BUTTON_WIDTH, BACK_BUTTON_HEIGHT)
        back_button_color = BLACK
        pygame.draw.rect(screen, back_button_color, back_button_rect)
        back_button_font = pygame.font.Font(None, 24)
        back_button_text_rendered = back_button_font.render("Back", True, WHITE)
        back_button_text_rect = back_button_text_rendered.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text_rendered, back_button_text_rect)
        
        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

    # Save calendar edition and quit Pygame
    pygame.quit()

#Timer Section

def run_pomodoro_timer(username):
    '''
    Run the Pomodoro timer.

    Args:
        username (str): The username of the user.
    '''
    
    WIDTH, HEIGHT = screen.get_size()

    BACKDROP = pygame.image.load("assets/Backdrop1.png")#grabs the png file and makes it the backround
    WHITE_BUTTON = pygame.image.load("assets/button.png")# grabs the png file and loads it as the button

    FONT = pygame.font.Font("assets/times.ttf", 120)#The font type from a ttf file and sets the size
    timer_text = FONT.render("25:00", True, "white")#Time displayed and color it is displayed in
    timer_text_rect = timer_text.get_rect(center=(WIDTH/2, HEIGHT/2-25))# Sets the position fo the button and how it can react

# Create buttons
    startStopButton = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START", 
                        pygame.font.Font("assets/times.ttf", 20), "#c97676", "#9ab034")
    workSeshbutton = Button(None, (WIDTH/2-150, HEIGHT/2-140), 120, 30, "Work Session", 
                        pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")
    shortBreakButton = Button(None, (WIDTH/2, HEIGHT/2-140), 120, 30, "Short Break", 
                        pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")
    longBreakButton = Button(None, (WIDTH/2+150, HEIGHT/2-140), 120, 30, "Long Break", 
                        pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")

    workSession = 1500  # 1500 secs / 25 mins
    shortBreak = 300  # 300 secs / 5 mins
    longBreak = 900  # 900 secs / 15 mins
    
    backButton = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+180), 170, 60, "BACK", 
                        pygame.font.Font("assets/times.ttf", 20), "#c97676", "#9ab034")

    current_seconds = workSession
    pygame.time.set_timer(pygame.USEREVENT, 1000)# Updates the timer every 1000ms = 1s so that the timer can count down and react to button clicks
    started = False #Set so that the timer starts in a paused state

    while True:
        for event in pygame.event.get():# The list of events like mouse clicks and movement
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startStopButton.check_for_input(pygame.mouse.get_pos()):
                    if started:
                        started = False
                    else:
                        started = True
                if workSeshbutton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = workSession
                    started = False
                if shortBreakButton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = shortBreak
                    started = False
                if longBreakButton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = longBreak
                    started = False
                if backButton.check_for_input(pygame.mouse.get_pos()):
                    menu_buttons(username)
                if started:
                    startStopButton.text_input = "PAUSE"
                    startStopButton.text = pygame.font.Font("assets/times.ttf", 20).render(
                        startStopButton.text_input, True, startStopButton.base_color)
                else:
                    startStopButton.text_input = "START"
                    startStopButton.text = pygame.font.Font("assets/times.ttf", 20).render(
                        startStopButton.text_input, True, startStopButton.base_color)
            if event.type == pygame.USEREVENT and started:
                current_seconds -= 1
                if current_seconds <= 0:
                    started = False
                    subprocess.Popen(["python", "-c", "import winsound; winsound.Beep(440, 4000)"])  # Play the beep sound

        screen.fill((0, 0, 0))
        screen.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH/2, HEIGHT/2)))

# Update and change color of buttons
        startStopButton.update(screen)
        startStopButton.change_color(pygame.mouse.get_pos())
        workSeshbutton.update(screen)
        workSeshbutton.change_color(pygame.mouse.get_pos())
        shortBreakButton.update(screen)
        shortBreakButton.change_color(pygame.mouse.get_pos())
        longBreakButton.update(screen)
        longBreakButton.change_color(pygame.mouse.get_pos())
        backButton.update(screen)
        backButton.change_color(pygame.mouse.get_pos())

        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
        timer_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        screen.blit(timer_text, timer_text_rect)

        pygame.display.flip()
        

#Menu Section

def menu_button_action(label, username):
    '''
    Function organizes all run functions into if statements. Whenever the button of one of these features is called, it will
    run the function corresponding to that feature. 
    Parameter: label is the button labels for the button buttons and is used to describe when one of the buttons is selected
    Parameter: username is to specify the account information of the user so that their work gets saved and loaded to their folders
    Return: N/A
    '''
    if label == "Whiteboard":
        run_whiteboard(username)
    elif label == "Kanban Board":
        run_kanban_main(username)
    elif label == "Calendar":
        run_calendar(username)
    elif label == "Timer":
        run_pomodoro_timer(username)
    elif label == "Exit":
        pygame.quit()
        sys.exit()

def menu_buttons(username):
    '''
    Function runs the menu buttons and draws the button shapes with the button labels. Also it uses a while loop to iterate the application
    when it runs. 
    Parameter: username recognizes who is using the code and saves and loads according to the user
    Return: N/A
    '''
    clock = pygame.time.Clock()

    #Determine labels, color and position of the menu buttons
    button_labels = ["Whiteboard", "Kanban Board", "Calendar", "Timer", "Exit"]
    button_width = 200
    button_height = 50
    button_spacing = 20
    button_font = pygame.font.Font(None, 24)
    button_color = BLACK
    button_text_color = WHITE

    #While loop to run the GUI
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
                        

        screen.fill(WHITE)
        
        #Iterate labels for multiple buttons and the drawing of each button
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
        clock.tick(60)


#Login Section

max_length_login_signup = 12

def login():
    '''
    Displays a login screen for the application

    The function sets up the screen and handles user inputs for entering a username and password with 
    buttons for logging in,signing up for an acount(which runs the signup() function).
    it validates the login credentials by comparig them to a csv file containing the userdata(usernames and passwords).
    if the login is succesful it runs the menu function for the specic accounts
    '''
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
    pygame.quit()

def signup():
    """
    Displays a signup screen where users can create a new account for KanBoard.5.

    The function sets up the screen, handles user input for entering a new username and password,
    and provides buttons for signing up or going back to the login screen. It validates the input,
    checks if the username is already taken, and creates a new account by appending the username and password
    to a CSV file. If the signup is successful, it displays a confirmation message and transitions to the login screen.

    """
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
    
#Run login page as first page 
if __name__ == '__main__':
    login()