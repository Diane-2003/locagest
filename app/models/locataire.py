from datetime import datetime
from app import db


class Locataire(db.Model):
    __tablename__ = "locataires"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150))
    cni = db.Column(db.String(50), unique=True, nullable=False)
    adresse = db.Column(db.String(255))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    locations = db.relationship(
        "Location", backref="locataire", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    @property
    def locations_actives(self):
        return [loc for loc in self.locations if loc.statut == "active"]

    @property
    def nombre_chambres_occupees(self):
        return len(self.locations_actives)

    def __repr__(self):
        return f"<Locataire {self.nom_complet}>"