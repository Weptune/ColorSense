# video_processor/emotion_grader.py

import cv2
import numpy as np
from video_processor.emotion_params import emotion_color_grades, intensity_map

def adjust_colors(frame, emotion, intensity="medium"):
    """
    Adjusts the color grading of the frame based on the emotion and intensity.
    Args:
        frame: np.ndarray - input BGR image
        emotion: str - emotion name (e.g., "sad", "happy")
        intensity: str - one of 'subtle', 'medium', 'strong'
    Returns:
        Color graded frame as np.uint8 image.
    """
    img = frame.astype(np.float32)
    intensity_factor = intensity_map.get(intensity.lower(), 1.0)
    e = emotion.lower()

    if e in emotion_color_grades:
        params = emotion_color_grades[e]
        # Note: OpenCV uses BGR format
        # B channel = 0, G channel = 1, R channel = 2
        img[..., 2] = np.clip(img[..., 2] * (params["red"] * intensity_factor), 0, 255)
        img[..., 1] = np.clip(img[..., 1] * (params["green"] * intensity_factor), 0, 255)
        img[..., 0] = np.clip(img[..., 0] * (params["blue"] * intensity_factor), 0, 255)
        img = cv2.convertScaleAbs(img)
    else:
        # If emotion unknown, return original frame
        img = cv2.convertScaleAbs(img)
    return img
