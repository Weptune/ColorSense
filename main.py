import os
import cv2
import numpy as np
from color_analysis import analyze_colors, extract_frames, plot_rgb_timeline
from color_grading import apply_emotion_tint
from emotion_detector.model import predict_emotion_from_rgb

def calculate_average_rgb(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    rgbs = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mean_rgb = rgb_frame.mean(axis=(0, 1))
        rgbs.append(mean_rgb)
    cap.release()
    if rgbs:
        avg_rgb = np.mean(rgbs, axis=0)
        return tuple(map(int, avg_rgb))
    return None

def run_full_pipeline(video_path, num_frames=20, emotion=None, intensity='medium', log_callback=print):
    os.makedirs("outputs", exist_ok=True)

    log_callback("Extracting frames from original video...")
    frames = extract_frames(video_path, num_frames=num_frames)

    log_callback("Analyzing original video colors...")
    original_rgb = analyze_colors(frames)
    original_rgb_plot = plot_rgb_timeline(original_rgb, title="Original RGB Timeline", output_path="outputs/original_rgb_timeline.png")

    if not emotion:
        log_callback("Predicting emotion from video colors...")
        predicted_emotion = predict_emotion_from_rgb(original_rgb, original_rgb)
    else:
        predicted_emotion = emotion
    log_callback(f"Using emotion: {predicted_emotion}")

    output_video_path = f"outputs/graded_video_{predicted_emotion}_{intensity}.mp4"
    log_callback(f"Applying {intensity} grading for emotion '{predicted_emotion}'...")
    apply_emotion_tint(video_path, predicted_emotion, intensity=intensity, output_path=output_video_path)

    log_callback("Extracting frames from graded video...")
    graded_frames = extract_frames(output_video_path, num_frames=num_frames)

    log_callback("Analyzing graded video colors...")
    graded_rgb = analyze_colors(graded_frames)
    graded_rgb_plot = plot_rgb_timeline(graded_rgb, title="Graded RGB Timeline", output_path="outputs/graded_rgb_timeline.png")

    log_callback("Calculating average RGB for original video...")
    orig_avg_rgb = calculate_average_rgb(video_path)
    log_callback(f"Original video avg RGB: {orig_avg_rgb}")

    log_callback("Calculating average RGB for graded video...")
    graded_avg_rgb = calculate_average_rgb(output_video_path)
    log_callback(f"Graded video avg RGB: {graded_avg_rgb}")

    return {
        "predicted_emotion": predicted_emotion,
        "output_video": output_video_path,
        "original_rgb_plot": original_rgb_plot,
        "graded_rgb_plot": graded_rgb_plot,
        "original_rgb_avg": orig_avg_rgb,
        "graded_rgb_avg": graded_avg_rgb
    }
