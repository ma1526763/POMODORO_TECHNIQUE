from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
BLUE = "#DFE9F5"
B_GREEN = "#2db83d"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
to_do = 0
tick_count = ""
timer = ""
def repeative_properties(bg, fg, text):
    window.config(background=bg)
    timer_label.config(text=text, foreground=fg, background=bg)
    tick_label.config(background=bg)
    canvas.config(background=bg, highlightbackground=bg)

# TIMER MECHANISM
def start_pomodoro():
    start_button.config(state="disabled", bg=GREEN)
    reset_button.config(state="normal", bg=RED)
    # Restore if window is minimized
    window.state("normal")
    # Bring to top level above all windows
    window.attributes("-topmost", True)
    # Allows other windows to top level again
    window.attributes("-topmost", False)

    global to_do
    to_do += 1
    if to_do % 8 == 0:
        repeative_properties(BLUE, RED, "Break")
        count_down(LONG_BREAK_MIN * 60)
    elif to_do % 2 == 1:
        repeative_properties(YELLOW, B_GREEN, "Timer")
        count_down(WORK_MIN * 60)
    elif to_do % 2 == 0:
        repeative_properties(BLUE, PINK, "Break")
        count_down(SHORT_BREAK_MIN * 60)

# COUNTDOWN MECHANISM
def count_down(seconds):
    global timer
    remaining_seconds = str(int(seconds) % 60)
    remaining_minutes = str(int(seconds) // 60)
    if int(remaining_seconds) < 10:
        remaining_seconds = f"0{remaining_seconds}"
    if int(remaining_minutes) < 10:
        remaining_minutes = f"0{remaining_minutes}"
    canvas.itemconfig(timer_text, text=f"{remaining_minutes}:{remaining_seconds}")
    if seconds >= 0:
        timer = window.after(1000, count_down, seconds - 1)
    else:
        if to_do % 2 == 1:
            global tick_count
            tick_count += "✅"
            tick_label.config(text=tick_count)
        start_pomodoro()

# TIMER RESET
def reset_pomodoro():
    start_button.config(state="normal", bg=B_GREEN)
    reset_button.config(state="disabled", bg=PINK)
    global to_do, tick_count
    window.after_cancel(timer)
    to_do = 0
    tick_count = ""
    timer_label.config(text="Timer", foreground=B_GREEN, background=YELLOW)
    tick_label.config(text=tick_count)
    canvas.itemconfig(timer_text, text="00:00")


# UI SETUP
window = Tk()
window.title("Pomodoro Technique")

window.minsize(600, 500)
window.maxsize(600, 500)
window.iconphoto(False, PhotoImage(file='tomato.png'))
window.config(background=YELLOW, padx=100, pady=50)
canvas = Canvas(window, width=203, height=225, background=YELLOW, highlightbackground=YELLOW)
canvas.grid(row=1, column=1)
img = PhotoImage(file='tomato.png')  # transparent image
canvas.create_image(102, 112, image=img)
timer_text = canvas.create_text(106, 140, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

start_button = Button(text="Start", highlightthickness=0, command=start_pomodoro,
                      activebackground=GREEN, bg=B_GREEN, fg=YELLOW, font=(FONT_NAME, 20, "bold"), relief="flat")
start_button.grid(row=2, column=0)


reset_button = Button(text="Reset", highlightthickness=0, command=reset_pomodoro,
                      activebackground=PINK, bg=PINK, fg=YELLOW, font=(FONT_NAME, 20, "bold"), relief="flat", state="disabled")

reset_button.grid(row=2, column=2)
timer_label = Label(text="Timer", foreground=B_GREEN, font=(FONT_NAME, 40, "bold"), background=YELLOW, pady=10)
timer_label.grid(row=0, column=1)

tick_label = Label(text=tick_count, foreground=B_GREEN, font=(FONT_NAME, 14, "bold"), pady=20, background=YELLOW)
tick_label.grid(row=3, column=1)

window.mainloop()
