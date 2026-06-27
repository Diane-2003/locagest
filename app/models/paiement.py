from datetime import datetime, date
from app import db


class Paiement(db.Model):
    __tablename__ = "paiements"

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"), nullable=False)
    mois = db.Column(db.Date, nullable=False)
    date_echeance = db.Column(db.Date, nullable=False)
    montant = db.Column(db.Numeric(10, 2), nullable=False)
    date_paiement = db.Column(db.Date, nullable=True)
    statut = db.Column(db.String(20), nullable=False, default="en_attente")
    mode_paiement = db.Column(db.String(50), nullable=True)
    numero_recu = db.Column(db.String(30), unique=True, nullable=True)
    # Reçu groupé : tous les mois payés ensemble partagent le même numéro
    numero_recu_groupe = db.Column(db.String(30), nullable=True, index=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def maj_statut_retard(self):
        if self.statut == "en_attente" and self.date_echeance < date.today():
            self.statut = "en_retard"

    @property
    def est_en_retard(self):
        return self.statut == "en_retard" or (
            self.statut == "en_attente" and self.date_echeance < date.today()
        )

    def marquer_paye(self, mode_paiement="especes"):
        """Paiement simple d'un seul mois."""
        self.statut = "paye"
        self.date_paiement = date.today()
        self.mode_paiement = mode_paiement
        if not self.numero_recu:
            self.numero_recu = f"RECU-{self.location_id}-{self.id}-{date.today().strftime('%Y%m%d')}"

    @staticmethod
    def marquer_paye_groupe(paiements, mode_paiement="especes"):
        """
        Marque plusieurs paiements comme payés avec un reçu groupé commun.
        Retourne le numéro de reçu groupe généré.
        """
        aujourd_hui = date.today()
        # Numéro groupe basé sur le premier paiement de la liste
        premier = paiements[0]
        numero_groupe = f"RECU-G-{premier.location_id}-{premier.id}-{aujourd_hui.strftime('%Y%m%d')}"

        for p in paiements:
            p.statut = "paye"
            p.date_paiement = aujourd_hui
            p.mode_paiement = mode_paiement
            p.numero_recu_groupe = numero_groupe
            if not p.numero_recu:
                p.numero_recu = f"RECU-{p.location_id}-{p.id}-{aujourd_hui.strftime('%Y%m%d')}"

        return numero_groupe

    @staticmethod
    def recalculer_statuts_location(location_id):
        """Recalcule les statuts de tous les mois non payés d'une location."""
        aujourd_hui = date.today()
        impayes = Paiement.query.filter(
            Paiement.location_id == location_id,
            Paiement.statut.in_(["en_attente", "en_retard"])
        ).all()
        for p in impayes:
            if p.date_echeance < aujourd_hui:
                p.statut = "en_retard"
            else:
                p.statut = "en_attente"

    def __repr__(self):
        return f"<Paiement location={self.location_id} mois={self.mois} statut={self.statut}>"