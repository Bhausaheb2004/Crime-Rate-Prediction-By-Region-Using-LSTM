# home.py

import tkinter as tk
from PIL import Image, ImageTk
import sys
import subprocess

root = tk.Tk()
root.title("Crime Rate Prediction System")
root.configure(background="white")

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# Background
try:
    image2 = Image.open("D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/home page img.jpg")
    image2 = image2.resize((w, h))
    bg = ImageTk.PhotoImage(image2)

    label = tk.Label(root, image=bg)
    label.image = bg
    label.place(x=0, y=0)
except:
    root.configure(bg="#E6F2FF")

# Title
tk.Label(root,
         text="Crime Rate Prediction by Region using LSTM",
         font=('Times New Roman', 40, 'bold'),
         bg="#013220",
         fg="white").pack(pady=50)

# Description
tk.Label(root,
         text="Analyze crime data and predict future trends",
         font=('Times New Roman', 20),
         bg="#013220",
         fg="white").pack(pady=20)

# Open Login
def open_login():
    root.destroy()
    subprocess.call([sys.executable, "login.py"])

# Button
tk.Button(root,
          text="Start Prediction",
          command=open_login,
          font=('times', 20, 'bold'),
          bg="blue", fg="white").pack(pady=100)

tk.Button(root,
          text="Exit",
          command=root.destroy,
          bg="red", fg="white").pack()

root.mainloop()