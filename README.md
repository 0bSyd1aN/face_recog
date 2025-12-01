# Face Recognition System

A web-based facial recognition application built with Flask and OpenCV.

---

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate Dataset CSV

```bash
python generate_csv.py
```

### 5. Run Application

```bash
python app.py
```

### 6. Open Browser

```
http://localhost:5000
```

---

## Setup Requirements

- Python 3.7+
- pip package manager
- Images in `dataset/` folder

---

## How to Use

1. Place images in `dataset/` folder
2. Run `python generate_csv.py`
3. Go to `http://localhost:5000`
4. Click "⚡ Auto-Train Model"
5. Upload image and click "🔍 Recognize Faces"

---

## CSV Format

```csv
image_filename,person_name

```

---

## Troubleshooting

### Fix pip install issues

```bash
pip cache purge
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Fix missing cv2 module

```bash
pip install opencv-python opencv-contrib-python --force-reinstall
```

### Generate CSV

```bash
python generate_csv.py
```

### Change Flask port

Edit `app.py` last line:
```python
app.run(debug=True, port=5001)
```

---

## Features

- ✅ Auto-train from CSV dataset
- ✅ Real-time face detection
- ✅ Confidence scoring
- ✅ Modern responsive UI
- ✅ Green boxes for matched faces
- ✅ Red boxes for unknown faces

---

## Dependencies

- flask
- opencv-python
- opencv-contrib-python
- numpy
- werkzeug

---

## License

Sujan_Tech