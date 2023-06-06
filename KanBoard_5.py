import pygame
from pygame.locals import *
import os
import csv

def login():
    pygame.init()

    # Set up the screen
    screen = pygame.display.set_mode((0, 0), FULLSCREEN)
    pygame.display.set_caption("Log into KanBoard.5")
    screen_width, screen_height = pygame.display.get_surface().get_size()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (220, 220, 220)

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
    
    
    
    
