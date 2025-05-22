import numpy as np
from video_processor.rgb_plotter import generate_rgb_timeline

# Generate RGB timeline and save plot
timeline, output_path = generate_rgb_timeline("outputs/frames", "outputs")

# Save the numeric timeline as .npy
np.save("outputs/rgb_timeline.npy", timeline)

print("✅ RGB timeline saved as", output_path)
