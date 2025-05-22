from video_processor.color_analyzer import analyze_colors
# If you saved analyze_colors_from_frames in video_processor folder, import it as well
# from video_processor.color_analyzer import analyze_colors_from_frames

def main():
    video_path = "test_videos/sample.mp4"
    frames_folder = "outputs/frames"
    output_dir = "outputs"

    # Option 1: Analyze colors directly from video file
    avg_rgb = analyze_colors(video_path, f"{output_dir}/color_analysis_plot.png")
    print("Average RGB from video:", avg_rgb)

    # Option 2: Analyze colors from extracted frames (if frames exist)
    # avg_rgb_frames = analyze_colors_from_frames(frames_folder, f"{output_dir}/color_analysis_plot_from_frames.png")
    # print("Average RGB from frames folder:", avg_rgb_frames)

if __name__ == "__main__":
    main()
