# Toutes les routes Flask ici (accueil, admin, etc.)
from flask import render_template, request, redirect, url_for, flash, session
from app import app, db, mail
from models import Participant
from flask_mail import Message
import qrcode
import os

    
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'thefame2025'
QR_FOLDER = 'qr_codes'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        total_inscrits = Participant.query.count()
        quota = 156
        if total_inscrits >= quota:
            flash("Les inscriptions sont closes.")
            return redirect(url_for("index"))

        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]

        if Participant.query.filter_by(email=email).first():
            flash("Cet email est déjà inscrit.")
            return redirect(url_for("index"))

        participant = Participant(nom=nom, prenom=prenom, email=email)

        # Générer QR code
        qr_data = f"ID:{participant.id}, Nom:{nom}, Prénom:{prenom}"
        img = qrcode.make(qr_data)
        qr_path = os.path.join(QR_FOLDER, f"{email}.png")
        if not os.path.exists('qr_codes'):
            os.makedirs('qr_codes')
        img.save(qr_path)
        participant.qr_code_path = qr_path

        db.session.add(participant)
        db.session.commit()

        # Envoyer l'email
        send_confirmation_email(participant, qr_path)

        flash("Réservation enregistrée ! Vérifie ton mail.")
        return redirect(url_for("index"))

    return render_template("index.html")


def send_confirmation_email(participant, qr_path):
    msg = Message("Confirmation de ta réservation – THE FAME Act 2", recipients=[participant.email])
    msg.html = render_template("email_template.html", participant=participant)
    with open(qr_path, "rb") as f:
        msg.attach("qr_code.png", "image/png", f.read())
    mail.send(msg)


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Identifiants invalides")
    return render_template("admin_login.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    participants = Participant.query.all()
    total = len(participants)
    quota = 155
    return render_template("admin_dashboard.html", participants=participants, total=total, remaining=quota - total)
