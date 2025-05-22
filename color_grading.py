import cv2
import numpy as np
import os

def apply_emotion_tint(input_video, emotion, intensity='medium', output_path="outputs/graded_video.mp4"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file {input_video}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    emotion_colors = {
        "happy": (30, 200, 200),    # BGR
        "sad": (180, 50, 20),
        "angry": (30, 30, 180),
        "calm": (180, 200, 200),
        "neutral": (120, 120, 120)
    }

    tint = emotion_colors.get(emotion.lower(), (128, 128, 128))
    intensity_map = {
        "subtle": 0.1,
        "medium": 0.3,
        "strong": 0.6
    }
    alpha = intensity_map.get(intensity.lower(), 0.5)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        overlay = np.full(frame.shape, tint, dtype=np.uint8)
        tinted_frame = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)
        out.write(tinted_frame)

    cap.release()
    out.release()

    return output_path
