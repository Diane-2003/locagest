from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required

from app import db
from app.models.chambre import Chambre
from app.models.locataire import Locataire
from app.models.location import Location
from app.models.paiement import Paiement

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Mettre à jour les statuts de retard avant l'affichage
    paiements_en_attente = Paiement.query.filter_by(statut="en_attente").all()
    for p in paiements_en_attente:
        p.maj_statut_retard()
    db.session.commit()

    total_chambres = Chambre.query.count()
    chambres_disponibles = Chambre.query.filter_by(statut="disponible").count()
    chambres_occupees = Chambre.query.filter_by(statut="occupee").count()
    total_locataires = Locataire.query.count()

    paiements_retard = (
        Paiement.query.filter_by(statut="en_retard")
        .join(Location)
        .order_by(Paiement.date_echeance.asc())
        .all()
    )

    paiements_recents = (
        Paiement.query.filter_by(statut="paye")
        .order_by(Paiement.date_paiement.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard/index.html",
        total_chambres=total_chambres,
        chambres_disponibles=chambres_disponibles,
        chambres_occupees=chambres_occupees,
        total_locataires=total_locataires,
        paiements_retard=paiements_retard,
        paiements_recents=paiements_recents,
        aujourdhui=date.today(),
    )