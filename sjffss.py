import pygame
import calendar

# Initialize Pygame
pygame.init()

# Set window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set font
FONT_SIZE = 24
font = pygame.font.Font(None, FONT_SIZE)

# Create a calendar
cal = calendar.Calendar()

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Calendar")

# Current date
current_year = pygame.time.get_ticks() // (1000 * 60 * 60 * 24 * 365) + 1970
current_month = (pygame.time.get_ticks() // (1000 * 60 * 60 * 24 * 30)) % 12 + 1
current_day = pygame.time.get_ticks() // (1000 * 60 * 60 * 24) % 30 + 1

# Calculate the position of the calendar grid
grid_x = 0
grid_y = FONT_SIZE + 10
cell_width = WINDOW_WIDTH // 7
cell_height = (WINDOW_HEIGHT - grid_y) // 7

# Create a notes dictionary to store notes for each day
notes = {}

# Variable to track the text input state
input_active = False
input_text = ""

# Function to save the calendar edition
def save_calendar():
    try:
        with open("calendar_notes.txt", "w") as file:
            for date, note in notes.items():
                file.write(f"{date[0]},{date[1]},{date[2]}:{note}\n")
        print("Calendar edition saved successfully.")
    except IOError:
        print("Error occurred while saving the calendar edition.")

# Function to load the calendar edition
def load_calendar():
    try:
        with open("calendar_notes.txt", "r") as file:
            for line in file:
                parts = line.strip().split(":")
                date_parts = parts[0].split(",")
                year = int(date_parts[0])
                month = int(date_parts[1])
                day = int(date_parts[2])
                note = parts[1]
                notes[(year, month, day)] = note
        print("Calendar edition loaded successfully.")
    except FileNotFoundError:
        print("Calendar edition file not found.")
    except IOError:
        print("Error occurred while loading the calendar edition.")

# Load the calendar edition
load_calendar()

# Main game loop
try:
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
                        save_calendar()
                elif event.key == pygame.K_ESCAPE:
                    # Save and exit the program
                    save_calendar()
                    running = False

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
                mouse_x, mouse_y = event.pos
                if mouse_y > grid_y:
                    row = (mouse_y - grid_y) // cell_height
                    col = mouse_x // cell_width

                    # Get the clicked day
                    cal_data = cal.monthdayscalendar(current_year, current_month)
                    day = cal_data[row][col]

                    if day != 0:
                        current_day = day

                        # Enable text input for the clicked day
                        input_active = True
                        input_text = ""

        # Clear the window
        window.fill(WHITE)

        # Render the calendar
        cal_data = cal.monthdayscalendar(current_year, current_month)
        
        # Display the current month
        month_name = calendar.month_name[current_month]
        month_text = font.render(month_name, True, BLACK)
        month_text_width = month_text.get_width()
        month_text_x = (WINDOW_WIDTH - month_text_width) // 2
        window.blit(month_text, (month_text_x, grid_y - FONT_SIZE - 5))

        # Display the days of the week
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days_of_week):
            text_surface = font.render(day, True, BLACK)
            window.blit(text_surface, (i * cell_width, grid_y - FONT_SIZE + 10))

        # Display the calendar days
        for i, week in enumerate(cal_data):
            for j, day in enumerate(week):
                if day != 0:
                    text_surface = font.render(str(day), True, BLACK)

                    # Highlight the current day
                    if day == current_day:
                        pygame.draw.rect(window, RED, (j * cell_width, grid_y + i * cell_height, cell_width, cell_height))

                    window.blit(text_surface, (j * cell_width, grid_y + i * cell_height))

                    # Display saved notes for each day
                    if (current_year, current_month, day) in notes:
                        note_text = notes[(current_year, current_month, day)]
                        note_surface = font.render(note_text, True, GREEN)
                        window.blit(note_surface, (j * cell_width, grid_y + i * cell_height + FONT_SIZE))

        # Display the input text
        input_surface = font.render(input_text, True, BLACK)
        window.blit(input_surface, (cell_width, WINDOW_HEIGHT - FONT_SIZE))

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        clock.tick(60)

except Exception as e:
    print("An error occurred:", str(e))

# Save calendar edition and quit Pygame
save_calendar()
pygame.quit()
