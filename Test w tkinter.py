import tkinter as tk

def run_timer():
    # Define some colors
    BLACK = "#000000"
    WHITE = "#FFFFFF"

    root = tk.Tk()
    root.title("Timer")

    # Create the canvas
    canvas = tk.Canvas(root, width=700, height=500, bg=WHITE)
    canvas.pack()

    # Used to manage how fast the screen updates
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
    button_x = 200
    button_y = 300
    button_rect = (button_x, button_y, button_x + button_width, button_y + button_height)

    def on_key(event):
        nonlocal start_time_input_complete
        nonlocal start_time

        if not start_time_input_complete:
            # Check if the pressed key is a number
            if event.char.isdigit():
                start_time += event.char  # Append the pressed number key to the start time string
            # Check if the pressed key is the Backspace key
            elif event.keysym == "BackSpace":
                start_time = start_time[:-1]  # Remove the last character from the start time string
            # Check if the pressed key is the Enter key
            elif event.keysym == "Return":
                if start_time != "":
                    start_time = int(start_time)  # Convert the start time string to an integer
                    start_time_input_complete = True

    def on_mouse(event):
        nonlocal timer_running

        if event.x >= button_rect[0] and event.x <= button_rect[2] and event.y >= button_rect[1] and event.y <= button_rect[3]:
            timer_running = True

    def draw_screen():
        nonlocal frame_count

        # Clear the canvas
        canvas.delete("all")

        # Display start time input prompt until input is complete
        if not start_time_input_complete:
            prompt_string = "Enter start time in seconds: " + start_time
            canvas.create_text(250, 250, text=prompt_string, fill=BLACK)
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

            # Draw the timer text
            canvas.create_text(250, 250, text=output_string, fill=BLACK)

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

                # Draw the timer text
                canvas.create_text(250, 280, text=output_string, fill=BLACK)

        # Draw the start button
        canvas.create_rectangle(button_rect, fill=BLACK)
        canvas.create_text(button_x + button_width/2, button_y + button_height/2, text="Start", fill=WHITE)

        # Check if the timer is running and reset the frame count if the button is clicked again
        if not timer_running:
            frame_count = 0

        # Increment the frame count
        frame_count += 1

        # Schedule the next update
        root.after(1000 // frame_rate, draw_screen)

    # Bind keyboard events
    root.bind("<Key>", on_key)

    # Bind mouse events
    canvas.bind("<Button-1>", on_mouse)

    # Start the game loop
    draw_screen()

    # Start the main tkinter event loop
    root.mainloop()

run_timer()
