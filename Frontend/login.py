import tkinter as tk
from tkinter import messagebox as ms
import os
import subprocess   
import sys          
from PIL import Image, ImageTk
from db import init_db, get_db_connection


init_db()

root = tk.Tk()
root.title("Login System")
root.geometry("800x500")
root.resizable(False, False)

# ---------------- BACKGROUND IMAGE ---------------- #
try:
    img = Image.open(rf"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/home page img.jpg")
    img = img.resize((800, 500))
    bg = ImageTk.PhotoImage(img)

    bg_label = tk.Label(root, image=bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="#E6F2FF")

# ---------------- VARIABLES ---------------- #
username = tk.StringVar()
password = tk.StringVar()

# ---------------- FUNCTIONS ---------------- #
def login():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM registration WHERE username=%s AND password=%s",
        (username.get(), password.get())
    )

    result = cursor.fetchone()

    if result:
        user_id = result[0]

        # SAVE SESSION
        with open("session.txt", "w") as f:
            f.write(str(user_id))

        # LOGIN HISTORY
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute(
                "INSERT INTO login_history (user_id) VALUES (%s)",
                (user_id,)
            )
            conn.commit()
        except:
            pass

        ms.showinfo("Success", "Login Successful")

        import guipage
        root.destroy()
        subprocess.call([sys.executable, "guipage.py"])
    
        
        
    else:
        ms.showerror("Error", "Invalid Username or Password")

    conn.close()


def register():
    # 🔥 HIDE LOGIN WINDOW
    root.withdraw()

    # 🔥 OPEN REGISTER WINDOW
    import registration
    new_window = tk.Toplevel(root)

    try:
        registration.main(new_window)
    except:
        pass


# ---------------- LOGIN CARD ---------------- #
frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=350)

# Title
tk.Label(frame,
         text="Login",
         font=("Arial", 22, "bold"),
         bg="white",
         fg="#333").pack(pady=20)

# Username
tk.Label(frame, text="Username", bg="white").pack(pady=5)
tk.Entry(frame, textvariable=username, width=25).pack(pady=5)

# Password
tk.Label(frame, text="Password", bg="white").pack(pady=5)
tk.Entry(frame, textvariable=password, show="*", width=25).pack(pady=5)

# Login Button
tk.Button(frame,
          text="Login",
          command=login,
          bg="#007BFF",
          fg="white",
          width=15,
          height=1).pack(pady=15)

# Register Button
tk.Button(frame,
          text="Register",
          command=register,
          bg="#28A745",
          fg="white",
          width=15,
          height=1).pack()

# Footer
tk.Label(root,
         text="Crime Prediction System",
         bg="black",
         fg="white").pack(side="bottom", fill="x")

root.mainloop()