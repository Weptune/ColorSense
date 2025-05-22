import numpy as np
from emotion_detector.model import predict_emotion_from_rgb

# Load saved RGB data
rgb_means = np.load("outputs/rgb_means.npy")  # Color distribution
rgb_timeline = np.load("outputs/rgb_timeline.npy")  # Temporal trends

# Run prediction
predicted_emotion = predict_emotion_from_rgb(rgb_means, rgb_timeline)

print(f"🎭 Predicted emotional tone: {predicted_emotion}")
