from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
MATCH_FOLDER = 'static/matched'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MATCH_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)   # 👈 Uses defined variable
    file.save(filepath)

    # your recognition logic...

    return "Done"

if __name__ == "__main__":
    app.run(debug=True)
