import numpy as np

def predict_emotion(rgb_means):
    avg_rgb = np.mean(rgb_means, axis=0)
    r, g, b = avg_rgb

    if r > b and r > g:
        return "angry"
    elif b > r and b > g:
        return "sad"
    elif g > r and g > b:
        return "calm"
    elif r > 180 and g > 180 and b > 180:
        return "happy"
    else:
        return "neutral"
