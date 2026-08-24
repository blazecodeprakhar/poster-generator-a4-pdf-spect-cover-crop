# poster-generator-a4-pdf-spect-cover-crop

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![UI Framework](https://img.shields.io/badge/GUI-CustomTkinter-purple.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Author](https://img.shields.io/badge/author-blazecodeprakhar-orange.svg)](https://github.com/blazecodeprakhar)

**Poster Studio Desktop** is a modern, high-performance desktop software to turn any poster images into high-resolution, print-ready A4 PDFs. It automatically applies an **Aspect Cover Fit** algorithm to ensure posters cover 100% of the A4 page without ugly white borders, distortion, or excessive zooming.

Developed by **[blazecodeprakhar](https://github.com/blazecodeprakhar)**.

---

## ⚡ 1-Click Launch Software (No Python Required)

> 🚀 **`PosterStudio.exe` is located right in the main root folder of this repository!**

1. Simply double-click **[`PosterStudio.exe`](PosterStudio.exe)** in the top folder to launch the software directly on Windows!
2. No installation, Python setup, or command line required.

---

## 💻 Developer Guide: Running Raw Source Code

If you prefer to run or modify the Python source code directly:

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
   - **On Windows (1-Click Batch)**: Double-click `Run_Poster_Studio.bat`.
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
├── PosterStudio.exe         # 🚀 1-Click Standalone Desktop Software
├── PosterStudioApp.py       # Main CustomTkinter Desktop GUI source code
├── main.py                  # Entry launcher script
├── generate_pdf.py          # Batch CLI converter engine
├── Run_Poster_Studio.bat    # Windows batch launcher
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
