# utils/emotion_grader.py

import cv2
import numpy as np

# Define color grading presets for different emotions and intensities
GRADING_PRESETS = {
    "Happy": {
        "low":   lambda img: cv2.convertScaleAbs(img * 1.05),
        "medium": lambda img: cv2.convertScaleAbs(adjust(img, r=1.2, g=1.1, b=0.9)),
        "high":  lambda img: cv2.convertScaleAbs(adjust(img, r=1.4, g=1.2, b=0.8)),
    },
    "Sad": {
        "low":   lambda img: cv2.convertScaleAbs(img * 0.95),
        "medium": lambda img: cv2.convertScaleAbs(adjust(img, r=0.8, g=0.9, b=1.2)),
        "high":  lambda img: cv2.convertScaleAbs(adjust(img, r=0.6, g=0.8, b=1.4)),
    },
    "Calm": {
        "low":   lambda img: cv2.convertScaleAbs(adjust(img, r=0.95, g=1.0, b=1.05)),
        "medium": lambda img: cv2.convertScaleAbs(adjust(img, r=0.9, g=1.0, b=1.1)),
        "high":  lambda img: cv2.convertScaleAbs(adjust(img, r=0.8, g=0.9, b=1.2)),
    },
    "Energetic": {
        "low":   lambda img: cv2.convertScaleAbs(adjust(img, r=1.1, g=1.05, b=1.0)),
        "medium": lambda img: cv2.convertScaleAbs(adjust(img, r=1.3, g=1.2, b=1.0)),
        "high":  lambda img: cv2.convertScaleAbs(adjust(img, r=1.5, g=1.3, b=0.9)),
    }
}

def adjust(img, r=1.0, g=1.0, b=1.0):
    """Apply RGB multipliers to an image"""
    img = img.astype(np.float32)
    img[..., 0] *= b
    img[..., 1] *= g
    img[..., 2] *= r
    img = np.clip(img, 0, 255)
    return img

def apply_emotion_grade(frame, emotion, intensity="medium"):
    """Apply color grading based on emotion and intensity"""
    if emotion in GRADING_PRESETS and intensity in GRADING_PRESETS[emotion]:
        return GRADING_PRESETS[emotion][intensity](frame)
    return frame
