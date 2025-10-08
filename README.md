---

# 🎯 YOLO Labeling Studio

> 🎯 Professional YOLO labeling tool with real-time rendering, movable box edges, dark mode, session recovery, and **AI-assisted pre-labeling**.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Professional YOLO annotation tool with real-time performance, movable edges, and built-in AI assistance**

[Features](#-features) • [Installation](#%EF%B8%8F-installation) • [Usage](#-how-to-use) • [AI Assistant](#-ai-assistant)

</div>

---

## 🚀 What is This?

**YOLO Labeling Studio Pro** is a desktop application built for **serious annotators** who need speed, precision, and comfort while labeling images in YOLO format. Unlike basic tools, it offers **movable box edges**, **real-time preview**, **session recovery**, **keyboard-driven workflow**, and now—**AI-powered pre-labeling** using YOLOv8.

> ✨ **Label 5x faster**: Let AI suggest boxes on image load—then edit, accept, or discard them with one click.

---

## 🎨 Features

### ✅ Core Annotation
- **YOLO format export** – Save directly to `.txt` files
- **Movable corners & edges** – Resize boxes with pixel precision
- **Multi-class support** – Define your own object classes
- **Real-time drawing preview** – See boxes as you draw
- **Zoom & pan navigation** – Handle large images with ease

### ⚙️ Professional Workflow
- **Undo/Redo (Ctrl+Z)** – Never lose work
- **Auto-save on navigation** – Labels saved when you switch images
- **Session recovery** – Reopen where you left off
- **Processed image management** – Auto-move finished images
- **Progress bar** – Track your labeling progress

### 🤖 AI Assistant (NEW!)
- **YOLOv8n pre-labeling** – Detect objects on image load
- **Configurable classes** – Choose which COCO classes to detect
- **Editable suggestions** – Modify or delete AI boxes like manual ones
- **Toggle on/off** – Enable only when needed via config

### 🌓 User Experience
- **Dark/Light theme toggle** (`Ctrl+D`)
- **Full keyboard shortcuts** – Power-user friendly
- **RTL text support** – For Persian/Arabic class names
- **Performance-optimized rendering** – Smooth even with 100+ boxes

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- ~500 MB disk space
- Internet connection (to auto-download YOLOv8n on first AI use)

### 🐧 Linux

```bash
git clone https://github.com/SisroCodeke/yolo-labeling-studio.git
cd yolo-labeling-studio

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies (including AI support)
pip install -r requirements.txt

# Run the app
python main.py
```

> 💡 **Note**: On some Linux distros (e.g., Ubuntu), you may need to install system packages:
> ```bash
> sudo apt install python3-tk python3-pil python3-opencv
> ```

### 🪟 Windows

```powershell
git clone https://github.com/SisroCodeke/yolo-labeling-studio.git
cd yolo-labeling-studio

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

> ✅ **AI Note**: The first time you enable AI, the app will auto-download `yolov8n.pt` (~6 MB).

---

## 🎮 How to Use

### Quick Start
1. Launch with `python main.py`
2. Click **"Open Image Dir"** → select your images folder
3. Click **"Open Label Dir"** → choose where labels will be saved
4. Select a **class** from the left panel
5. **Click & drag** on the image to draw a box
6. Use **handles** to resize, or **drag inside** to move
7. Press `Ctrl+S` to save, or let auto-save do it!

### 🔑 Keyboard Shortcuts
| Key | Action |
|-----|--------|
| `Ctrl+S` | Save labels |
| `Ctrl+Z` | Undo |
| `Delete` | Delete selected box |
| `A` or `←` | Previous image |
| `D` or `→` | Next image |
| `Ctrl+A` | Select first box |
| `Ctrl+D` | Duplicate selected box |
| `Ctrl+Shift+S` | Save & go to next image |
| `R` | Reset zoom |
| `+` / `-` | Zoom in/out |
| `I` | Reload current image |
| `Ctrl+D` (again) | Toggle dark/light mode |

> 💡 Tip: Right-click a box to select it. Right-click empty space to deselect.

---

## 🤖 AI Assistant

### How It Works
1. Enable AI in your `config.json`:
   ```json
   "ai_assistant": {
     "enabled": true,
     "suggest_on_load": true,
     "enabled_classes": [2, 5, 7],  // car, bus, truck
     "confidence_threshold": 0.5
   }
   ```
2. When you open an image, YOLOv8n runs automatically.
3. Detected boxes appear as **editable suggestions** (same as manual boxes).
4. You can **move, resize, delete, or keep** them—no special workflow!

## 🔮 Future Plans



### 🗺️ Roadmap
- [x] Core labeling engine ✅  
- [x] **AI pre-labeling with YOLO model** (Phase 1)
- [ ] Export to COCO, Pascal VOC
- [ ] Video frame labeling
- [ ] Plugin system
- [ ] Web version (Flask + React)

> 🌟 **Want to help build the AI feature?** Contributions welcome!

---

### Requirements
- Add `ultralytics` to your environment:
  ```bash
  pip install ultralytics
  ```
- Your `classes.class_names` should include COCO class names (or map them).

> ⚠️ **Note**: AI only suggests boxes if **no manual labels exist** for that image (configurable).

---

## 🐛 Troubleshooting

| Issue | Solution |
|------|--------|
| "No module named 'cv2'" | Run `pip install opencv-python` |
| "No module named 'ultralytics'" | Run `pip install ultralytics` |
| Blank/gray canvas | Ensure image directory contains `.jpg`, `.png`, etc. |
| Labels not saving | Check write permissions in label directory |
| App crashes on startup | Delete `session_history.pkl` and restart |

Logs are saved in the `logs/` folder — check them for details!

---

## 🤝 Contributing

We ❤️ contributors! To get started:
1. Fork the repo
2. Create a branch: `git checkout -b feature/your-idea`
3. Commit & push your changes
4. Open a Pull Request

> 📌 Looking for ideas? Check the [Issues](https://github.com/SisroCodeke/yolo-labeling-studio/issues) tab!

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with **OpenCV**, **Pillow**, **Tkinter**, **Python**, and **Ultralytics YOLOv8**
- Inspired by the need for better open-source labeling tools
- Thanks to the computer vision community ❤️

---

<div align="center">

**Happy Labeling! 🎯**  
*If this saves you time, give it a ⭐ on GitHub!*

</div>

---
