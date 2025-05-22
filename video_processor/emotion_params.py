# video_processor/emotion_params.py

def get_adjustment_params(emotion, intensity):
    adjustments = {
        "happy": {
            "subtle": {
                "channel_multipliers": {"r": 1.05, "g": 1.05, "b": 0.95},
                "overall_multiplier": 1.03
            },
            "medium": {
                "channel_multipliers": {"r": 1.1, "g": 1.1, "b": 0.9},
                "overall_multiplier": 1.06
            },
            "strong": {
                "channel_multipliers": {"r": 1.2, "g": 1.2, "b": 0.8},
                "overall_multiplier": 1.1
            },
        },
        "sad": {
            "subtle": {
                "channel_multipliers": {"r": 0.95, "g": 0.95, "b": 1.05},
                "overall_multiplier": 0.97
            },
            "medium": {
                "channel_multipliers": {"r": 0.9, "g": 0.9, "b": 1.1},
                "overall_multiplier": 0.95
            },
            "strong": {
                "channel_multipliers": {"r": 0.8, "g": 0.8, "b": 1.2},
                "overall_multiplier": 0.9
            },
        },
        "angry": {
            "subtle": {
                "channel_multipliers": {"r": 1.1, "g": 0.95, "b": 0.95},
                "overall_multiplier": 1.02
            },
            "medium": {
                "channel_multipliers": {"r": 1.2, "g": 0.9, "b": 0.9},
                "overall_multiplier": 1.05
            },
            "strong": {
                "channel_multipliers": {"r": 1.3, "g": 0.85, "b": 0.85},
                "overall_multiplier": 1.08
            },
        },
        "calm": {
            "subtle": {
                "channel_multipliers": {"r": 0.95, "g": 1.05, "b": 1.1},
                "overall_multiplier": 1.0
            },
            "medium": {
                "channel_multipliers": {"r": 0.9, "g": 1.1, "b": 1.2},
                "overall_multiplier": 0.98
            },
            "strong": {
                "channel_multipliers": {"r": 0.8, "g": 1.2, "b": 1.3},
                "overall_multiplier": 0.95
            },
        },
    }

    try:
        return adjustments[emotion][intensity]
    except KeyError:
        print(f"⚠️ No grading config found for '{emotion}' with intensity '{intensity}'")
        return {
            "channel_multipliers": {"r": 1.0, "g": 1.0, "b": 1.0},
            "overall_multiplier": 1.0
        }
