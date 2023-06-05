import tkinter as tk

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
        exit()

def menu_buttons():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Menu Buttons")

    button_labels = ["Whiteboard", "Kanban Board", "Calendar", "Timer", "Exit"]

    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(side="bottom", pady=20)

    for label in button_labels:
        button = tk.Button(button_frame, text=label, width=20, height=2, fg="white", bg="black", command=lambda l=label: menu_button_action(l))
        button.pack(side="left", padx=10)

    # Add an empty label to center-align the buttons
    empty_label = tk.Label(button_frame, bg="white")
    empty_label.pack(side="left", expand=True, fill="x")

    root.mainloop()

if __name__ == "__main__":
    menu_buttons()