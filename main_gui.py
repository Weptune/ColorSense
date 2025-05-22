import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from main import run_full_pipeline
import threading
import os
import cv2

class ColorSenseApp:
    def __init__(self, root):
        self.root = root
        root.title("ColorSense - Video Emotion Color Grading")
        root.geometry("1000x700")
        root.minsize(900, 600)

        # Main frames layout
        top_frame = ttk.Frame(root)
        top_frame.pack(side='top', fill='x', padx=10, pady=10)

        # Video selection and controls
        ttk.Label(top_frame, text="Select video file:", font=("Segoe UI", 11)).pack(side='left')
        self.video_path = tk.StringVar()
        self.entry_path = ttk.Entry(top_frame, textvariable=self.video_path, width=50, state='readonly')
        self.entry_path.pack(side='left', padx=10)
        ttk.Button(top_frame, text="Browse...", command=self.browse_file).pack(side='left')

        ttk.Label(top_frame, text="Emotion to convey (optional):", font=("Segoe UI", 11)).pack(side='left', padx=(20, 5))
        self.user_emotion = ttk.Combobox(top_frame, values=["", "happy", "sad", "angry", "calm", "excited", "romantic"], width=15)
        self.user_emotion.set("")  # Blank = auto-detect
        self.user_emotion.pack(side='left')

        ttk.Label(top_frame, text="Intensity:", font=("Segoe UI", 11)).pack(side='left', padx=(20, 5))
        self.intensity = ttk.Combobox(top_frame, values=["subtle", "medium", "strong"], state='readonly', width=10)
        self.intensity.current(1)
        self.intensity.pack(side='left')

        ttk.Button(top_frame, text="Run Analysis & Grading", command=self.run_analysis_thread).pack(side='left', padx=10)

        # Status label
        self.status_var = tk.StringVar(value="No video loaded.")
        ttk.Label(root, textvariable=self.status_var, font=("Segoe UI", 10, "italic")).pack(fill='x', padx=10)

        # Main content layout
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Left panel - original
        self.orig_panel = ttk.Frame(self.content_frame)
        self.orig_panel.pack(side='left', fill='both', expand=True, padx=5)

        ttk.Label(self.orig_panel, text="Original Video", font=("Segoe UI", 12, "bold")).pack()

        self.orig_video_label = ttk.Label(self.orig_panel)
        self.orig_video_label.pack(pady=5)

        self.orig_graph_label = ttk.Label(self.orig_panel)
        self.orig_graph_label.pack(pady=(10, 5))

        self.orig_stats_label = ttk.Label(self.orig_panel, justify='left', font=("Segoe UI", 10))
        self.orig_stats_label.pack(pady=5)

        # Right panel - graded
        self.graded_panel = ttk.Frame(self.content_frame)
        self.graded_panel.pack(side='left', fill='both', expand=True, padx=5)

        ttk.Label(self.graded_panel, text="Graded Video", font=("Segoe UI", 12, "bold")).pack()

        self.graded_video_label = ttk.Label(self.graded_panel)
        self.graded_video_label.pack(pady=5)

        self.graded_graph_label = ttk.Label(self.graded_panel)
        self.graded_graph_label.pack(pady=(10, 5))

        self.graded_stats_label = ttk.Label(self.graded_panel, justify='left', font=("Segoe UI", 10))
        self.graded_stats_label.pack(pady=5)

        # Log window
        self.log_text = tk.Text(root, height=8, state='disabled', font=("Consolas", 10))
        self.log_text.pack(fill='both', padx=10, pady=(0,10))

        # Playback variables
        self.orig_video_cap = None
        self.graded_video_cap = None
        self.playing = False

    def browse_file(self):
        filetypes = (("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Select Video File", filetypes=filetypes)
        if filename:
            self.video_path.set(filename)
            self.status_var.set(f"Selected: {filename}")
            self.clear_log()
            self.log("Selected file: " + filename)
            self.clear_video_panels()

    def clear_log(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')

    def log(self, message):
        self.log_text.configure(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.configure(state='disabled')
        self.log_text.see(tk.END)

    def run_analysis_thread(self):
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()

    def run_analysis(self):
        video = self.video_path.get()
        if not video:
            messagebox.showerror("Error", "Please select a video file first.")
            return

        user_emotion = self.user_emotion.get().strip() or None
        intensity = self.intensity.get()

        self.clear_log()
        self.log(f"Running on video: {video}")
        self.log(f"Emotion to convey: {user_emotion if user_emotion else 'Auto-detect'}")
        self.log(f"Intensity: {intensity}")
        self.status_var.set("Processing... please wait.")

        try:
            result = run_full_pipeline(
                video_path=video,
                emotion=user_emotion,
                intensity=intensity,
                log_callback=self.log
            )
            self.status_var.set(f"Done! Predicted emotion: {result['predicted_emotion']}")

            # Display graphs
            self.load_graphs(result["original_rgb_plot"], result["graded_rgb_plot"])

            # Show average RGB values
            orig_rgb_avg = result.get("original_rgb_avg", "N/A")
            graded_rgb_avg = result.get("graded_rgb_avg", "N/A")

            self.orig_stats_label.config(text=f"Avg RGB: {orig_rgb_avg}")
            self.graded_stats_label.config(text=f"Avg RGB: {graded_rgb_avg}")

            # Play both videos
            self.play_videos(result["output_video"], video)

        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", str(e))
            self.status_var.set("Error occurred.")

    def load_graphs(self, orig_graph_path, graded_graph_path):
        try:
            orig_img = Image.open(orig_graph_path).resize((450, 150))
            orig_imgtk = ImageTk.PhotoImage(orig_img)
            self.orig_graph_label.imgtk = orig_imgtk
            self.orig_graph_label.config(image=imgtk)
        except Exception:
            self.orig_graph_label.config(text="Original graph not available", image='')

        try:
            graded_img = Image.open(graded_graph_path).resize((450, 150))
            graded_imgtk = ImageTk.PhotoImage(graded_img)
            self.graded_graph_label.imgtk = graded_imgtk
            self.graded_graph_label.config(image=graded_imgtk)
        except Exception:
            self.graded_graph_label.config(text="Graded graph not available", image='')

    def clear_video_panels(self):
        self.orig_video_label.config(image='')
        self.graded_video_label.config(image='')
        self.orig_graph_label.config(image='', text='')
        self.graded_graph_label.config(image='', text='')
        self.orig_stats_label.config(text='')
        self.graded_stats_label.config(text='')
        self.status_var.set("No video loaded.")
        if self.orig_video_cap:
            self.orig_video_cap.release()
            self.orig_video_cap = None
        if self.graded_video_cap:
            self.graded_video_cap.release()
            self.graded_video_cap = None
        self.playing = False

    def play_videos(self, graded_path, orig_path):
        if self.orig_video_cap:
            self.orig_video_cap.release()
        if self.graded_video_cap:
            self.graded_video_cap.release()

        self.orig_video_cap = cv2.VideoCapture(orig_path)
        self.graded_video_cap = cv2.VideoCapture(graded_path)

        self.playing = True
        self.show_frames()

    def show_frames(self):
        if not self.playing:
            return

        ret1, frame1 = self.orig_video_cap.read()
        ret2, frame2 = self.graded_video_cap.read()

        if ret1:
            frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(frame1).resize((450, 250))
            imgtk1 = ImageTk.PhotoImage(image=img1)
            self.orig_video_label.imgtk = imgtk1
            self.orig_video_label.config(image=imgtk1)
        else:
            self.orig_video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if ret2:
            frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(frame2).resize((450, 250))
            imgtk2 = ImageTk.PhotoImage(image=img2)
            self.graded_video_label.imgtk = imgtk2
            self.graded_video_label.config(image=imgtk2)
        else:
            self.graded_video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        self.root.after(30, self.show_frames)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorSenseApp(root)
    root.mainloop()
