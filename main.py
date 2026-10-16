#!/usr/bin/env python3

import serial
import tkinter as tk
from tkinter import font

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

def parse_nmea_sentence(sentence):
    if sentence.startswith('$GPRMC'):
        parts = sentence.split(',')
        if len(parts) > 7 and parts[2] == 'A':
            try:
                speed_knots = float(parts[7])
                return speed_knots
            except ValueError:
                pass
    return None

def update_speed():
    try:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        if line:
            speed_knots = parse_nmea_sentence(line)
            if speed_knots is not None:
                speed_kmh = speed_knots * 1.852
                speed_mph = speed_knots * 1.15078
                label_kmh.config(text=f"{speed_kmh:.1f}")
                label_mph.config(text=f"{speed_mph:.1f}")
                status_label.config(text="GPS FIX ACTIVE", fg='green')
            else:
                status_label.config(text="WAITING FOR GPS FIX...", fg='red')
    except Exception as e:
        status_label.config(text="READ ERROR", fg='orange')
    root.after(100, update_speed)

root = tk.Tk()
root.title("GPS Speedometer")
root.attributes('-fullscreen', True)
root.configure(background='black')

big_font = font.Font(family="Helvetica", size=120, weight="bold")
medium_font = font.Font(family="Helvetica", size=48, weight="bold")
small_font = font.Font(family="Helvetica", size=36)

label_kmh = tk.Label(root, text="0.0", font=big_font, fg="white", bg="black")
label_kmh.pack(expand=True)

kmh_unit = tk.Label(root, text="km/h", font=medium_font, fg="white", bg="black")
kmh_unit.pack()

label_mph = tk.Label(root, text="0.0", font=big_font, fg="cyan", bg="black")
label_mph.pack(expand=True)

mph_unit = tk.Label(root, text="mph", font=medium_font, fg="cyan", bg="black")
mph_unit.pack()

status_label = tk.Label(root, text="INITIALIZING...", font=small_font, fg="yellow", bg="black")
status_label.pack(pady=20)

exit_label = tk.Label(root, text="Press ESC to exit", font=small_font, fg="gray", bg="black")
exit_label.pack(side='bottom')

def quit_app(event=None):
    ser.close()
    root.destroy()
root.bind('<Escape>', quit_app)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    root.after(1000, update_speed)
    root.mainloop()
except serial.SerialException as e:
    print(f"Error: {e}")
    root.mainloop()