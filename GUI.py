import tkinter as tk
import customtkinter as ck

import pandas as pd
import numpy as np
import pickle

import mediapipe as mp
import cv2
from PIL import Image, ImageTk


def reset_counter():
    pass


window = tk.Tk()
window.geometry("960x540")
window.title("Human Hand Tracking System")
ck.set_appearance_mode("dark")

# lables
classLabel = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="black", padx=10)
classLabel.place(x=10, y=1)
classLabel.configure(text='STAGE')

counterLabel = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="black", padx=10)
counterLabel.place(x=160, y=1)
counterLabel.configure(text='REPS')

probLabel = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="black", padx=10)
probLabel.place(x=300, y=1)
probLabel.configure(text='PROB')

classBox = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="white", fg_color="blue")
classBox.place(x=10, y=41)
classBox.configure(text='0')

counterBox = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="white", fg_color="blue")
counterBox.place(x=160, y=41)
counterBox.configure(text='0')

probBox = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="white", fg_color="blue")
probBox.place(x=300, y=41)
probBox.configure(text='0')

# button
button = ck.CTkButton(window, text='RESET', command=reset_counter, height=40, width=120, text_font=("Arial", 20),
                      text_color="white", fg_color="blue")
button.place(x=10, y=600)

# place to video
frame = tk.Frame(height=480, width=480)
frame.place(x=10, y=90)
lmain = tk.Label(frame)
lmain.place(x=0, y=0)

# checkbox
registered_label = tk.Label(window, text="Registration Status")  # lable

reg_status_var = tk.StringVar(value="Not Registered")
registered_check = tk.Checkbutton(window, text="Currently Registered",
                                  variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

registered_label.place(x=800, y=41)  # lable posision
registered_check.place(x=800, y=60)  # checkbox posission

window.mainloop()

print("Hello")
