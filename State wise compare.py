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

# ---------------- CONFIGURATIONS & ASSET PATHS ---------------- #
DATA_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/data/crime_data_india.csv"
BG_PATH = r"D:/Crime rate Prediction Project  F/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/crime rate pred.jpg"

# ---------------- LOG METRICS TO STATE WISE COMPARISON TABLE ---------------- #
def save_comparison_record(state_a, state_b, score_a, score_b, mean_a, mean_b, forecast_a_y5, forecast_b_y5):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Automatically construct the state comparison table structure if missing
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS state_wise_comparisons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            state_a VARCHAR(100),
            state_b VARCHAR(100),
            safety_score_a INT,
            safety_score_b INT,
            historical_mean_a INT,
            historical_mean_b INT,
            forecast_5yr_a INT,
            forecast_5yr_b INT,
            compared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        """INSERT INTO state_wise_comparisons 
           (user_id, state_a, state_b, safety_score_a, safety_score_b, 
            historical_mean_a, historical_mean_b, forecast_5yr_a, forecast_5yr_b) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (user_id, state_a, state_b, int(score_a), int(score_b), 
         int(mean_a), int(mean_b), int(forecast_a_y5), int(forecast_b_y5))
    )

    conn.commit()
    conn.close()


class DualStateComparisonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dual-State Comparative Analytics Module")
        self.root.geometry("1100x700")

        # Background Image Layout Setup
        try:
            img = Image.open(BG_PATH)
            img = img.resize((1600, 1200))
            self.bg = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except:
            self.root.configure(bg="#1e1e2f")

        # Module Header Title
        tk.Label(
            root,
            text="Side-by-Side State Safety & Distribution Comparison",
            font=("Arial", 18, "bold"),
            bg="#1e1e2f",
            fg="white"
        ).pack(pady=10)

        # Load Dataset File Structure Matrix
        try:
            self.df = pd.read_csv(DATA_PATH)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV data matrix:\n{str(e)}")
            root.destroy()
            return

        self.states = sorted(self.df["STATE/UT"].dropna().unique())

        # Top Selection Control Bar Block
        top_frame = tk.Frame(root, bg="#2c2c3e")
        top_frame.pack(fill="x", pady=5)

        # State Selection Dropdown Profile A
        tk.Label(top_frame, text="State A Profile:", bg="#2c2c3e", fg="#00E5FF", font=("Arial", 9, "bold")).pack(side="left", padx=(15, 5))
        self.combo_a = ttk.Combobox(top_frame, values=self.states, state="readonly", width=22)
        self.combo_a.pack(side="left", padx=5)
        if len(self.states) > 0: self.combo_a.set(self.states[0])

        # State Selection Dropdown Profile B
        tk.Label(top_frame, text="State B Profile:", bg="#2c2c3e", fg="#FF9800", font=("Arial", 9, "bold")).pack(side="left", padx=(20, 5))
        self.combo_b = ttk.Combobox(top_frame, values=self.states, state="readonly", width=22)
        self.combo_b.pack(side="left", padx=5)
        if len(self.states) > 1: self.combo_b.set(self.states[1])

        # Interactive Trigger Buttons Row
        tk.Button(
            top_frame,
            text="Compare Profiles",
            bg="#9C27B0",
            fg="white",
            command=self.execute_comparison,
            font=("Arial", 9, "bold"),
            width=16
        ).pack(side="left", padx=25, pady=5)

        tk.Button(
            top_frame,
            text="Close Module",
            bg="red",
            fg="white",
            command=root.destroy,
            width=12
        ).pack(side="right", padx=15, pady=5)

        # Metrics Markdown Intelligence Report Workspace Box
        self.output_box = tk.Text(root, height=11, width=125, font=("Courier New", 9))
        self.output_box.pack(pady=10)

        # Embedded Graphic Histogram Display Layer Panel
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True, padx=15, pady=5)

        # Auto-compile comparison analytics using fallback state metrics targets instantly on launch
        self.execute_comparison()

    def get_state_metrics(self, state):
        state_data = self.df[self.df["STATE/UT"] == state].sort_values("YEAR")
        if state_data.empty:
            return None
        
        years = state_data["YEAR"].tolist()
        total_crimes = state_data["TOTAL IPC CRIMES"].values
        recent_trend = total_crimes[-3:] if len(total_crimes) >= 3 else total_crimes
        
        mean_volume = np.mean(total_crimes)
        recent_mean = np.mean(recent_trend)
        
        base_score = 100.0
        volume_penalty = min(40, (mean_volume / 10000) * 2.5) 
        
        trend_variance = ((recent_mean - total_crimes[0]) / total_crimes[0]) if total_crimes[0] > 0 else 0
        trend_penalty = max(-15, min(45, trend_variance * 75))
        
        safety_score = max(5, min(100, int(base_score - volume_penalty - trend_penalty)))
        
        # Extrapolate baseline target projections metrics
        last_value = total_crimes[-1]
        future_values = [int(last_value + (i * 1000)) for i in range(1, 6)]
        
        return {
            "score": safety_score,
            "mean": int(mean_volume),
            "recent_avg": int(recent_mean),
            "history": list(total_crimes),
            "forecast": future_values
        }

    def execute_comparison(self):
        state_a = self.combo_a.get()
        state_b = self.combo_b.get()

        if state_a == state_b:
            messagebox.showerror("Selection Error", "Please select two different states to compare.")
            return

        metrics_a = self.get_state_metrics(state_a)
        metrics_b = self.get_state_metrics(state_b)

        if not metrics_a or not metrics_b:
            messagebox.showwarning("Data Missing", "Could not compile statistical profiles for your selection.")
            return

        # 1. PARSE & STREAM TEXT INDEX REPORT MATRIX DATA 
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f" 🛡️ CRIME METRICS COMPARISON INDEX MATRIX\n")
        self.output_box.insert(tk.END, " =" * 60 + "\n")
        self.output_box.insert(tk.END, f" Evaluation Parameters         | [STATE A] {state_a:<22} | [STATE B] {state_b:<22}\n")
        self.output_box.insert(tk.END, " -" * 60 + "\n")
        self.output_box.insert(tk.END, f" Calculated Safety Index Score | {metrics_a['score']}/100 {' ':<20} | {metrics_b['score']}/100\n")
        self.output_box.insert(tk.END, f" Historical Baseline Case Mean | {metrics_a['mean']:<25,} | {metrics_b['mean']:,}\n")
        self.output_box.insert(tk.END, f" Recent 3-Year Rolling Average | {metrics_a['recent_avg']:<25,} | {metrics_b['recent_avg']:,}\n")
        self.output_box.insert(tk.END, " -" * 60 + "\n")
        self.output_box.insert(tk.END, f" 🔮 5-Year Forecast Projections Baseline Targets:\n")
        self.output_box.insert(tk.END, f"   * Year +1 Horizon Projected | {metrics_a['forecast'][0]:<25,} | {metrics_b['forecast'][0]:,}\n")
        self.output_box.insert(tk.END, f"   * Year +3 Horizon Projected | {metrics_a['forecast'][2]:<25,} | {metrics_b['forecast'][2]:,}\n")
        self.output_box.insert(tk.END, f"   * Year +5 Horizon Projected | {metrics_a['forecast'][4]:<25,} | {metrics_b['forecast'][4]:,}\n")

        # Database Logging execution
        try:
            save_comparison_record(
                state_a, state_b, 
                metrics_a['score'], metrics_b['score'], 
                metrics_a['mean'], metrics_b['mean'], 
                metrics_a['forecast'][4], metrics_b['forecast'][4]
            )
        except Exception as e:
            print(f"Comparison records database sync logs failed: {e}")

        # 2. RENDER MULTI-VARIATE COMPARATIVE PLOT GRAPH DENSITY HISTOGRAM
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 3.5))
        
        # Merge structured ranges tracking pools together
        pool_a = metrics_a['history'] + metrics_a['forecast']
        pool_b = metrics_b['history'] + metrics_b['forecast']

        # Isolate extreme values across both states variables bounds matrices
        min_val = min(min(pool_a), min(pool_b))
        max_val = max(max(pool_a), max(pool_b))
        bins = np.linspace(min_val, max_val, 12)

        # Plot Histograms overlays side-by-side
        ax.hist(pool_a, bins=bins, alpha=0.65, color="#00E5FF", edgecolor="#1e1e2f", rwidth=0.85, label=f"{state_a} Density")
        ax.hist(pool_b, bins=bins, alpha=0.55, color="#FF9800", edgecolor="#1e1e2f", rwidth=0.85, label=f"{state_b} Density")

        ax.set_title(f"Comparative Crime Range Density Distribution Histogram", fontsize=11, fontweight="bold")
        ax.set_xlabel("Crime Volume Scale Thresholds", fontsize=9)
        ax.set_ylabel("Data Sample Frequency", fontsize=9)
        ax.legend()
        ax.grid(True, linestyle=":", alpha=0.5)

        # Mount generated matplotlib graph on canvas engine frame panel
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# Application startup configuration thread engine
if __name__ == "__main__":
    root = tk.Tk()
    app = DualStateComparisonApp(root)
    root.mainloop()