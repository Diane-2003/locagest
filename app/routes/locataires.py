from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.models.locataire import Locataire
from app.models.paiement import Paiement
from app.models.location import Location
from app.forms import LocataireForm

locataires_bp = Blueprint("locataires", __name__)


@locataires_bp.route("/")
@login_required
def list_locataires():
    locataires = Locataire.query.order_by(Locataire.nom.asc()).all()
    return render_template("locataires/list.html", locataires=locataires)


@locataires_bp.route("/ajouter", methods=["GET", "POST"])
@login_required
def ajouter_locataire():
    form = LocataireForm()
    if form.validate_on_submit():
        if Locataire.query.filter_by(cni=form.cni.data).first():
            flash("Un locataire avec ce numéro de CNI existe déjà.", "danger")
            return render_template("locataires/form.html", form=form, titre="Ajouter un locataire")

        locataire = Locataire(
            nom=form.nom.data,
            prenom=form.prenom.data,
            telephone=form.telephone.data,
            email=form.email.data,
            cni=form.cni.data,
            adresse=form.adresse.data,
        )
        db.session.add(locataire)
        db.session.commit()
        flash(f"Locataire {locataire.nom_complet} ajouté avec succès.", "success")
        return redirect(url_for("locataires.list_locataires"))

    return render_template("locataires/form.html", form=form, titre="Ajouter un locataire")


@locataires_bp.route("/<int:locataire_id>/modifier", methods=["GET", "POST"])
@login_required
def modifier_locataire(locataire_id):
    locataire = Locataire.query.get_or_404(locataire_id)
    form = LocataireForm(obj=locataire)

    if form.validate_on_submit():
        doublon = Locataire.query.filter(
            Locataire.cni == form.cni.data, Locataire.id != locataire.id
        ).first()
        if doublon:
            flash("Un autre locataire utilise déjà ce numéro de CNI.", "danger")
            return render_template("locataires/form.html", form=form, titre="Modifier le locataire", locataire=locataire)

        locataire.nom = form.nom.data
        locataire.prenom = form.prenom.data
        locataire.telephone = form.telephone.data
        locataire.email = form.email.data
        locataire.cni = form.cni.data
        locataire.adresse = form.adresse.data
        db.session.commit()
        flash("Locataire modifié avec succès.", "success")
        return redirect(url_for("locataires.list_locataires"))

    return render_template("locataires/form.html", form=form, titre="Modifier le locataire", locataire=locataire)


@locataires_bp.route("/<int:locataire_id>/supprimer", methods=["POST"])
@login_required
def supprimer_locataire(locataire_id):
    locataire = Locataire.query.get_or_404(locataire_id)
    if locataire.locations_actives:
        flash("Impossible de supprimer un locataire ayant une location active.", "danger")
        return redirect(url_for("locataires.list_locataires"))

    db.session.delete(locataire)
    db.session.commit()
    flash("Locataire supprimé.", "info")
    return redirect(url_for("locataires.list_locataires"))


@locataires_bp.route("/<int:locataire_id>/historique")
@login_required
def historique_locataire(locataire_id):
    locataire = Locataire.query.get_or_404(locataire_id)
    location_ids = [l.id for l in locataire.locations]
    paiements = (
        Paiement.query.filter(Paiement.location_id.in_(location_ids))
        .order_by(Paiement.mois.desc())
        .all()
        if location_ids
        else []
    )
    return render_template(
        "locataires/list.html",
        locataires=[locataire],
        historique=paiements,
        mode_historique=True,
    )