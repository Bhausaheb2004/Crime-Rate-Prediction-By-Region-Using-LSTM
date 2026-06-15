import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Import the database module connection functions from your project files
from db import get_db_connection

# ---------------- CONFIGURATIONS & FILE PATHS ---------------- #
DATA_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/data/crime_data_india.csv"
BG_IMAGE = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/crime rate pred.jpg"

# ---------------- LOG TO CRIME WISE PREDICTION DATABASE TABLE ---------------- #
def save_crime_wise_prediction(state, crime_type, year, predicted_value):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the crime_wise_prediction table automatically if it does not exist yet
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crime_wise_prediction (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            state VARCHAR(100),
            crime_type VARCHAR(100),
            year INT,
            predicted_cases INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Attempt to load an active user login session ID identifier variable
    try:
        with open("session.txt", "r") as f:
            user_id = int(f.read())
    except:
        user_id = None

    # Insert metrics records data column array rows
    cursor.execute(
        """INSERT INTO crime_wise_prediction 
           (user_id, state, crime_type, year, predicted_cases) 
           VALUES (%s, %s, %s, %s, %s)""",
        (user_id, state, crime_type, int(year), int(predicted_value))
    )

    conn.commit()
    conn.close()

# ---------------- CORE APPLICATION FRAMEWORK ---------------- #
class CrimeWisePredictionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Crime Wise Prediction Dashboard")
        self.root.geometry("1400x800")

        # Background Configuration Setup
        try:
            img = Image.open(BG_IMAGE)
            img = img.resize((1600, 900))
            self.bg = ImageTk.PhotoImage(img)

            bg_label = tk.Label(root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except:
            root.configure(bg="#1e1e2f")

        # Title Header Text Element
        tk.Label(
            root,
            text="Crime Wise Prediction Dashboard",
            font=("Arial", 22, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=10)

        # Load Dataset File Structure
        try:
            self.df = pd.read_csv(DATA_PATH)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            root.destroy()
            return

        self.states = sorted(self.df["STATE/UT"].dropna().unique())

        # Top Grid Filter Controls Frame Row Block
        top_frame = tk.Frame(root, bg="#2c2c3e")
        top_frame.pack(fill="x", pady=10)

        tk.Label(
            top_frame,
            text="Select State:",
            bg="#2c2c3e",
            fg="white"
        ).pack(side="left", padx=10)

        self.state_combo = ttk.Combobox(
            top_frame,
            values=self.states,
            width=25,
            state="readonly"
        )
        self.state_combo.pack(side="left", padx=10)

        tk.Label(
            top_frame,
            text="Crime Type:",
            bg="#2c2c3e",
            fg="white"
        ).pack(side="left", padx=10)

        self.crime_combo = ttk.Combobox(
            top_frame,
            values=[
                "MURDER",
                "RAPE",
                "KIDNAPPING & ABDUCTION",
                "ROBBERY",
                "BURGLARY",
                "THEFT",
                "RIOTS",
                "CHEATING",
                "ARSON"
            ],
            width=25,
            state="readonly"
        )
        self.crime_combo.pack(side="left", padx=10)

        # Action Buttons Layer
        tk.Button(
            top_frame,
            text="Predict",
            bg="#4CAF50",
            fg="white",
            command=self.predict_crime
        ).pack(side="left", padx=10)

        tk.Button(
            top_frame,
            text="Exit",
            bg="red",
            fg="white",
            command=root.destroy
        ).pack(side="left", padx=10)

        # Text Report Index Markdown Output Workspace Element
        self.output = tk.Text(
            root,
            height=12,
            width=120,
            font=("Consolas", 11)
        )
        self.output.pack(pady=10, padx=10)

        # Embedded Graphic Plot Frame Canvas Layer Container
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

    # ---------------- RUN TIME SERIES PREDICTION ENGINE ---------------- #
    def predict_crime(self):
        state = self.state_combo.get()
        crime = self.crime_combo.get()

        if not state:
            messagebox.showerror("Error", "Please Select State")
            return

        if not crime:
            messagebox.showerror("Error", "Please Select Crime Type")
            return

        data = self.df[self.df["STATE/UT"] == state].sort_values("YEAR")

        if crime not in data.columns:
            messagebox.showerror("Error", f"{crime} column not found in dataset")
            return

        # Prepare linear dataset inputs
        X = np.array(data["YEAR"]).reshape(-1, 1)
        y = np.array(data[crime])

        # Execute Regression modeling math fitting array sequence logic variables
        model = LinearRegression()
        model.fit(X, y)

        last_year = int(data["YEAR"].max())
        future_years = np.array([
            last_year + 1,
            last_year + 2,
            last_year + 3,
            last_year + 4,
            last_year + 5
        ]).reshape(-1, 1)

        future_values = model.predict(future_years)

        # Parse outputs calculations parameters display interface logs configuration
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"State : {state}\n")
        self.output.insert(tk.END, f"Crime Type : {crime}\n\n")
        self.output.insert(tk.END, "Historical Data\n")
        self.output.insert(tk.END, "-" * 50 + "\n")

        for year, value in zip(data["YEAR"], data[crime]):
            self.output.insert(tk.END, f"{year} : {int(value)} Cases\n")

        self.output.insert(tk.END, "\nFuture Prediction\n")
        self.output.insert(tk.END, "-" * 50 + "\n")

        # Save elements tracking loop array variables context
        for year, value in zip(future_years.flatten(), future_values):
            predicted_cases = max(0, int(value))  # Ensure logic bounds metrics don't drop negative numbers
            self.output.insert(tk.END, f"{year} : {predicted_cases} Cases\n")
            
            # Database log transaction injection query execution
            try:
                save_crime_wise_prediction(state, crime, year, predicted_cases)
            except Exception as e:
                print(f"Database sync connection logs failed: {e}")

        # Re-render embedded graphical canvas plots layout data
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(data["YEAR"], data[crime], marker="o", linewidth=2, label="Historical Data")
        ax.plot(future_years.flatten(), future_values, marker="o", linestyle="--", linewidth=2, label="Future Prediction")

        ax.set_title(f"{crime} Prediction - {state}", fontsize=18)
        ax.set_xlabel("Year")
        ax.set_ylabel("Cases")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrimeWisePredictionApp(root)
    root.mainloop()