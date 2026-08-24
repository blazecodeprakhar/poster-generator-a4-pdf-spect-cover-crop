# poster-generator-a4-pdf-spect-cover-crop

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-CustomTkinter-purple.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Author](https://img.shields.io/badge/author-blazecodeprakhar-orange.svg)](https://github.com/blazecodeprakhar)

**Poster Studio Desktop** is a modern, high-performance Python desktop application to turn any poster images into high-resolution, print-ready A4 PDFs. It automatically applies an **Aspect Cover Fit** algorithm to ensure posters cover 100% of the A4 page without ugly white borders, distortion, or excessive zooming.

Developed by **[blazecodeprakhar](https://github.com/blazecodeprakhar)**.

---

## 🌟 Key Features

- 🎯 **Aspect Cover Fit (Zero White Borders)**: Automatically calculates aspect ratios to crop excess top/bottom or left/right pixels symmetrically, giving 100% page coverage.
- 🖼️ **Multi-Format Image Support**: Drag & drop or select PNG, JPG, JPEG, WEBP poster images.
- 🏷️ **Customizable Watermark**: Render subtle, sleek translucent watermarks on every page (Default: `https://github.com/blazecodeprakhar`).
- ⚡ **300 DPI High-Resolution Export**: Generates crisp, print-quality A4 PDFs (2480 × 3508 pixels).
- 🖥️ **Modern Dark Mode GUI**: Built with CustomTkinter for a fast, responsive desktop experience on Windows, macOS, and Linux.
- 🧵 **Multi-Threaded Processing**: Smooth PDF export with live progress bars without UI freeze.

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install the dependencies:

```bash
git clone https://github.com/blazecodeprakhar/poster-generator-a4-pdf-spect-cover-crop.git
cd poster-generator-a4-pdf-spect-cover-crop
pip install -r requirements.txt
```

### 2. Launching the App

**On Windows (Double-Click):**
Simply double-click `Run_Poster_Studio.bat` in the project folder.

**Via Terminal:**
```bash
python main.py
```

**CLI Batch Converter:**
```bash
python generate_pdf.py
```

---

## 📁 Repository Structure

```
poster-generator-a4-pdf-spect-cover-crop/
├── PosterStudioApp.py       # Main CustomTkinter Desktop GUI application
├── main.py                  # Entry launcher script
├── generate_pdf.py          # Batch CLI converter engine
├── Run_Poster_Studio.bat    # Double-clickable Windows launcher
├── requirements.txt         # Dependencies
├── README.md                # Documentation
├── .gitignore               # Git ignore rules
└── LICENSE                  # MIT License
```

---

## 👤 Author & Support

Created with ❤️ by **Prakhar**
- GitHub: [@blazecodeprakhar](https://github.com/blazecodeprakhar)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
