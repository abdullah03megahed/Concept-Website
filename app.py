from flask import Flask, request, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# File upload settings
UPLOAD_FOLDER_CV = 'uploads/cvs'
UPLOAD_FOLDER_ID = 'uploads/ids'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}

os.makedirs(UPLOAD_FOLDER_CV, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_ID, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')  # use your HTML

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.to_dict()
    cv = request.files.get('cvUpload')
    id_doc = request.files.get('idUpload')

    # Validate file uploads
    if not cv or not allowed_file(cv.filename):
        flash('Invalid or missing CV file.')
        return redirect(url_for('form'))
    if not id_doc or not allowed_file(id_doc.filename):
        flash('Invalid or missing ID file.')
        return redirect(url_for('form'))

    # Save files
    cv_filename = secure_filename(cv.filename)
    id_filename = secure_filename(id_doc.filename)
    cv.save(os.path.join(UPLOAD_FOLDER_CV, cv_filename))
    id_doc.save(os.path.join(UPLOAD_FOLDER_ID, id_filename))

    # Add file paths to data
    data['cv_filename'] = cv_filename
    data['id_filename'] = id_filename

    # Save data to JSON file (or insert into DB if needed)
    with open('submissions.json', 'a') as f:
        f.write(json.dumps(data) + '\n')

    flash('Form submitted successfully!')
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
