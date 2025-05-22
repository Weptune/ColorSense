import cv2
import numpy as np
import os

def extract_color_features(frames_folder):
    features = []
    frame_names = sorted(os.listdir(frames_folder))

    for fname in frame_names:
        frame_path = os.path.join(frames_folder, fname)
        img = cv2.imread(frame_path)
        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)  # HSV: [H, S, V]

        features.append(avg_color)

    return np.array(features)
