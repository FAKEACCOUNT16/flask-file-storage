from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, send_file
from flask_login import login_required, current_user
from app.utils.file_helpers import allowed_file, save_file
from app import db
from app.models import File
from datetime import datetime  # ✅ Import datetime
import os

dashboard_bp = Blueprint('routes', __name__)

@dashboard_bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard_view():
    if request.method == 'POST':
        print("POST request received ✅")  # Debug line
        file = request.files['file']
        if file and allowed_file(file.filename):
            filepath = save_file(file, current_user.username)
            new_file = File(
                filename=file.filename,
                filepath=filepath,
                upload_time=datetime.utcnow(),  # ✅ Set the correct upload_time
                user_id=current_user.id
            )
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('routes.dashboard_view'))
        else:
            flash('Invalid file type.', 'danger')

    files = File.query.filter_by(user_id=current_user.id).order_by(File.upload_time.desc()).all()
    return render_template('dashboard.html', username=current_user.username, files=files)


@dashboard_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:
        abort(403)  # Forbidden

    try:
        if os.path.exists(file.filepath):
            os.remove(file.filepath)
        db.session.delete(file)
        db.session.commit()
        flash('File deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'danger')

    return redirect(url_for('routes.dashboard_view'))

@dashboard_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)

    # Check if the file belongs to the current user
    if file.user_id != current_user.id:
        abort(403)  # Forbidden

    # Check if the file exists on disk
    if not os.path.exists(file.filepath):
        flash('File not found on server.', 'danger')
        return redirect(url_for('routes.dashboard_view'))

    # Serve file securely
    return send_file(
        file.filepath,
        as_attachment=True,
        download_name=file.filename
    )