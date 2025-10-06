# yolo-labeling-studio
🎯 Advanced YOLO Labeling Tool with Real-Time Performance - A feature-rich desktop application for creating YOLO format datasets with movable edges, smart rendering, and professional annotation workflow.

No, there are several formatting issues with your README.md. The main problems are:

1. **Missing code block formatting** for Windows installation
2. **Missing section headers** (##) for some sections
3. **Incorrect markdown formatting** for the feature checklist
4. **Broken structure** in the middle sections

Here's the corrected version that you can copy and paste directly:

```markdown
# 🎯 YOLO Labeling Studio Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Professional YOLO annotation tool with real-time performance and smart features**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Future Plans](#-future-plans)

</div>

---

## 🚀 What is This?

YOLO Labeling Studio Pro is not just another annotation tool - it's your **AI-powered assistant** for creating high-quality YOLO datasets! Built with performance in mind, it transforms the tedious task of bounding box annotation into a smooth, efficient workflow.

### ✨ Why Choose This Tool?

- ⚡ **Real-time performance** with smart rendering
- 🎯 **Movable edges & corners** for pixel-perfect adjustments
- 🎨 **Dark/Light mode** for comfortable long sessions
- 📚 **Smart session management** that remembers your work
- 🖱️ **Intuitive keyboard shortcuts** for power users

---

## 🎨 Features

### Core Annotation
- ✅ **YOLO format support** - Direct export to YOLO txt files
- ✅ **Movable edges & corners** - Precise box adjustments
- ✅ **Multi-class support** - Organize your objects efficiently
- ✅ **Real-time drawing** - See boxes as you draw them
- ✅ **Smart zoom & pan** - Navigate large images smoothly

### Professional Workflow
- ✅ **Undo/Redo history** - Never lose work accidentally
- ✅ **Batch operations** - Process multiple images efficiently
- ✅ **Auto-save sessions** - Resume right where you left off
- ✅ **Progress tracking** - Know how much work remains
- ✅ **Processed image management** - Keep workspace organized

### User Experience
- ✅ **Dark/Light themes** - Work comfortably day or night
- ✅ **Comprehensive shortcuts** - Keyboard-driven workflow
- ✅ **Visual feedback** - Clear selection and hover states
- ✅ **Performance optimized** - Handles large datasets smoothly

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Linux Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/yolo-labeling-studio-pro.git
cd yolo-labeling-studio-pro

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python yolo_labeling_tool.py
```

### Windows Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/yolo-labeling-studio-pro.git
cd yolo-labeling-studio-pro

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python yolo_labeling_tool.py
```

### Manual Dependency Installation
If you prefer manual installation:

```bash
pip install opencv-python pillow numpy
```

---

## 🎮 How to Use

### 🖱️ Basic Workflow

1. **Launch the application**
   ```bash
   python yolo_labeling_tool.py
   ```

2. **Set up directories**
   - Click "Open Image Dir" to select your images folder
   - Click "Open Label Dir" to select where labels will be saved

3. **Start annotating**
   - Select a class from the left panel
   - Click and drag on image to draw bounding boxes
   - Adjust boxes using movable edges and corners
   - Save with `Ctrl+S` or use auto-save

### 🎯 Advanced Features

#### Movable Edges & Corners
- **Click corners** to resize from specific points
- **Click edges** to adjust single sides
- **Click inside** to move entire boxes
- Visual cursor changes show what you're adjusting!

#### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save labels |
| `Ctrl+Z` | Undo |
| `Delete` | Delete selected box |
| `A / ←` | Previous image |
| `D / →` | Next image |
| `Ctrl+A` | Select all boxes |
| `Ctrl+D` | Duplicate box |
| `Ctrl+Shift+S` | Quick save & next |
| `R` | Reset zoom |
| `+ / -` | Zoom in/out |
| `I` | Reload current image |

#### Smart Session Management
- Tool automatically saves your session
- Reopens last worked-on image
- Removes processed images from workspace
- Maintains annotation history

### 🎨 Customization

Edit `config.jsonc` to customize:
- Class names and colors
- Keyboard shortcuts
- UI themes and appearance
- Performance settings
- File paths and directories

---

## 🔮 Future Plans

### 🧠 AI-Powered Features (Coming Soon!)

**Smart Pre-labeling with YOLO Model**
- Load pre-trained YOLO model
- Auto-detect objects on image load
- Human-in-the-loop verification
- Dramatically reduce manual work

### 🚀 Enhanced Features
- [ ] **AI pre-labeling** - YOLO model suggests boxes automatically
- [ ] **Multi-object tracking** - Track objects across video frames
- [ ] **Export to multiple formats** - COCO, Pascal VOC, etc.
- [ ] **Team collaboration** - Multiple annotators, one project
- [ ] **Quality metrics** - Detect annotation inconsistencies
- [ ] **Plugin system** - Extend functionality with custom plugins
- [ ] **Web version** - Browser-based annotation
- [ ] **API integration** - Connect to model training pipelines

### 🤖 AI Integration Roadmap
1. **Phase 1**: Basic YOLO model for object suggestions
2. **Phase 2**: Smart box refinement using AI
3. **Phase 3**: Active learning - model improves from your corrections
4. **Phase 4**: Full AI-assisted workflow

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: Images not loading  
**Solution**: Check image paths and ensure files are not corrupted

**Problem**: Labels not saving  
**Solution**: Verify write permissions in label directory

**Problem**: Performance issues with large images  
**Solution**: Enable GPU acceleration in config or resize images

**Problem**: UI looks different  
**Solution**: Reset config file or check display scaling settings

### Getting Help
- Check the `logs/` folder for detailed error information
- Ensure all dependencies are properly installed
- Verify Python version compatibility

---

## 🤝 Contributing

We love contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting
black yolo_labeling_tool.py
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Acknowledgments

- Built with amazing open-source libraries: OpenCV, PIL, Tkinter
- Inspired by the computer vision community
- Special thanks to all contributors and testers

---

<div align="center">

**Happy Labeling! 🎯**

*If this tool saves you time, consider giving it a ⭐ on GitHub!*

</div>
```
