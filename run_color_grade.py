# run_color_grade.py

import numpy as np
import cv2
import sys
from emotion_detector.model import predict_emotion_from_rgb
from video_processor.frame_extractor import extract_frames
from video_processor.color_analyzer import analyze_colors
from video_processor.rgb_plotter import generate_rgb_timeline
from video_processor.emotion_params import get_adjustment_params

def adjust_colors(frame, emotion, intensity):
    img = frame.astype(np.float32)
    params = get_adjustment_params(emotion, intensity)

    if not params:
        return cv2.convertScaleAbs(img)  # No adjustment

    for c, factor in params['channel_multipliers'].items():
        idx = {'r': 2, 'g': 1, 'b': 0}[c]
        img[..., idx] = np.clip(img[..., idx] * factor, 0, 255)

    img *= params.get('overall_multiplier', 1.0)
    img = np.clip(img, 0, 255)
    return cv2.convertScaleAbs(img)

def process_video(input_path, output_path, emotion, intensity):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        adjusted_frame = adjust_colors(frame, emotion, intensity)
        out.write(adjusted_frame)

    cap.release()
    out.release()
    print(f"✅ Adjusted video saved as {output_path}")

def main():
    # Support command-line argument for GUI input
    input_video = sys.argv[1] if len(sys.argv) > 1 else "test_videos/sample.mp4"
    output_video = "outputs/sample_color_graded.mp4"

    print(f"✅ Extracted 20 frames to outputs/frames")
    extract_frames(input_video, "outputs/frames", frame_rate=1)

    avg_rgb = analyze_colors("outputs/frames", "outputs")
    print("🎨 Color analysis completed.")
    generate_rgb_timeline("outputs/frames", "outputs")

    rgb_means = np.load("outputs/rgb_means.npy")
    rgb_timeline = np.load("outputs/rgb_timeline.npy")
    print("rgb_means shape:", rgb_means.shape)
    print("rgb_timeline shape:", rgb_timeline.shape)
    print("avg_rgb:", avg_rgb)

    predicted_emotion = predict_emotion_from_rgb(rgb_means, rgb_timeline)
    print(f"🎭 Predicted emotion: {predicted_emotion}")

    # Ask user only if running interactively
    if sys.stdin.isatty():
        user_emotion = input("Enter emotion to convey (or press Enter to use predicted): ").strip().lower()
        emotion = user_emotion if user_emotion else predicted_emotion.lower()

        user_intensity = input("Enter intensity (subtle, medium, strong) [default: medium]: ").strip().lower()
        intensity = user_intensity if user_intensity in ["subtle", "medium", "strong"] else "medium"
    else:
        # GUI mode: use predicted and default medium
        emotion = predicted_emotion.lower()
        intensity = "medium"

    print(f"Using emotion: {emotion}, intensity: {intensity}")
    process_video(input_video, output_video, emotion, intensity)

if __name__ == "__main__":
    main()
