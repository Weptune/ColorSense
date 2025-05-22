import os
print("📂 Current working directory:", os.getcwd())
print("📄 Files in current directory:", os.listdir())

from video_processor.frame_extractor import extract_frames

extract_frames("test_videos/sample.mp4", "outputs/frames", frame_rate=1)
