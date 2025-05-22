# gui_main.py

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class ColorSenseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ColorSense - Emotion-Based Color Grading")
        self.root.geometry("500x300")

        self.video_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="🎬 Select a video file:").pack(pady=10)
        tk.Entry(self.root, textvariable=self.video_path, width=50).pack(pady=5)
        tk.Button(self.root, text="Browse", command=self.browse_file).pack()

        tk.Button(self.root, text="Run Analysis", command=self.run_analysis, bg="#4CAF50", fg="white").pack(pady=20)

        self.status_label = tk.Label(self.root, text="", fg="blue")
        self.status_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video_path.set(file_path)

    def run_analysis(self):
        path = self.video_path.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please select a valid video file.")
            return

        self.status_label.config(text="Processing...")
        try:
            subprocess.run(["python", "run_color_grade.py", path], check=True)
            self.status_label.config(text="✅ Processing complete! Check the outputs folder.")
        except subprocess.CalledProcessError:
            self.status_label.config(text="❌ Failed to process video.")
            messagebox.showerror("Error", "An error occurred while processing.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorSenseApp(root)
    root.mainloop()
