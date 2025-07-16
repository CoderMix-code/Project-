# EduQRCheck

**EduQRCheck** is a simple QR code-based attendance system built with Python. It helps schools track student attendance by scanning QR codes assigned to each student.

## 📌 Features

- Generate unique QR codes for each student
- Scan QR codes using a webcam or external scanner
- Automatically log attendance data with timestamp
- Simple terminal interface (or extendable to GUI)
- Stores attendance in local database (CSV/SQLite)

## 🛠️ Tech Stack

- Python 3
- OpenCV (`cv2`) for camera and image processing
- `qrcode` library for QR code generation
- `pyzbar` or `opencv` for QR code scanning
- SQLite3 or CSV for attendance data storage

## 🚀 Installation

```bash
git clone https://github.com/yourusername/eduqrcheck.git
cd eduqrcheck
pip install -r requirements.txt
# Project-