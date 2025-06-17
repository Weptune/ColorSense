# 🎨 ColorSense: Emotion-Based Video Color Analysis and Grading Tool

**ColorSense** is an intelligent video analysis tool that detects the emotional tone of a video based on its color profile and applies targeted color grading to enhance or convey a specific mood. Designed for filmmakers, video editors, and researchers, it features:

- 🧠 Emotion prediction from average color trends  
- 📊 RGB timeline visualizations of original and graded videos  
- 🎞️ Frame extraction for direct visual comparison  
- 🎨 Automatic or user-guided emotion-based color grading  
- 💾 Output of enhanced video and side-by-side plots


![image](https://github.com/user-attachments/assets/482b4832-dc1f-4b1e-ac79-2b50b54a04c8)


---

## 🔧 Features

- **Automatic Emotion Detection**: Predicts emotional tone (e.g., happy, sad, calm) from video color data.
- **Manual Emotion Input**: Override emotion detection with your own choice and intensity level.
- **Color Grading Engine**: Applies mood-specific tints based on psychological color-emotion mappings.
- **Visualization Tools**: Creates RGB timeline plots for both original and graded videos.
- **Modular Design**: Clean, maintainable Python package structure for easy extension.

---

## 📸 Example Output

| Feature                | Output                          |
|------------------------|----------------------------------|
| Original RGB Timeline  | ![Original RGB](./outputs/runs/run_YYYYMMDD_HHMMSS/rgb_timeline_original_plot.png) |
| Graded RGB Timeline    | ![Graded RGB](./outputs/runs/run_YYYYMMDD_HHMMSS/rgb_timeline_graded_plot.png) |
| Enhanced Video         | `outputs/runs/run_*/graded_video_*.mp4` |

---

## 📁 Project Structure

colorsense/
│
├── colorsense/
│ ├── init.py
│ ├── color_analysis.py # Frame extraction, RGB mean calculation, RGB plots
│ ├── color_grading.py # Tint logic based on emotion & intensity
│ ├── emotion_detector/
│ │ ├── init.py
│ │ └── model.py # RGB-based emotion prediction
│ └── run_pipeline.py # Main orchestration script
│
├── inputs/ # Put input videos here
├── outputs/
│ └── runs/run_/ # Auto-created folders for each run
│ ├── rgb_timeline_original_plot.png
│ ├── rgb_timeline_graded_plot.png
│ ├── graded_video_.mp4
│ └── frames/
│ └── frame_000.jpg ...

## 🧠 Supported Emotions
- happy
- sad
- calm
- angry
- romantic
- fear
- neutral (default fallback)

Each emotion supports these grading intensities: subtle, medium, and strong.

---

## 🧪 Dependencies
- opencv-python
- numpy
- matplotlib

---

## 📚 Future Enhancements
- Deep learning-based emotion recognition from faces and scenes
- GUI for drag-and-drop editing
- Fine-grained control over hue/saturation curves
- Export of summary stats (mean color deltas, histograms)

