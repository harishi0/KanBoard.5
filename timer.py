import time
from tkinter import *
from tkinter import messagebox

def run_timer():
    def submit():
        nonlocal paused, initial_time
        if paused:
            paused = False
        else:
            try:
                initial_time = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
            except ValueError:
                messagebox.showerror("Error", "Please input the right value")
                return

            temp = initial_time
            while temp > -1 and not paused:
                mins, secs = divmod(temp, 60)
                hours = 0

                if mins > 60:
                    hours, mins = divmod(mins, 60)

                hour.set("{0:02d}".format(hours))
                minute.set("{0:02d}".format(mins))
                second.set("{0:02d}".format(secs))

                root.update()
                time.sleep(1)

                if temp == 0:
                    messagebox.showinfo("Time Countdown", "Time's up")

                temp -= 1

    def pause():
        nonlocal paused
        paused = not paused

    def reset():
        nonlocal paused, initial_time
        hour.set("{0:02d}".format(initial_time // 3600))
        minute.set("{0:02d}".format((initial_time // 60) % 60))
        second.set("{0:02d}".format(initial_time % 60))
        paused = False

    root = Tk()
    root.geometry("300x250")
    root.title("Time Counter")
    root.configure(bg="black")

    hour = StringVar()
    minute = StringVar()
    second = StringVar()

    hour.set("00")
    minute.set("00")
    second.set("00")

    hourEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=hour)
    hourEntry.place(x=80, y=20)

    minuteEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=minute)
    minuteEntry.place(x=130, y=20)

    secondEntry = Entry(root, width=3, font=("Arial", 18, ""), textvariable=second)
    secondEntry.place(x=180, y=20)

    btn = Button(root, text='Start Timer', bd='5', command=submit)
    btn.place(x=70, y=120)

    pause_btn = Button(root, text='Pause', bd='5', command=pause)
    pause_btn.place(x=170, y=120)

    reset_btn = Button(root, text='Reset', bd='5', command=reset)
    reset_btn.place(x=130, y=160)

    paused = False
    initial_time = 0

    root.mainloop()

run_timer()
