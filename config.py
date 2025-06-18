import os

class Config:
    # Secret key for session cookies and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

    # SQLAlchemy database URI (default is local SQLite, can be overridden)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload configuration
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max upload size

    # Use environment variable for upload folder if defined, else fallback to local 'uploads' directory
    UPLOAD_FOLDER = os.environ.get(
        'UPLOAD_FOLDER',
        os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    )

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'exe', 'ini', 'py', 'txt', 'bat', 'dll'}
