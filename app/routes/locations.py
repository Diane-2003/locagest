from datetime import date
from calendar import monthrange
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.models.location import Location
from app.models.locataire import Locataire
from app.models.chambre import Chambre
from app.models.paiement import Paiement
from app.forms import LocationForm

locations_bp = Blueprint("locations", __name__)


def _date_echeance(mois_date, jour_echeance=5):
    """Renvoie la date d'échéance du loyer pour le mois donné (par défaut le 5)."""
    dernier_jour = monthrange(mois_date.year, mois_date.month)[1]
    jour = min(jour_echeance, dernier_jour)
    return date(mois_date.year, mois_date.month, jour)


def generer_paiement_initial(location):
    """Crée le paiement du mois en cours avec le statut 'en_attente'."""
    aujourdhui = date.today()
    debut_mois = date(aujourdhui.year, aujourdhui.month, 1)
    paiement = Paiement(
        location_id=location.id,
        mois=debut_mois,
        date_echeance=_date_echeance(debut_mois),
        montant=location.chambre.loyer_mensuel,
        statut="en_attente",
    )
    db.session.add(paiement)


@locations_bp.route("/")
@login_required
def list_locations():
    locations = Location.query.order_by(Location.date_creation.desc()).all()
    return render_template("locations/list.html", locations=locations)


@locations_bp.route("/ajouter", methods=["GET", "POST"])
@login_required
def ajouter_location():
    form = LocationForm()
    form.locataire_id.choices = [
        (l.id, l.nom_complet) for l in Locataire.query.order_by(Locataire.nom).all()
    ]
    form.chambre_id.choices = [
        (c.id, f"{c.numero} ({c.superficie} m² - {c.loyer_mensuel} FCFA)")
        for c in Chambre.query.filter_by(statut="disponible").order_by(Chambre.numero).all()
    ]

    if not form.chambre_id.choices:
        flash("Aucune chambre disponible actuellement.", "warning")

    if form.validate_on_submit():
        chambre = Chambre.query.get(form.chambre_id.data)
        if not chambre or chambre.statut != "disponible":
            flash("Cette chambre n'est plus disponible.", "danger")
            return redirect(url_for("locations.ajouter_location"))

        location = Location(
            locataire_id=form.locataire_id.data,
            chambre_id=form.chambre_id.data,
            date_debut=form.date_debut.data,
            statut="active",
        )
        db.session.add(location)
        chambre.statut = "occupee"
        db.session.flush()  

        generer_paiement_initial(location)
        db.session.commit()

        flash("Chambre attribuée avec succès. Le premier paiement a été généré.", "success")
        return redirect(url_for("locations.list_locations"))

    return render_template("locations/form.html", form=form, titre="Attribuer une chambre")


@locations_bp.route("/<int:location_id>/resilier", methods=["POST"])
@login_required
def resilier_location(location_id):
    location = Location.query.get_or_404(location_id)
    location.statut = "terminee"
    location.date_fin = date.today()
    db.session.flush()          
    location.chambre.maj_statut()
    db.session.commit()
    flash("Location résiliée. La chambre est de nouveau disponible.", "info")
    return redirect(url_for("locations.list_locations"))