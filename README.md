
# 🎯 YOLO Labeling Studio

> 🎯 Professional YOLO labeling tool with real-time rendering, movable box edges, dark mode, session recovery, and planned AI-assisted pre-labeling.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Professional YOLO annotation tool with real-time performance, movable edges, and AI-ready workflow**

[Features](#-features) • [Installation](#%EF%B8%8F-installation) • [Usage](#-how-to-use) • [Future Plans](#-future-plans)

</div>

---

## 🚀 What is This?

**YOLO Labeling Studio Pro** is a desktop application built for **serious annotators** who need speed, precision, and comfort while labeling images in YOLO format. Unlike basic tools, it offers **movable box edges**, **real-time preview**, **session recovery**, and **keyboard-driven workflow**—all in a sleek, responsive interface.

And soon? **AI pre-labeling** using a YOLO model to auto-detect objects before you even start!

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
- (Optional) GPU not required – runs on CPU

### 🐧 Linux

```bash
git clone https://github.com/SisroCodeke/yolo-labeling-studio.git
cd yolo-labeling-studio

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
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

> ✅ Windows users: `tkinter`, `PIL`, and `numpy` are usually included with Python, but `opencv-python` must be installed via pip.

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

## 🔮 Future Plans

### 🤖 AI-Powered Pre-Labeling (Coming Soon!)
We’re adding **built-in YOLO object detection** so the tool can:
- Load a pre-trained YOLO model (e.g., YOLOv8n)
- Auto-detect objects when an image loads
- Let you **accept, edit, or delete** suggested boxes
- **Dramatically reduce labeling time** by 50–80%

### 🗺️ Roadmap
- [x] Core labeling engine ✅  
- [ ] **AI pre-labeling with YOLO model** (Phase 1)
- [ ] Export to COCO, Pascal VOC
- [ ] Video frame labeling
- [ ] Plugin system
- [ ] Web version (Flask + React)

> 🌟 **Want to help build the AI feature?** Contributions welcome!

---

## 🐛 Troubleshooting

| Issue | Solution |
|------|--------|
| "No module named 'cv2'" | Run `pip install opencv-python` |
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

- Built with **OpenCV**, **Pillow**, **Tkinter**, and **Python**
- Inspired by the need for better open-source labeling tools
- Thanks to the computer vision community ❤️

---

<div align="center">

**Happy Labeling! 🎯**  
*If this saves you time, give it a ⭐ on GitHub!*

</div>
