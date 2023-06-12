import pygame
import sys
from button import Button
import subprocess

def run_pomodoro_timer():
    '''
    Sets the width and hight of the timer
    '''
    pygame.init() # initializes all the available pygame modules and prepares them for use.

    width, height = 700, 600
    timerDisplay = pygame.display.set_mode((width, height))#Displays based on the width and hight 
    pygame.display.set_caption("Pomodoro") #Sets a caption at the top of the display

    CLOCK = pygame.time.Clock()#creates a Clock object from the pygame.time module

    backroundColor = pygame.image.load("assets/Backdrop1.png") #grabs the png file and makes it the backround
    WHITE_BUTTON = pygame.image.load("assets/button.png") # grabs the png file and loads it as the button

    textfont = pygame.font.Font("assets/times.ttf", 150)#The font type from a ttf file and sets the size
    timer_text = textfont.render("25:00", True, "white") #Time displayed and color it is displayed in
    timer_text_rect = timer_text.get_rect(center=(width/2, height/2-25))# Sets the position fo the button and how it can react

    # Create buttons
    startStopButton = Button(WHITE_BUTTON, (width/2, height/2+100), 170, 60, "START",
                             pygame.font.Font("assets/times.ttf", 20), "#c97676", "#9ab034") #Grabs the font and assigns colors based on when it is clicked
    workSeshbutton = Button(None, (width/2-150, height/2-140), 120, 30, "Work Session",
                            pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")
    shortBreakButton = Button(None, (width/2, height/2-140), 120, 30, "Short Break",
                              pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")
    longBreakButton = Button(None, (width/2+150, height/2-140), 120, 30, "Long Break",
                             pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")
    resetButton = Button(None, (width/2, height/2+200), 170, 60, "RESET",
                         pygame.font.Font("assets/times.ttf", 20), "#FFFFFF", "#9ab034")

    workSession = 1500  # 1500 secs / 25 mins
    shortBreak = 300  # 300 secs / 5 mins
    longBreak = 900  # 900 secs / 15 mins

    current_seconds = workSession
    initial_seconds = workSession  # Store initial time
    pygame.time.set_timer(pygame.USEREVENT, 1000)# Updates the timer every 1000ms = 1s so that the timer can count down and react to button clicks
    started = False #Set so that the timer starts in a paused state

    while True:
        for event in pygame.event.get():# The list of events like mouse clicks and movement
            if event.type == pygame.QUIT:
                pygame.quit()#}Properly exits the timer
                sys.exit()####}
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle button clicks
                if startStopButton.check_for_input(pygame.mouse.get_pos()):
                    if started:
                        started = False
                    else:
                        started = True
                if workSeshbutton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = workSession
                    initial_seconds = workSession  # Update initial time
                    started = False
                if shortBreakButton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = shortBreak
                    initial_seconds = shortBreak  # Update initial time
                    started = False
                if longBreakButton.check_for_input(pygame.mouse.get_pos()):
                    current_seconds = longBreak
                    initial_seconds = longBreak  # Update initial time
                    started = False
                if resetButton.check_for_input(pygame.mouse.get_pos()):  # Reset button clicked
                    current_seconds = initial_seconds  # Reset the timer to initial value
                    started = False
                    startStopButton.text_input = "START"
                    startStopButton.text = pygame.font.Font("assets/times.ttf", 20).render(
                        startStopButton.text_input, True, startStopButton.base_color)
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

        timerDisplay.fill((0, 0, 0))
        timerDisplay.blit(backroundColor, backroundColor.get_rect(center=(width/2, height/2)))

        # Update and change color of buttons
        startStopButton.update(timerDisplay)
        startStopButton.change_color(pygame.mouse.get_pos())
        workSeshbutton.update(timerDisplay)
        workSeshbutton.change_color(pygame.mouse.get_pos())
        shortBreakButton.update(timerDisplay)
        shortBreakButton.change_color(pygame.mouse.get_pos())
        longBreakButton.update(timerDisplay)
        longBreakButton.change_color(pygame.mouse.get_pos())
        resetButton.update(timerDisplay)
        resetButton.change_color(pygame.mouse.get_pos())

        if current_seconds >= 0:
            display_seconds = current_seconds % 60
            display_minutes = int(current_seconds / 60) % 60
        timer_text = textfont.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
        timerDisplay.blit(timer_text, timer_text_rect)

        pygame.display.update()

run_pomodoro_timer()
