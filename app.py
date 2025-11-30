from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import numpy as np
import os
from pathlib import Path
import json
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
MATCH_FOLDER = 'static/matched'
IMAGES_FOLDER = 'dataset'
CSV_FILE = 'dataset.csv'
MODEL_PATH = 'face_model.yml'
LABELS_PATH = 'labels.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCH_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)
recognizer = cv2.face.LBPHFaceRecognizer_create()
labels_dict = {}
model_trained = False


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_labels():
    global labels_dict
    if os.path.exists(LABELS_PATH):
        with open(LABELS_PATH, 'r') as f:
            labels_dict = json.load(f)
            labels_dict = {int(k): v for k, v in labels_dict.items()}
    return labels_dict


def save_labels():
    with open(LABELS_PATH, 'w') as f:
        json.dump({str(k): v for k, v in labels_dict.items()}, f)


def train_model_from_csv():
    """Train model from CSV file and images folder"""
    global recognizer, labels_dict, model_trained
    
    if not os.path.exists(CSV_FILE):
        return False, f"CSV file '{CSV_FILE}' not found"
    
    if not os.path.exists(IMAGES_FOLDER):
        return False, f"Images folder '{IMAGES_FOLDER}' not found"
    
    faces = []
    face_labels = []
    labels_dict = {}
    label_counter = 0
    person_to_label = {}
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header if exists
            
            for row in reader:
                if len(row) < 2:
                    continue
                
                image_filename = row[0].strip()
                person_name = row[1].strip()
                
                # Assign label to person if new
                if person_name not in person_to_label:
                    person_to_label[person_name] = label_counter
                    labels_dict[label_counter] = person_name
                    label_counter += 1
                
                # Load image
                image_path = os.path.join(IMAGES_FOLDER, image_filename)
                
                if not os.path.exists(image_path):
                    print(f"Warning: Image not found: {image_path}")
                    continue
                
                try:
                    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None and img.size > 0:
                        faces.append(img)
                        face_labels.append(person_to_label[person_name])
                except Exception as e:
                    print(f"Error reading {image_path}: {e}")
        
        if not faces:
            return False, "No valid images found in dataset"
        
        recognizer.train(faces, np.array(face_labels))
        recognizer.save(MODEL_PATH)
        save_labels()
        model_trained = True
        return True, f"Model trained on {len(faces)} images from {len(labels_dict)} people"
    
    except Exception as e:
        return False, f"Training error: {str(e)}"


def load_model():
    global recognizer, labels_dict, model_trained
    if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
        try:
            recognizer.read(MODEL_PATH)
            load_labels()
            model_trained = True
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    return False


def get_dataset_stats():
    """Get statistics from CSV file"""
    if not os.path.exists(CSV_FILE):
        return 0, 0, {}
    
    total_images = 0
    people_dict = {}
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header
            
            for row in reader:
                if len(row) < 2:
                    continue
                
                person_name = row[1].strip()
                if person_name not in people_dict:
                    people_dict[person_name] = 0
                people_dict[person_name] += 1
                total_images += 1
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return total_images, len(people_dict), people_dict


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auto-train', methods=['POST'])
def auto_train():
    """Auto-train from CSV and images folder"""
    success, message = train_model_from_csv()
    
    if success:
        return jsonify({
            'message': message,
            'status': 'success'
        }), 200
    else:
        return jsonify({
            'message': message,
            'status': 'error'
        }), 400


@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    if not os.path.exists(MODEL_PATH):
        return jsonify({'error': 'Model not trained. Train first'}), 400
    
    load_model()
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        img = cv2.imread(filepath)
        if img is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        results = []
        output_img = img.copy()
        
        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]
            label, confidence = recognizer.predict(face_roi)
            
            name = labels_dict.get(label, "Unknown")
            confidence_pct = round(100 - confidence)
            
            if confidence_pct > 70:
                color = (0, 255, 0)
            else:
                color = (0, 0, 255)
            
            cv2.rectangle(output_img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(output_img, f"{name} ({confidence_pct}%)", (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            results.append({
                'name': name,
                'confidence': confidence_pct,
                'matched': confidence_pct > 70
            })
        
        output_filename = secure_filename(f"matched_{filename}")
        output_path = os.path.join(MATCH_FOLDER, output_filename)
        cv2.imwrite(output_path, output_img)
        
        return jsonify({
            'results': results,
            'matched_image': f'/static/matched/{output_filename}',
            'total_faces': len(faces)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Recognition error: {str(e)}'}), 500


@app.route('/status', methods=['GET'])
def status():
    model_exists = os.path.exists(MODEL_PATH)
    total_images, people_count, _ = get_dataset_stats()
    
    return jsonify({
        'model_trained': model_exists,
        'total_images': total_images,
        'people_count': people_count,
        'labels': labels_dict
    }), 200


@app.route('/dataset-info', methods=['GET'])
def dataset_info():
    """Get detailed dataset information"""
    total_images, people_count, people_dict = get_dataset_stats()
    
    return jsonify({
        'total_images': total_images,
        'people': people_dict,
        'people_count': people_count
    }), 200


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large'}), 413


if __name__ == "__main__":
    print("Checking for existing model...")
    if load_model():
        print("Model loaded successfully!")
    else:
        print("No trained model found. Train first!")
    
    app.run(debug=True)