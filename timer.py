import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# Set the height and width of the screen
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Timer")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

font = pygame.font.Font(None, 25)

frame_count = 0
frame_rate = 60

# Flag to determine if start time input is complete
start_time_input_complete = False
start_time = ""

# Flag to determine if the timer is running
timer_running = False

# Button dimensions and properties
button_width = 100
button_height = 50
button_x = 300
button_y = 200
button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Check for keyboard events
        if event.type == pygame.KEYDOWN:
            # If start time input is not complete
            if not start_time_input_complete:
                # Check if the key pressed is a number key
                if pygame.K_0 <= event.key <= pygame.K_9:
                    start_time += pygame.key.name(event.key)  # Append the pressed number key to the start time string
                # Check if the key pressed is the Backspace key
                elif event.key == pygame.K_BACKSPACE:
                    start_time = start_time[:-1]  # Remove the last character from the start time string
                # Check if the key pressed is the Enter key
                elif event.key == pygame.K_RETURN:
                    if start_time != "":
                        start_time = int(start_time)  # Convert the start time string to an integer
                        start_time_input_complete = True

        # Check for mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the left mouse button is clicked within the button rectangle
            if event.button == 1 and button_rect.collidepoint(event.pos):
                timer_running = True

    # Set the screen background
    screen.fill(WHITE)

    # Display start time input prompt until input is complete
    if not start_time_input_complete:
        prompt_string = "Enter start time in seconds: " + start_time
        prompt_text = font.render(prompt_string, True, BLACK)
        screen.blit(prompt_text, [250, 250])
    else:
        # --- Timer going up ---
        # Calculate total seconds
        total_seconds = frame_count // frame_rate

        # Divide by 60 to get total minutes
        minutes = total_seconds // 60

        # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60

        # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

        # Blit to the screen
        text = font.render(output_string, True, BLACK)
        screen.blit(text, [250, 250])

        # --- Timer going down ---
        if timer_running:
            # Calculate total seconds
            total_seconds = start_time - (frame_count // frame_rate)
            if total_seconds < 0:
                total_seconds = 0
            # Divide by 60 to get total minutes
            minutes = total_seconds // 60

            # Use modulus (remainder) to get seconds
            seconds = total_seconds % 60

            # Use python string formatting to format in leading zeros
            output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)

            # Blit to the screen
            text = font.render(output_string, True, BLACK)

            screen.blit(text, [250, 280])

    # Draw the start button
    pygame.draw.rect(screen, BLACK, button_rect)
    button_text = font.render("Start", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    # Check if the timer is running and reset the frame count if the button is clicked again
    if not timer_running:
        frame_count = 0

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

    frame_count += 1

    # Limit frames per second
    clock.tick(frame_rate)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()


