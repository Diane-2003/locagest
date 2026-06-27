from datetime import datetime
from app import db


class Chambre(db.Model):
    __tablename__ = "chambres"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    superficie = db.Column(db.Float, nullable=False)  # en m²
    loyer_mensuel = db.Column(db.Numeric(10, 2), nullable=False)  # FCFA
    description = db.Column(db.Text)
    statut = db.Column(db.String(20), nullable=False, default="disponible")
    # statut possibles : disponible, occupee
    proprietaire_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    locations = db.relationship(
        "Location", backref="chambre", lazy=True, cascade="all, delete-orphan"
    )

    @property
    def est_disponible(self):
        return self.statut == "disponible"

    def maj_statut(self):
        """Recalcule le statut en fonction des locations actives."""
        actives = [l for l in self.locations if l.statut == "active"]
        self.statut = "occupee" if actives else "disponible"

    def __repr__(self):
        return f"<Chambre {self.numero}>"