import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def extract_frames(video_path, output_dir="outputs/frames", num_frames=20):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, frame_count // num_frames)

    frames = []
    count = 0
    saved = 0
    while cap.isOpened() and saved < num_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
            cv2.imwrite(f"{output_dir}/frame_{saved:03d}.jpg", frame)
            saved += 1
        count += 1
    cap.release()
    return frames

def analyze_colors(frames, output_path="outputs/rgb_timeline.png"):
    rgb_means = [np.mean(frame.reshape(-1, 3), axis=0) for frame in frames]
    rgb_array = np.array(rgb_means)

    plt.figure(figsize=(10, 4))
    plt.plot(rgb_array[:, 0], label="Red", color='r')
    plt.plot(rgb_array[:, 1], label="Green", color='g')
    plt.plot(rgb_array[:, 2], label="Blue", color='b')
    plt.title("RGB Timeline")
    plt.xlabel("Frame Index")
    plt.ylabel("Mean RGB Value")
    plt.legend()
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    return rgb_array

def plot_rgb_timeline(rgb_array, title="RGB Timeline", output_path="outputs/rgb_timeline_plot.png"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(rgb_array[:, 0], label="Red", color='r')
    plt.plot(rgb_array[:, 1], label="Green", color='g')
    plt.plot(rgb_array[:, 2], label="Blue", color='b')
    plt.title(title)
    plt.xlabel("Frame Index")
    plt.ylabel("Mean RGB Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
