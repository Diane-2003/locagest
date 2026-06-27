from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from app import db
from app.models.paiement import Paiement
from app.models.location import Location
from app.forms import PaiementForm
from app.routes.locations import _date_echeance

import app.forms

print(app.forms.__file__) 
paiements_bp = Blueprint("paiements", __name__)


def _choix_mois(paiement):
    import locale
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        pass
    base = date(paiement.mois.year, paiement.mois.month, 1)
    mois_list = []
    for delta in range(-3, 3):
        m = base + relativedelta(months=delta)
        mois_list.append((m.strftime("%Y-%m-%d"), m.strftime("%B %Y").capitalize()))
    return mois_list


@paiements_bp.route("/")
@login_required
def list_paiements():
    filtre = request.args.get("statut", "toutes")
    tous_impayes = Paiement.query.filter(
        Paiement.statut.in_(["en_attente", "en_retard"])
    ).all()
    for p in tous_impayes:
        p.maj_statut_retard()
    db.session.commit()

    query = Paiement.query.join(Location)
    if filtre in ("en_attente", "paye", "en_retard"):
        query = query.filter(Paiement.statut == filtre)
    paiements = query.order_by(Paiement.mois.desc(), Paiement.date_echeance.asc()).all()
    return render_template("paiements/list.html", paiements=paiements, filtre=filtre)


@paiements_bp.route("/<int:paiement_id>/payer", methods=["GET", "POST"])
@login_required
def payer(paiement_id):
    paiement = Paiement.query.get_or_404(paiement_id)
    form = PaiementForm()
    
    form.mois.choices = _choix_mois(paiement)

    if form.validate_on_submit():
        nombre_mois = form.nombre_mois.data
        mois_depart = date.fromisoformat(form.mois.data)
        mode = form.mode_paiement.data

        # Collecter les paiements existants et en créer si nécessaire
        paiements_a_payer = []
        for i in range(nombre_mois):
            mois_cible = mois_depart + relativedelta(months=i)
            mois_cible = date(mois_cible.year, mois_cible.month, 1)

            # Chercher un paiement existant pour ce mois
            p = Paiement.query.filter_by(
                location_id=paiement.location_id,
                mois=mois_cible
            ).first()

            if p and p.statut == "paye":
                flash(f"Le mois {mois_cible.strftime('%B %Y')} est déjà payé.", "warning")
                return render_template(
                    "paiements/list.html",
                    paiements=[paiement], form=form, mode_paiement=True,
                )

            if not p:
                # Créer le paiement s'il n'existe pas encore
                p = Paiement(
                    location_id=paiement.location_id,
                    mois=mois_cible,
                    date_echeance=_date_echeance(mois_cible),
                    montant=paiement.location.chambre.loyer_mensuel,
                    statut="en_attente",
                )
                db.session.add(p)
                db.session.flush() 

            paiements_a_payer.append(p)

        if nombre_mois == 1:
            # Paiement simple
            paiements_a_payer[0].marquer_paye(mode_paiement=mode)
            Paiement.recalculer_statuts_location(paiement.location_id)
            db.session.commit()
            flash("Paiement enregistré.", "success")
            return redirect(url_for("paiements.recu", paiement_id=paiements_a_payer[0].id))
        else:
            # Paiement groupé
            numero_groupe = Paiement.marquer_paye_groupe(paiements_a_payer, mode_paiement=mode)
            Paiement.recalculer_statuts_location(paiement.location_id)
            db.session.commit()
            flash(f"{nombre_mois} mois enregistrés avec succès.", "success")
            return redirect(url_for("paiements.recu_groupe", numero_groupe=numero_groupe))

    form.mois.data = date(paiement.mois.year, paiement.mois.month, 1).strftime("%Y-%m-%d")
    return render_template(
        "paiements/list.html",
        paiements=[paiement], form=form, mode_paiement=True,
    )


@paiements_bp.route("/recu-groupe/<string:numero_groupe>")
@login_required
def recu_groupe(numero_groupe):
    paiements = Paiement.query.filter_by(numero_recu_groupe=numero_groupe).order_by(Paiement.mois.asc()).all()
    if not paiements:
        flash("Reçu introuvable.", "danger")
        return redirect(url_for("paiements.list_paiements"))
    locataire = paiements[0].location.locataire
    chambre = paiements[0].location.chambre
    montant_total = sum(p.montant for p in paiements)
    return render_template(
        "paiements/recu_groupe.html",
        paiements=paiements,
        locataire=locataire,
        chambre=chambre,
        montant_total=montant_total,
        numero_groupe=numero_groupe,
    )


@paiements_bp.route("/<int:paiement_id>/recu")
@login_required
def recu(paiement_id):
    paiement = Paiement.query.get_or_404(paiement_id)
    if paiement.statut != "paye":
        flash("Ce paiement n'a pas encore été réglé.", "warning")
        return redirect(url_for("paiements.list_paiements"))
    # Si ce paiement fait partie d'un groupe, rediriger vers le reçu groupe
    if paiement.numero_recu_groupe:
        return redirect(url_for("paiements.recu_groupe", numero_groupe=paiement.numero_recu_groupe))
    return render_template("paiements/recu.html", paiement=paiement)


@paiements_bp.route("/<int:location_id>/generer-mois-suivant", methods=["POST"])
@login_required
def generer_mois_suivant(location_id):
    location = Location.query.get_or_404(location_id)
    dernier = (
        Paiement.query.filter_by(location_id=location.id)
        .order_by(Paiement.mois.desc())
        .first()
    )
    mois_suivant = (
        date(dernier.mois.year, dernier.mois.month, 1) + relativedelta(months=1)
        if dernier
        else date(date.today().year, date.today().month, 1)
    )
    existe = Paiement.query.filter_by(location_id=location.id, mois=mois_suivant).first()
    if existe:
        flash("Le paiement de ce mois existe déjà.", "warning")
        return redirect(url_for("paiements.list_paiements"))

    p = Paiement(
        location_id=location.id,
        mois=mois_suivant,
        date_echeance=_date_echeance(mois_suivant),
        montant=location.chambre.loyer_mensuel,
        statut="en_attente",
    )
    db.session.add(p)
    db.session.commit()
    flash("Paiement du mois suivant généré.", "success")
    return redirect(url_for("paiements.list_paiements"))