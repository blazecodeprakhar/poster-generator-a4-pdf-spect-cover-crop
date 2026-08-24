# poster-generator-a4-pdf-spect-cover-crop

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-CustomTkinter-purple.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Author](https://img.shields.io/badge/author-blazecodeprakhar-orange.svg)](https://github.com/blazecodeprakhar)

**Poster Studio Desktop** is a modern, high-performance desktop application to turn any poster images into high-resolution, print-ready A4 PDFs. It automatically applies an **Aspect Cover Fit** algorithm to ensure posters cover 100% of the A4 page without ugly white borders, distortion, or excessive zooming.

Developed by **[blazecodeprakhar](https://github.com/blazecodeprakhar)**.

---

## 💻 How to Use the Software

Choose the easiest option for your system:

### 🌟 Option 1: Standalone Software Executable (Easiest - No Python Required)
1. Download the latest **`PosterStudio`** executable folder from the GitHub Releases page or `dist/` directory.
2. Double-click **`PosterStudio.exe`** to launch the software directly on Windows!

---

### 💻 Option 2: Run Raw Source Code (For Developers)

If you have Python installed on your PC, follow these quick steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/blazecodeprakhar/poster-generator-a4-pdf-spect-cover-crop.git
   cd poster-generator-a4-pdf-spect-cover-crop
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the software:**
   - **On Windows (1-Click)**: Double-click `Run_Poster_Studio.bat` in the folder.
   - **Via Terminal**:
     ```bash
     python main.py
     ```
   - **CLI Batch Mode**:
     ```bash
     python generate_pdf.py
     ```

---

## ✨ Key Features

- 🎯 **Aspect Cover Fit (Zero White Borders)**: Automatically calculates aspect ratios to crop excess top/bottom or left/right pixels symmetrically, giving 100% page coverage.
- 🖼️ **Multi-Format Image Support**: Select PNG, JPG, JPEG, WEBP poster images.
- ⚡ **300 DPI High-Resolution Export**: Generates crisp, print-quality clean A4 PDFs (2480 × 3508 pixels).
- 🔗 **Built-in Software Branding**: Embedded developer link to [`github.com/blazecodeprakhar`](https://github.com/blazecodeprakhar).
- 🖥️ **Modern Dark Mode GUI**: Built with CustomTkinter for a fast, responsive desktop experience.
- 🧵 **Multi-Threaded Processing**: Smooth PDF export with live progress bars without UI freeze.

---

## 📁 Repository Structure

```
poster-generator-a4-pdf-spect-cover-crop/
├── PosterStudioApp.py       # Main CustomTkinter Desktop GUI application
├── main.py                  # Entry launcher script
├── generate_pdf.py          # Batch CLI converter engine
├── Run_Poster_Studio.bat    # Double-clickable Windows batch launcher
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
