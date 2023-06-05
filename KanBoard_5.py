import pygame
import sys

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

if __name__ == "__main__":
    menu_buttons()