from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    telephone = db.Column(db.String(20))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    chambres = db.relationship("Chambre", backref="proprietaire", lazy=True)

    def set_password(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def check_password(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)

    def __repr__(self):
        return f"<User {self.email}>"