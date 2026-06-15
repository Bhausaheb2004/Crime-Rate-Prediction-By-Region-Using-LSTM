import tkinter as tk
from tkinter import messagebox as ms
import subprocess, sys, os, re
from PIL import Image, ImageTk
from db import init_db, get_db_connection

init_db()

# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("Register")
root.geometry("900x600")
root.resizable(False, False)

# ---------------- BACKGROUND IMAGE ---------------- #
try:
    img = Image.open(rf"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/registration img.jpeg")
    img = img.resize((900, 600))
    bg = ImageTk.PhotoImage(img)
    bg_label = tk.Label(root, image=bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="#F0F2F5")

# ---------------- SMART PLACEHOLDER FUNCTION ---------------- #
def placeholder(entry, text, is_password=False):
    entry.insert(0, text)
    entry.config(fg="gray")

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")
            if is_password:
                entry.config(show="*") # Start masking when typing

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="gray", show="") # Show text when empty

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------------- VARIABLES ---------------- #
fullname = tk.StringVar()
username = tk.StringVar()
email = tk.StringVar()
phone = tk.StringVar()
password = tk.StringVar()
confirm = tk.StringVar()
gender = tk.StringVar(value="Male") # Default selected

# ---------------- REGISTER FUNCTION ---------------- #
def register_user():
    full = fullname_entry.get().strip()
    user = username_entry.get().strip()
    mail = email_entry.get().strip()
    ph = phone_entry.get().strip()
    pwd = pass_entry.get().strip()
    conf = confirm_entry.get().strip()
    gen = gender.get()

    # Validation
    if full in ["", "Full Name"] or user in ["", "Username"] or \
       mail in ["", "Email"] or ph in ["", "Phone Number"] or \
       pwd in ["", "Password"] or conf in ["", "Confirm Password"]:
        ms.showerror("Error", "All fields are required")
        return
    
    if pwd != conf:
        ms.showerror("Error", "Passwords mismatch")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO registration (fullname, username, email, phone, gender, password) VALUES (%s,%s,%s,%s,%s,%s)",
                       (full, user, mail, ph, gen, pwd))
        conn.commit()
        ms.showinfo("Success", "Registered Successfully")
        root.destroy()
        subprocess.Popen([sys.executable, "login.py"])
    except Exception as e:
        ms.showerror("Error", str(e))
    finally:
        if 'conn' in locals(): conn.close()

# ---------------- UI ---------------- #
card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=450)

tk.Label(card, text="Create Account", font=("Segoe UI", 22, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=15)

entry_style = {"font": ("Segoe UI", 11), "bd": 2, "relief": "groove", "width": 25}

# Rows
fullname_entry = tk.Entry(card, textvariable=fullname, **entry_style); fullname_entry.grid(row=1, column=0, padx=20, pady=5); placeholder(fullname_entry, "Full Name")
username_entry = tk.Entry(card, textvariable=username, **entry_style); username_entry.grid(row=1, column=1, padx=20, pady=5); placeholder(username_entry, "Username")
email_entry = tk.Entry(card, textvariable=email, **entry_style); email_entry.grid(row=3, column=0, padx=20, pady=5); placeholder(email_entry, "Email")
phone_entry = tk.Entry(card, textvariable=phone, **entry_style); phone_entry.grid(row=3, column=1, padx=20, pady=5); placeholder(phone_entry, "Phone Number")

# Password Rows (Modified to support smart placeholders)
pass_entry = tk.Entry(card, textvariable=password, **entry_style); pass_entry.grid(row=5, column=0, padx=20, pady=5); placeholder(pass_entry, "Password", True)
confirm_entry = tk.Entry(card, textvariable=confirm, **entry_style); confirm_entry.grid(row=5, column=1, padx=20, pady=5); placeholder(confirm_entry, "Confirm Password", True)

# Gender
gender_frame = tk.Frame(card, bg="white")
gender_frame.grid(row=7, column=0, columnspan=2, pady=10)
tk.Label(gender_frame, text="Gender:", bg="white").pack(side="left", padx=5)
tk.Radiobutton(gender_frame, text="Male", variable=gender, value="Male", bg="white").pack(side="left", padx=5)
tk.Radiobutton(gender_frame, text="Female", variable=gender, value="Female", bg="white").pack(side="left", padx=5)

# Button
tk.Button(card, text="Register", command=register_user, bg="#4CAF50", fg="white", font=("Segoe UI", 11, "bold"), width=20).grid(row=8, column=0, columnspan=2, pady=20)

root.mainloop()