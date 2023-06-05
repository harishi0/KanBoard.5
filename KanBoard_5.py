import pygame
from pygame.locals import *
import tkinter as tk
from tkinter import colorchooser

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 191, 255)
WHITE = (255, 255, 255)
GREY = (220, 220, 220)

# Background color
background_color = WHITE

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

    if button_states["canvas_rect"].collidepoint(pos):
        start_drawing(pos, button_states)

    if button_states["black"]:
        button_states["color"] = BLACK
    elif button_states["blue"]:
        button_states["color"] = BLUE
    elif button_states["eraser"]:
        button_states["color"] = background_color
    elif button_states["clear"]:
        clear_canvas(button_states["canvas"])
    elif button_states["save"]:
        save_canvas(button_states["canvas"])
    elif button_states["load"]:
        load_canvas(button_states)
    elif button_states["back"]:
        back_button_action()

    if button_states["color_picker"]:
        button_states["color"] = choose_color()

def back_button_action():
    print("Back button clicked")
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
            pygame.draw.circle(button_states["canvas"], color, (x, y), button_states["slider_width"] // 2)

        button_states["last_pos"] = pos

def clear_canvas(canvas):
    canvas.fill(background_color)

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

def save_canvas(canvas):
    pygame.image.save(canvas, "whiteboard.png")
    print("Canvas saved as whiteboard.png")

def load_canvas(button_states):
    try:
        button_states["canvas"] = pygame.image.load("whiteboard.png").convert()
        print("Canvas loaded from whiteboard.png")
    except pygame.error:
        print("Could not load canvas from whiteboard.png")

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
    canvas = pygame.Surface((info.current_w, info.current_h))
    canvas.fill(background_color)

    # Button properties
    button_states = {
        "canvas": canvas,
        "canvas_rect": pygame.Rect(0, 0, info.current_w, info.current_h),
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

        screen.fill(GREY)
        screen.blit(button_states["canvas"], (0, 0))

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

run()