import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def analyze_colors_from_frames(frames_folder, output_path="outputs/color_analysis_plot.png"):
    frame_files = sorted([f for f in os.listdir(frames_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    if not frame_files:
        raise FileNotFoundError(f"No image frames found in folder: {frames_folder}")

    rgb_means = []

    for fname in frame_files:
        frame_path = os.path.join(frames_folder, fname)
        frame = cv2.imread(frame_path)
        if frame is None:
            print(f"Warning: Could not read frame {frame_path}, skipping.")
            continue
        avg_color_per_row = np.mean(frame, axis=0)
        avg_color = np.mean(avg_color_per_row, axis=0)  # BGR
        rgb_means.append(avg_color[::-1])  # Convert BGR to RGB

    rgb_means = np.array(rgb_means)

    plt.figure(figsize=(10, 4))
    plt.plot(rgb_means[:, 0], color='red', label='Red')
    plt.plot(rgb_means[:, 1], color='green', label='Green')
    plt.plot(rgb_means[:, 2], color='blue', label='Blue')
    plt.title("Average RGB per Frame (from extracted frames)")
    plt.xlabel("Frame Index")
    plt.ylabel("Average Color Intensity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    return np.mean(rgb_means, axis=0)
