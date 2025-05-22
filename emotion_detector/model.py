import numpy as np

def predict_emotion_from_rgb(rgb_means, rgb_timeline):
    rgb_means = np.array(rgb_means)
    if rgb_means.ndim == 1 and rgb_means.size == 3:
        avg_rgb = rgb_means
    else:
        avg_rgb = np.mean(rgb_means, axis=0)

    r, g, b = avg_rgb if len(avg_rgb) == 3 else (float(avg_rgb),) * 3

    if r > g and r > b:
        return "happy"
    elif b > r and b > g:
        return "sad"
    elif g > r and g > b:
        return "calm"
    else:
        return "neutral"
