from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thefame2025'

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'poulaintatiana121@gmail.com'  # Remplacez par votre adresse email
app.config['MAIL_PASSWORD'] = 'rdcwvcwutllababl'     # Remplacez par votre mot de passe ou App Password
app.config['MAIL_DEFAULT_SENDER'] = 'THE FAME Act 2 '


db = SQLAlchemy(app)
mail = Mail(app)


# Import routes (important: après l'initialisation de `app`, `db`, `mail`)
from routes import *

# Créer la base de données dans le bon contexte Flask
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
