import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

def extract_frames(video_path, output_folder, frame_rate=1):
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return

    os.makedirs(output_folder, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps // frame_rate)

    count = 0
    saved = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            filename = os.path.join(output_folder, f"frame_{saved:04d}.jpg")
            cv2.imwrite(filename, frame)
            saved += 1
        count += 1

    cap.release()
    print(f"✅ Extracted {saved} frames to {output_folder}")

def analyze_video_colors(video_path):
    if not os.path.exists(video_path):
        print(f"❌ Video not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Unable to open video: {video_path}")
        return

    os.makedirs("outputs", exist_ok=True)
    all_means = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mean_colors = np.mean(rgb, axis=(0, 1))  # Mean R, G, B
        all_means.append(mean_colors)
        frame_count += 1

    cap.release()

    all_means = np.array(all_means)
    plt.figure(figsize=(10, 5))
    plt.plot(all_means[:, 0], label='Red', color='red')
    plt.plot(all_means[:, 1], label='Green', color='green')
    plt.plot(all_means[:, 2], label='Blue', color='blue')
    plt.legend()
    plt.title('RGB Color Mean per Frame')
    plt.xlabel('Frame')
    plt.ylabel('Color Intensity')
    plt.savefig("outputs/color_analysis_plot.png")
    print("✅ Color analysis completed. Output saved to outputs/color_analysis_plot.png")
