import pyautogui
import threading
import time
import tkinter as tk
from pynput import keyboard

clicking = False  # Flag to track clicking state
click_thread = None  # Thread for clicking loop
sleep_time = 0.5  # Default sleep time
hold_time = 0.5  # Default hold time 

def click_loop():
    # Simulate holding the mouse button down for hold_time seconds, then use the sleep_time.
    while clicking:
        pyautogui.mouseDown()
        time.sleep(hold_time)  
        pyautogui.mouseUp()
        time.sleep(sleep_time)

def toggle_clicking():
    # Toggles clicking on/off and updates the GUI.
    global clicking, click_thread
    
    clicking = not clicking  # Switch state
    if clicking:
        status_label.config(
        text=f"Status: Clicking\nDelay: {sleep_time:.3f}s | Hold: {hold_time:.3f}s", 
        fg="green"
    )

    else:
        status_label.config(text="Status: Stopped", fg="red")
    
    instructions_label.config(text="Press F6 to start/stop", fg="black")  # Instructions
    if clicking:
        click_thread = threading.Thread(target=click_loop, daemon=True)
        click_thread.start()

def on_press(key):
    # Listens for the F6 key to toggle autoclicking.
    if key == keyboard.Key.f6:
        toggle_clicking()

def update_sleep_time_from_slider(value):
    # Updates the sleep time based on the slider.
    global sleep_time
    sleep_time = round(float(value), 3)  
    sleep_time_entry.delete(0, tk.END) 
    sleep_time_entry.insert(0, str(sleep_time))
    if clicking:
        status_label.config(text=f"Status: Clicking (Delay: {sleep_time:.3f}s, Hold: {hold_time:.3f}s)", fg="green")

def update_sleep_time_from_entry():
    # Updates the sleep time based on the typed entry value.
    global sleep_time
    try:
        sleep_time = round(float(sleep_time_entry.get()), 3)
        sleep_time_slider.set(sleep_time)
        if clicking:
            status_label.config(text=f"Status: Clicking (Delay: {sleep_time:.3f}s, Hold: {hold_time:.3f}s)", fg="green")
    except ValueError:
        pass  # Ignore invalid input

def update_hold_time_from_slider(value):
    # Updates the hold time based on the slider.
    global hold_time
    hold_time = round(float(value), 3)  
    hold_time_entry.delete(0, tk.END) 
    hold_time_entry.insert(0, str(hold_time))
    if clicking:
        status_label.config(text=f"Status: Clicking (Delay: {sleep_time:.3f}s, Hold: {hold_time:.3f}s)", fg="green")

def update_hold_time_from_entry():
    # Updates the hold time based on the typed entry value.
    global hold_time
    try:
        hold_time = round(float(hold_time_entry.get()), 3)
        hold_time_slider.set(hold_time)
        if clicking:
            status_label.config(text=f"Status: Clicking (Delay: {sleep_time:.3f}s, Hold: {hold_time:.3f}s)", fg="green")
    except ValueError:
        pass  # Ignore invalid input

# Start listening for keypresses in a separate thread
keyboard_listener = keyboard.Listener(on_press=on_press)
keyboard_listener.start()

# GUI
root = tk.Tk()
root.title("Autoclicker")
root.geometry("300x400")
root.resizable(False, False)

status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12), fg="red")
status_label.pack(pady=10)

# Slider for adjusting the delay time
sleep_time_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", label="Click Delay (s)", resolution=0.001, length=200)
sleep_time_slider.set(sleep_time)
sleep_time_slider.pack(pady=10)

# Update the sleep time when the slider is moved
sleep_time_slider.bind("<Motion>", lambda event: update_sleep_time_from_slider(sleep_time_slider.get()))

# Entry field for manual sleep time input
sleep_time_entry_label = tk.Label(root, text="Enter Delay (s):")
sleep_time_entry_label.pack()

sleep_time_entry = tk.Entry(root)
sleep_time_entry.insert(0, str(sleep_time))
sleep_time_entry.pack(pady=5)

# Bind the entry field to update sleep time when the user presses Enter
sleep_time_entry.bind("<Return>", lambda event: update_sleep_time_from_entry())

hold_time_slider = tk.Scale(root, from_=0, to=10, orient="horizontal", label="Click Hold (s)", resolution=0.001, length=200)
hold_time_slider.set(hold_time)
hold_time_slider.pack(pady=10)

# Update the hold time when the slider is moved
hold_time_slider.bind("<Motion>", lambda event: update_hold_time_from_slider(hold_time_slider.get()))

hold_time_entry_label = tk.Label(root, text="Enter Hold (s):")
hold_time_entry_label.pack()

hold_time_entry = tk.Entry(root)
hold_time_entry.insert(0, str(hold_time))
hold_time_entry.pack(pady=5)

hold_time_entry.bind("<Return>", lambda event: update_hold_time_from_entry())

# Instructions
instructions_label = tk.Label(root, text="Press F6 to Start/Stop", font=("Arial", 17), fg="black")
instructions_label.pack(pady=10)

root.mainloop()
