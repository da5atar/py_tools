'''
pomudora.py
------------------

This Python automation script enhances the Pomodoro Technique by adding a Forced device lock once the timer runs out.

The script creates a simple Pomodoro timer GUI using Tkinter that counts down from 25 minutes. When the timer reaches zero, the script locks the screen to enforce a break.

The script uses the `ctypes` library to lock the screen on Windows and provides a placeholder for macOS and Linux systems.

To run the script, save it as `pomudora.py` and execute it using Python. The GUI will appear, and you can start the timer by clicking the "Start" button.

Author: Abhay Parashar https://medium.com/@abhayparashar31

'''

import tkinter as tk
import time
import ctypes
import os
from threading import Timer

class PomodoroTimer:
    '''
    PomodoroTimer class that creates a simple GUI using Tkinter to implement the Pomodoro Technique.
    The timer counts down from 25 minutes, and locks the screen when it reaches 0.

    Attributes:
    - root: The Tkinter root window
    - time_var: A Tkinter StringVar to store the time display
    - running: A boolean flag to track if the timer is running
    - paused: A boolean flag to track if the timer is paused
    - remaining_time: The remaining time on the timer in seconds (default: 25 minutes)

    Methods:
    - update_time: Updates the timer display every second
    - start_timer: Starts the timer countdown
    - pause_timer: Pauses the timer
    - reset_timer: Resets the timer to the default 25 minutes
    - lock_screen: Locks the screen to enforce a break once the timer reaches zero
    '''
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        self.time_var = tk.StringVar()
        self.time_var.set("25:00")
        self.running = False
        self.paused = False
        self.remaining_time = 25 * 60  # 25 minutes

        self.label = tk.Label(root, textvariable=self.time_var, font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def update_time(self):
        '''
        Update the timer display every second and lock the screen when the timer reaches zero.
        The timer runs in a separate thread using the `after` method of Tkinter to
        avoid blocking the main GUI thread.
        The method checks if the timer is paused or running to handle the timer state correctly.
        '''
        if self.running:
            minutes, seconds = divmod(self.remaining_time, 60)
            self.time_var.set(f"{minutes:02}:{seconds:02}")
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.update_time)
            else:
                self.running = False
                self.lock_screen()

    def start_timer(self):
        '''
        Start the timer countdown.
        '''
        if not self.running:
            self.running = True
            self.paused = False
            self.update_time()

    def pause_timer(self):
        '''
        Pause the timer.
        '''
        if self.running:
            self.running = False
            self.paused = True

    def reset_timer(self):
        '''
        Reset the timer to the default 25 minutes.
        '''
        self.running = False
        self.paused = False
        self.remaining_time = 25 * 60
        self.time_var.set("25:00")

    def lock_screen(self):
        '''
        Lock the screen to enforce a break once the timer reaches zero.
        '''
        if os.name == 'nt':  # Windows
            ctypes.windll.user32.LockWorkStation()
        elif os.name == 'posix':  # macOS and Linux
            # This is a placeholder, as locking the screen in macOS/Linux typically requires different handling
            os.system(r'/System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend')
            # For Linux, use: os.system('gnome-screensaver-command --lock')
            print("Locking screen on macOS/Linux is not implemented in this script.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()