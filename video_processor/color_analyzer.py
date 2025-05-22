import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def analyze_colors(frames_folder, output_folder="outputs"):
    rgb_means = []
    rgb_timeline = []

    frame_files = sorted(
        [f for f in os.listdir(frames_folder) if f.endswith((".png", ".jpg"))]
    )

    if not frame_files:
        raise FileNotFoundError(f"No image frames found in {frames_folder}")

    for file in frame_files:
        path = os.path.join(frames_folder, file)
        frame = cv2.imread(path)
        if frame is None:
            raise FileNotFoundError(f"Could not read frame: {path}")

        avg_color_per_row = np.mean(frame, axis=0)
        avg_color = np.mean(avg_color_per_row, axis=0)  # BGR
        rgb = avg_color[::-1]  # Convert BGR to RGB
        rgb_means.append(rgb)
        rgb_timeline.append(rgb)

    rgb_means = np.array(rgb_means)
    rgb_timeline = np.array(rgb_timeline)

    # Save plots
    plt.figure(figsize=(10, 4))
    plt.plot(rgb_timeline[:, 0], color='red', label='Red')
    plt.plot(rgb_timeline[:, 1], color='green', label='Green')
    plt.plot(rgb_timeline[:, 2], color='blue', label='Blue')
    plt.title("Average RGB per Frame")
    plt.xlabel("Frame Index")
    plt.ylabel("Intensity")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, "color_analysis_plot.png"))
    plt.close()

    # Save data for emotion prediction
    np.save(os.path.join(output_folder, "rgb_means.npy"), np.mean(rgb_means, axis=0))
    np.save(os.path.join(output_folder, "rgb_timeline.npy"), rgb_timeline)

    print("🎨 Color analysis completed.")
