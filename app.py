import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils.ocr import file_to_text
from utils.parser import is_aadhaar_text, extract_aadhaar_fields

UPLOAD_FOLDER='uploads'
ALLOWED={'png','jpg','jpeg','tif','tiff','bmp','pdf'}

app=Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.secret_key='secret'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(f): return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED

@app.route('/')
def index(): return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files: flash('No file'); return redirect('/')
    f=request.files['file']
    if f.filename=='': flash('No filename'); return redirect('/')
    if not allowed_file(f.filename): flash('Not allowed'); return redirect('/')

    filename=secure_filename(f.filename)
    path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(path)

    text=file_to_text(path)
    if not is_aadhaar_text(text):
        return render_template('result.html', error='Not Aadhaar card')

    data=extract_aadhaar_fields(text)
    return render_template('result.html', data=data)

if __name__=='__main__':
    app.run(debug=True)
