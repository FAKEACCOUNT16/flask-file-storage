import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_user_upload_path(username):
    """
    Constructs and returns a secure, user-specific upload path.
    Creates the directory if it doesn't exist.
    """
    base_upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(os.getcwd(), 'uploads'))
    path = os.path.join(base_upload_folder, username)
    os.makedirs(path, exist_ok=True)
    return path

def save_file(file, username):
    """
    Saves the uploaded file to the appropriate user-specific directory.
    Returns the full path to the saved file.
    """
    upload_path = get_user_upload_path(username)
    filename = secure_filename(file.filename)
    full_path = os.path.join(upload_path, filename)
    file.save(full_path)
    return full_path
