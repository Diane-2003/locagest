from datetime import datetime
from app import db


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    locataire_id = db.Column(db.Integer, db.ForeignKey("locataires.id"), nullable=False)
    chambre_id = db.Column(db.Integer, db.ForeignKey("chambres.id"), nullable=False)
    date_debut = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_fin = db.Column(db.Date, nullable=True)
    statut = db.Column(db.String(20), nullable=False, default="active")
    # statut possibles : active, terminee
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    paiements = db.relationship(
        "Paiement", backref="location", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Location locataire={self.locataire_id} chambre={self.chambre_id}>"