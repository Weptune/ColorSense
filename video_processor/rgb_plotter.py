import os
import numpy as np
import matplotlib.pyplot as plt

def generate_rgb_timeline(frames_dir, output_dir):
    rgb_means = []

    for filename in sorted(os.listdir(frames_dir)):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join(frames_dir, filename)
            img = plt.imread(path)
            mean_rgb = img[:, :, :3].mean(axis=(0, 1))  # Ignore alpha if exists
            rgb_means.append(mean_rgb)

    rgb_means = np.array(rgb_means)

    # Save RGB means as .npy for emotional tone analysis
    np.save(os.path.join(output_dir, "rgb_timeline.npy"), rgb_means)

    # Plot RGB timeline
    plt.figure(figsize=(10, 4))
    plt.plot(rgb_means[:, 0], label='Red', color='red')
    plt.plot(rgb_means[:, 1], label='Green', color='green')
    plt.plot(rgb_means[:, 2], label='Blue', color='blue')
    plt.title("RGB Timeline Across Frames")
    plt.xlabel("Frame Index")
    plt.ylabel("Mean Color Intensity")
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(output_dir, "rgb_timeline.png")
    plt.savefig(output_path)
    plt.close()
    print(f"✅ RGB timeline saved as {output_path}")

    # Return values so caller can use them
    return rgb_means, output_path
