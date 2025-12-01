🔍 Face Recognition System
A modern web-based face recognition application built with Flask and OpenCV. Train on your dataset and recognize faces in real-time!

📋 Prerequisites

Python 3.7+ installed on your system
pip (Python package manager)
Images in your dataset/ folder
CSV file mapping images to person names


🚀 Complete Setup Guide (One Shot)
Step 1: Create Project Folder
bashmkdir face_recognition_project
cd face_recognition_project
Step 2: Create Virtual Environment
Windows:
bashpython -m venv venv
venv\Scripts\activate
macOS/Linux:
bashpython -m venv venv
source venv/bin/activate
Step 3: Upgrade pip
bashpython -m pip install --upgrade pip
pip cache purge
Step 4: Install Dependencies
bashpip install -r requirements.txt
If that fails, install manually:
bashpip install flask opencv-python opencv-contrib-python numpy werkzeug
Step 5: Prepare Your Dataset
Expected folder structure:
face_recognition_project/
├── venv/
├── dataset/                    ← Put all your .jpg, .png files here
│   ├── alice.png
│   ├── bob.jpg
│   ├── carol_1.png
│   └── ...
├── static/
│   ├── uploads/
│   └── matched/
├── templates/
│   └── index.html
├── app.py
├── generate_csv.py
└── requirements.txt
Step 6: Generate dataset.csv
bashpython generate_csv.py
Output:
✓ alice.png -> Alice
✓ bob.jpg -> Bob
✓ carol_1.png -> Carol
✓ ...

✅ Created dataset.csv with X entries!
Step 7: Start the Application
bashpython app.py
Expected output:
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Step 8: Open in Browser
http://localhost:5000

🎯 Using the Application
Train the Model

Click the "⚡ Auto-Train Model" button
Wait for the training to complete
You'll see a success message and statistics

Recognize Faces

Upload an image with faces
Click "🔍 Recognize Faces"
View results with confidence scores
See the annotated image with bounding boxes


📁 File Structure
face_recognition_project/
├── app.py                      # Main Flask application
├── generate_csv.py             # CSV generator script
├── requirements.txt            # Python dependencies
├── dataset.csv                 # Generated: image mappings
├── face_model.yml              # Generated: trained model
├── labels.json                 # Generated: person labels
├── dataset/                    # Your images folder
├── static/
│   ├── uploads/               # Uploaded test images
│   └── matched/               # Output images with boxes
└── templates/
    └── index.html             # Web UI

🔧 Troubleshooting
Issue: pip install fails
bash# Clear cache and try again
pip cache purge
pip install --upgrade pip
pip install -r requirements.txt
Issue: No module named 'cv2'
bashpip install opencv-python opencv-contrib-python --force-reinstall
Issue: No such file or directory: 'dataset.csv'
bash# Generate it first
python generate_csv.py
Issue: Model not trained message

Make sure your images are in dataset/ folder
Run python generate_csv.py
Click "⚡ Auto-Train Model" button

Issue: Port 5000 already in use
bash# Use a different port
# Edit app.py, change the last line:
app.run(debug=True, port=5001)

📊 CSV Format
Your dataset.csv should look like:
csvimage_filename,person_name
alice_1.png,Alice
bob_5.jpg,Bob
carol_2.png,Carol
The script auto-generates this from your image filenames!

🎨 Features
✅ Auto-train from CSV dataset
✅ Real-time face detection
✅ Confidence scoring (0-100%)
✅ Beautiful modern UI
✅ Green boxes for matched faces
✅ Red boxes for unknown faces
✅ Live status updates
✅ Responsive design
✅ Easy dataset management

💾 Requirements
All dependencies are in requirements.txt:

flask - Web framework
opencv-python - Face detection
opencv-contrib-python - Face recognition
numpy - Array operations
werkzeug - Utilities


🚨 Quick Fix Commands
If something breaks, try these in order:
bash# 1. Clear everything and start fresh
pip cache purge
pip install --upgrade pip setuptools wheel

# 2. Reinstall OpenCV
pip install opencv-python opencv-contrib-python --force-reinstall --no-cache-dir

# 3. Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# 4. Generate CSV
python generate_csv.py

# 5. Run app
python app.py

📞 Support
If you encounter issues:

Check that Python 3.7+ is installed: python --version
Verify images are in dataset/ folder
Run python generate_csv.py to create CSV
Check browser console for errors (F12)
Try with a fresh virtual environment


🎯 One-Line Quick Start (After Setup)
bash# Activate venv, then run:
python app.py
Open: http://localhost:5000 → Click "⚡ Auto-Train Model" → Upload image → Done! 🎉

Enjoy your Face Recognition System! 🚀