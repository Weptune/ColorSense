# color_pipeline.py

from color_analysis import analyze_colors, extract_frames, plot_rgb_timeline
from color_grading import apply_emotion_tint
from emotion_detector.model import predict_emotion_from_rgb

def run_full_pipeline(video_path, num_frames=20, emotion=None, intensity='medium', log_callback=print):
    log_callback("Extracting frames...")
    frames = extract_frames(video_path, num_frames=num_frames)

    log_callback("Analyzing original video colors...")
    original_rgb = analyze_colors(frames)
    original_rgb_plot = plot_rgb_timeline(original_rgb, title="Original RGB Timeline", output_path="outputs/original_rgb_timeline.png")

    if not emotion:
        log_callback("Predicting emotion from video...")
        predicted_emotion = predict_emotion_from_rgb(original_rgb, frames)
    else:
        predicted_emotion = emotion
    log_callback(f"Using emotion: {predicted_emotion}")

    log_callback(f"Applying {intensity} grading for emotion '{predicted_emotion}'...")
    output_video_path = f"outputs/graded_video_{predicted_emotion}_{intensity}.mp4"
    apply_emotion_tint(video_path, predicted_emotion, intensity=intensity, output_path=output_video_path)

    log_callback("Extracting frames from graded video...")
    graded_frames = extract_frames(output_video_path, num_frames=num_frames)
    log_callback("Analyzing graded video colors...")
    graded_rgb = analyze_colors(graded_frames)
    graded_rgb_plot = plot_rgb_timeline(graded_rgb, title="Graded RGB Timeline", output_path="outputs/graded_rgb_timeline.png")

    # Calculate average RGBs
    avg_original_rgb = [round(sum(x)/len(x), 2) for x in zip(*original_rgb)]
    avg_graded_rgb = [round(sum(x)/len(x), 2) for x in zip(*graded_rgb)]

    return {
        "predicted_emotion": predicted_emotion,
        "output_video": output_video_path,
        "original_rgb_plot": original_rgb_plot,
        "graded_rgb_plot": graded_rgb_plot,
        "avg_original_rgb": avg_original_rgb,
        "avg_graded_rgb": avg_graded_rgb
    }
