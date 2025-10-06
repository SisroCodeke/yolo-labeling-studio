#!/usr/bin/env python3
"""
YOLO Labeling Studio - Professional image annotation tool
Main entry point
"""

import tkinter as tk
import logging
from core.application import YOLOLabelStudio

def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = YOLOLabelStudio(root)
        root.mainloop()
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger("YOLOLabelStudio")
        logger.error("Fatal error", exc_info=True)
        tk.messagebox.showerror(
            "Fatal Error", 
            f"Application encountered a fatal error:\n{str(e)}\n\nCheck log file for details."
        )

if __name__ == '__main__':
    main()
