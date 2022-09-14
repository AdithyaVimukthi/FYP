import tkinter as tk
import customtkinter as ck

import pandas as pd
import numpy as np
import pickle

import mediapipe as mp
import cv2
from PIL import Image, ImageTk


def start():
    pass


def end():
    pass


def pause():
    pass


window = tk.Tk()
window.geometry("960x540")
window.title("Human Hand Tracking System")
ck.set_appearance_mode("dark")

#lables
tilable = ck.CTkLabel(window, height=40, width=320, text_font=("Calibre", 20), text_color="white", padx=10, fg_color="blue")
tilable.place(x=280, y=10)
tilable.configure(text='Human Motion Recognition System')

'''
classLabel = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="black", padx=10)
classLabel.place(x=10, y=1)
classLabel.configure(text='STAGE')

classBox = ck.CTkLabel(window, height=40, width=120, text_font=("Arial", 20), text_color="white", fg_color="blue")
classBox.place(x=10, y=41)
classBox.configure(text='0')
'''

# buttons
button_st = ck.CTkButton(window, text='Start', command=start, height=30, width=60, text_font=("Arial", 10),
                      text_color="white", fg_color="blue")
button_st.place(x=740, y=240)

button_stp = ck.CTkButton(window, text='End', command=end, height=30, width=60, text_font=("Arial", 10),
                      text_color="white", fg_color="blue")
button_stp.place(x=810, y=240)

button_pus = ck.CTkButton(window, text='Pause', command=pause, height=30, width=60, text_font=("Arial", 10),
                      text_color="white", fg_color="blue")
button_pus.place(x=880, y=240)

# place for videos
frame1 = tk.Frame(height=480, width=660)
frame1.place(x=20, y=60)
lmain1 = tk.Label(frame1)
lmain1.place(x=0, y=0)

arm_cam = ck.CTkLabel(window, height=30, width=220, text_font=("Calibre", 10), text_color="white", padx=5, fg_color="red")
arm_cam.place(x=240, y=65)
arm_cam.configure(text='Video Feed From Arm Side')

frame2 = tk.Frame(height=240, width=240)
frame2.place(x=700, y=280)
lmain2 = tk.Label(frame2)
lmain2.place(x=0, y=0)

# checkbox
skeleton_var = tk.StringVar(value="sk_off")
skeleton_check = tk.Checkbutton(window, text="Skeleton View", variable=skeleton_var, onvalue="sk_on", offvalue="sk_off")
skeleton_check.place(x=740, y=200)  # checkbox posission

blackBG_var = tk.StringVar(value="bbg_off")
blackBG_check = tk.Checkbutton(window, text="Black Background", variable=blackBG_var, onvalue="bbg_on", offvalue="bbg_off")
blackBG_check.place(x=740, y=180)

cap = cv2.VideoCapture(0)


def detect():
    ret, frame = cap.read()

    image1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image1 = cv2.resize(image1, (660,470))

    img1 = image1[:, :650, :]
    imgarr1 = Image.fromarray(img1)
    imgtk1 = ImageTk.PhotoImage(imgarr1)
    lmain1.imgtk = imgtk1
    lmain1.configure(image=imgtk1)
    lmain1.after(10, detect)


detect()
window.mainloop()


print("Hello")
