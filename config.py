class Config:
    SECRET_KEY = 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'poulaintatiana121@gmail.com'
    MAIL_PASSWORD = 'rdcwvcwutllababl'
    MAIL_DEFAULT_SENDER = 'poulaintatiana121@gmail.com'