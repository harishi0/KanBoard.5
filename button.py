import pygame

class Button():
    """
    A class representing a button in a graphical user interface.

    Attributes:
        surface (pygame.Surface): The surface of the button.
        x_pos (int): The x-coordinate position of the button.
        y_pos (int): The y-coordinate position of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        font (pygame.font.Font): The font used for the button's text.
        base_color (str): The base color of the button.
        hovering_color (str): The color of the button when the mouse hovers over it.
        text_input (str): The input text displayed on the button.
        text (pygame.Surface): The rendered text surface.
        rect (pygame.Rect): The rectangular area occupied by the button.
        text_rect (pygame.Rect): The rectangular area occupied by the text.

    Methods:
        update(screen: pygame.Surface): Renders the button on the screen.
        check_for_input(position: tuple[int, int]) -> bool: Checks if the given position is within the button area.
        change_color(position: tuple[int, int]): Changes the button color based on the given position.
    """
    def __init__(self, surface=None, pos=None, width=None, height=None, text_input=None, font=None, base_color=None, hovering_color=None):
        """
        Initializes a Button instance.

        Args:
            surface (pygame.Surface, optional): The surface of the button. If None, the button will be text-only.
            pos (tuple[int, int]): The position of the button (x, y).
            width (int): The width of the button.
            height (int): The height of the button.
            text_input (str): The input text displayed on the button.
            font (pygame.font.Font): The font used for the button's text.
            base_color (str): The base color of the button.
            hovering_color (str): The color of the button when the mouse hovers over it.
        """
        self.surface = surface
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = width
        self.height = height
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.surface is None:
            self.surface = self.text
        else:
            self.surface = pygame.transform.smoothscale(self.surface, (width, height))
        self.rect = self.surface.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        """
        Renders the button on the given screen.

        Args:
            screen (pygame.Surface): The surface to render the button on.
        """
        if self.surface is not None:
            screen.blit(self.surface, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        """
        Checks if the given position is within the button area.

        Args:
            position (tuple[int, int]): The position to check (x, y).

        Returns:
            bool: True if the position is within the button area, False otherwise.
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def change_color(self, position):
        """
        Changes the button color based on the given position.

        Args:
            position (tuple[int, int]): The position to check (x, y).
        """
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
