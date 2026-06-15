import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

# Import the database connection utility from your project files
from db import get_db_connection

# Fallback configurations if main script doesn't pass them
DEFAULT_DATA_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/data/crime_data_india.csv"
BG_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/crime rate pred.jpg"

# ---------------- LOG METRICS TO SAFETY ASSESSMENT TABLE ---------------- #
def save_safety_record(state, safety_score, classification, historical_mean, recent_avg):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Automatically construct the safety data logger table structure if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS safety_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            state VARCHAR(100),
            safety_score INT,
            classification VARCHAR(100),
            historical_mean INT,
            recent_avg INT,
            calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Attempt to pull active user metadata session constraints if available
    try:
        with open("session.txt", "r") as f:
            user_id = int(f.read())
    except:
        user_id = None

    # Inject calculations parameters row inside the database layer
    cursor.execute(
        """INSERT INTO safety_records 
           (user_id, state, safety_score, classification, historical_mean, recent_avg) 
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (user_id, state, int(safety_score), classification, int(historical_mean), int(recent_avg))
    )

    conn.commit()
    conn.close()


class SafetyAssessmentApp:
    # Accept the exact arguments your main dashboard is sending
    def __init__(self, root, initial_state=None, df_data=None, data_path=None):
        self.root = root
        self.root.title("Safety Index Assessment Module")
        self.root.geometry("1050x650")

        # Background Canvas Setup (Exact UI Matching)
        try:
            img = Image.open(BG_PATH)
            img = img.resize((1500, 1200))
            self.bg = ImageTk.PhotoImage(img)

            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except Exception:
            self.root.configure(bg="#1e1e2f")

        # Page Header Text Element
        tk.Label(
            root,
            text="Safety Index & 5-Year Projections",
            font=("Arial", 20, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=10)

        # Use passed DataFrame or load fallback
        if df_data is not None:
            self.df = df_data
        else:
            try:
                path_to_use = data_path if data_path else DEFAULT_DATA_PATH
                self.df = pd.read_csv(path_to_use)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV data within Safety sub-module:\n{str(e)}")
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

        # Dropdown Combobox Setup
        self.state_combo = ttk.Combobox(
            top_frame,
            values=self.states,
            state="readonly",
            width=25
        )
        self.state_combo.pack(side="left", padx=10)

        # BUTTON 1: RUN EVALUATION (Purple Styling Element)
        tk.Button(
            top_frame,
            text="Safety",
            bg="#9C27B0",
            fg="white",
            command=self.run_evaluation,
            width=12,
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=10)

        # BUTTON 2: DISMISS WINDOW (Red Styling Element)
        tk.Button(
            top_frame,
            text="Exit",
            bg="red",
            fg="white",
            command=root.destroy,
            width=10
        ).pack(side="left", padx=10)

        # Data Stream Text Container Box
        self.output_box = tk.Text(root, height=10, width=110)
        self.output_box.pack(pady=10)

        # Embedded Graphic Plot Frame Layer
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

        # If an initial state was passed from the main window, set it and evaluate immediately
        if initial_state and initial_state in self.states:
            self.state_combo.set(initial_state)
            self.run_evaluation()

    def run_evaluation(self):
        state = self.state_combo.get()
        
        if not state:
            messagebox.showerror("Error", "Select a state")
            return

        data = self.df[self.df["STATE/UT"] == state].sort_values("YEAR")
        
        if data.empty:
            messagebox.showwarning("Data Missing", f"No metric logs found for state profile: {state}")
            return

        years = data["YEAR"].tolist()
        total_crimes = data["TOTAL IPC CRIMES"].values
        recent_trend = total_crimes[-3:] if len(total_crimes) >= 3 else total_crimes
        
        mean_volume = np.mean(total_crimes)
        recent_mean = np.mean(recent_trend)
        
        base_score = 100.0
        volume_penalty = min(40, (mean_volume / 10000) * 2.5) 
        
        trend_variance = ((recent_mean - total_crimes[0]) / total_crimes[0]) if total_crimes[0] > 0 else 0
        trend_penalty = max(-15, min(45, trend_variance * 75))
        
        safety_score = max(5, min(100, int(base_score - volume_penalty - trend_penalty)))

        if safety_score >= 75:
            zone_rating = "SAFE ZONE"
            zone_display = "🟢 SAFE ZONE PROFILE (Low Vulnerability Risk Factors)"
            advice = "Maintain current local community enforcement configurations. Region displays low volatility."
            graph_color = "#4CAF50"
        elif safety_score >= 45:
            zone_rating = "MODERATE RISK ZONE"
            zone_display = "🟡 MODERATE RISK ZONE (Requires Increased Preventive Patrols)"
            advice = "Tactical resource deployment suggested. Monitor regional specific crimes to prevent upward shifts."
            graph_color = "#FF9800"
        else:
            zone_rating = "CRITICAL WATCH ZONE"
            zone_display = "🔴 CRITICAL WATCH ALERT (High Volatility Core Hotspot)"
            advice = "Immediate task force intervention recommended. High variance spikes found in local crime history metrics."
            graph_color = "red"

        # Next 5-Year Forecaster Projections Vector System
        last_year = years[-1]
        last_value = total_crimes[-1]

        future_years = []
        future_values = []
        for i in range(1, 6):
            future_years.append(last_year + i)
            future_values.append(int(last_value + (i * 1000)))

        # Update Log Stream Outputs
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"\n🛡️ Safety Assessment Intelligence Report: {state}\n")
        self.output_box.insert(tk.END, "-" * 65 + "\n")
        self.output_box.insert(tk.END, f"Calculated Safety Index Score : {safety_score} / 100\n")
        self.output_box.insert(tk.END, f"Classification Tier           : {zone_display}\n")
        self.output_box.insert(tk.END, f"Historical Mean baseline     : {int(mean_volume)} Registered Case Records\n")
        self.output_box.insert(tk.END, f"Recent 3-Year Rolling Average: {int(recent_mean)} Cases\n")
        self.output_box.insert(tk.END, f"💡 Strategic Advice          : {advice}\n")
        
        self.output_box.insert(tk.END, "\n🔮 Next 5 Years Prediction\n")
        self.output_box.insert(tk.END, "-" * 65 + "\n")
        for y, v in zip(future_years, future_values):
            self.output_box.insert(tk.END, f"{y} - {v} crimes\n")

        # Database transaction sync process
        try:
            save_safety_record(state, safety_score, zone_rating, mean_volume, recent_mean)
        except Exception as e:
            print(f"Safety records database sync logs failed: {e}")

        # Dynamic Graphic Node Refresh Sequence
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Trend Baselines Drawing Node Execution
        ax.plot(years, total_crimes, marker='o', color=graph_color, linewidth=2, label="Past Data")
        ax.plot(future_years, future_values, marker='o', linestyle='--', color="#2196F3", linewidth=2, label="Future Prediction")
        
        ax.set_title(f"Crime Trend - {state}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Crimes")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = SafetyAssessmentApp(root)
    root.mainloop()