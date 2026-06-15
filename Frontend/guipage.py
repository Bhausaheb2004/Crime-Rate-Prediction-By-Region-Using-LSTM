import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from db import get_db_connection
from db import init_db
import importlib  # Required to cleanly import filenames with spaces

# Initialize database tables on load
init_db()

# ---------------- CONFIGURATIONS & SYSTEM PATHS ---------------- #
DATA_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/data/crime_data_india.csv"
BG_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/crime rate pred.jpg"

# ---------------- LOG METRICS TO REGIONAL DATA MATRIX ---------------- #
def save_prediction(state, year, value):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        with open("session.txt", "r") as f:
            user_id = int(f.read())
    except:
        user_id = None

    cursor.execute(
        "INSERT INTO predictions (user_id, state, year, predicted_crime) VALUES (%s,%s,%s,%s)",
        (user_id, state, year, int(value))
    )

    conn.commit()
    conn.close()

# ---------------- CORE APPLICATION FRAMEWORK ---------------- #
class CrimePredictionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Crime Prediction Dashboard")
        self.root.geometry("1150x650") 

        # Background Canvas Setup
        try:
            img = Image.open(BG_PATH)
            img = img.resize((1500, 1200))
            self.bg = ImageTk.PhotoImage(img)

            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except:
            self.root.configure(bg="#1e1e2f")

        # Page Header Elements
        tk.Label(
            root,
            text="Crime Rate Prediction Dashboard",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=10)

        # Load Dataset File Structure
        try:
            self.df = pd.read_csv(DATA_PATH)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV data:\n{str(e)}")
            root.destroy()
            return

        self.states = sorted(self.df["STATE/UT"].dropna().unique())

        # Top Control Frame Grid Layer
        top_frame = tk.Frame(root, bg="#2c2c3e")
        top_frame.pack(fill="x", pady=10)

        tk.Label(
            top_frame,
            text="Select State:",
            bg="#2c2c3e",
            fg="white"
        ).pack(side="left", padx=10)

        self.combo = ttk.Combobox(
            top_frame,
            values=self.states,
            state="readonly",
            width=25
        )
        self.combo.pack(side="left", padx=10)

        # Predict Button Element
        tk.Button(
            top_frame,
            text="Predict",
            bg="#4CAF50",
            fg="white",
            command=self.run_prediction,
            width=10
        ).pack(side="left", padx=10)

        # Safety Score Button Element
        tk.Button(
            top_frame,
            text="Safety Score",
            bg="#9C27B0",
            fg="white",
            command=self.calculate_safety_index,
            width=12,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=10)

        # Crime Wise Prediction Button Element
        tk.Button(
            top_frame,
            text="Crime Wise Prediction",
            bg="#2196F3",
            fg="white",
            command=self.crime_wise_prediction
        ).pack(side="left", padx=10)

        # State Wise Compare Button Element
        tk.Button(
            top_frame,
            text="State Wise Compare",
            bg="#FF9800",
            fg="black",
            command=self.open_state_comparison,
            width=18,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=10)

        # Exit Button Element
        tk.Button(
            top_frame,
            text="Exit",
            bg="red",
            fg="white",
            command=root.destroy,
            width=10
        ).pack(side="left", padx=10)

        # Output Text Area Element
        self.output = tk.Text(root, height=10, width=110)
        self.output.pack(pady=10)

        # Embedded Graphic Plot Frame Layer
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

    # ---------------- REGIONAL TIME SERIES PREDICTION ENGINE ---------------- #
    def run_prediction(self):
        state = self.combo.get()

        if not state:
            messagebox.showerror("Error", "Select a state")
            return

        data = self.df[self.df["STATE/UT"] == state].sort_values("YEAR")

        if data.empty:
            messagebox.showwarning("Data Missing", f"No records found for state: {state}")
            return

        years = data["YEAR"].tolist()
        values = data["TOTAL IPC CRIMES"].values

        last_year = years[-1]
        last_value = values[-1]

        future_years = []
        future_values = []

        for i in range(1, 6):
            year = last_year + i
            value = int(last_value + (i * 1000))

            future_years.append(year)
            future_values.append(value)

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"\n📊 {state} Data\n")
        self.output.insert(tk.END, "-" * 40 + "\n")

        for y, v in zip(years, values):
            self.output.insert(tk.END, f"{y} - {int(v)} crimes\n")

        self.output.insert(tk.END, "\n🔮 Next 5 Years Prediction\n")
        self.output.insert(tk.END, "-" * 40 + "\n")

        for y, v in zip(future_years, future_values):
            self.output.insert(tk.END, f"{y} - {v} crimes\n")
            try:
                save_prediction(state, y, v)
            except Exception as e:
                print(f"Database insertion failed: {e}")

        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(years, values, marker='o', label="Past Data")
        ax.plot(future_years, future_values, marker='o', linestyle='--', label="Future Prediction")

        ax.set_title(f"Crime Trend - {state}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Crimes")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------- AUTOMATICALLY OPEN Safety.py FOR CHANGED STATE ---------------- #
    def calculate_safety_index(self):
        state = self.combo.get()

        if not state:
            messagebox.showerror("Error", "Please select a state to calculate its safety index status.")
            return

        try:
            from Safety import SafetyAssessmentApp
            safety_window = tk.Toplevel(self.root)
            
            app = SafetyAssessmentApp(safety_window)
            
            if hasattr(app, 'combo') and state:
                app.combo.set(state)
            elif hasattr(app, 'state_combo') and state:
                app.state_combo.set(state)
            
        except ImportError:
            messagebox.showerror("Error", "Could not locate 'Safety.py' script inside your project folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute Safety file window pipeline:\n{str(e)}")

    # ---------------- CRIME WISE PREDICTION CONNECTOR ---------------- #
    def crime_wise_prediction(self):
        state = self.combo.get()

        if not state:
            messagebox.showerror("Error", "Please select a state first")
            return

        try:
            from crime_wise_prediction import CrimeWisePredictionApp
            crime_window = tk.Toplevel(self.root)
            app = CrimeWisePredictionApp(crime_window)
            
            if hasattr(app, 'state_combo'):
                app.state_combo.set(state)
            
        except ImportError:
            messagebox.showerror("Error", "Could not find file 'crime_wise_prediction.py' in the same folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open module:\n{str(e)}")

    # ---------------- STATE WISE COMPARISON CONNECTOR (SPACES FIXED) ---------------- #
    def open_state_comparison(self):
        state = self.combo.get()

        try:
            # Uses importlib to safely parse modules named with spaces
            module = importlib.import_module("State wise compare")
            DualStateComparisonApp = getattr(module, "DualStateComparisonApp")
            
            comp_window = tk.Toplevel(self.root)
            app = DualStateComparisonApp(comp_window)
            
            if state and hasattr(app, 'combo_a'):
                app.combo_a.set(state)
                app.execute_comparison()
                
        except ModuleNotFoundError:
            messagebox.showerror("Error", "Could not locate 'State wise compare.py' inside your project root folder.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open comparison window module:\n{str(e)}")

# ---------------- MAIN INITIALIZER BLOCK ---------------- #
def main(root):
    app = CrimePredictionApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()