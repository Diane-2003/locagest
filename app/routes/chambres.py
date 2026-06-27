from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models.chambre import Chambre
from app.forms import ChambreForm

chambres_bp = Blueprint("chambres", __name__)


@chambres_bp.route("/")
@login_required
def list_chambres():
    filtre = request.args.get("statut", "toutes")
    query = Chambre.query
    if filtre in ("disponible", "occupee"):
        query = query.filter_by(statut=filtre)
    chambres = query.order_by(Chambre.numero.asc()).all()
    return render_template("chambres/list.html", chambres=chambres, filtre=filtre)


@chambres_bp.route("/ajouter", methods=["GET", "POST"])
@login_required
def ajouter_chambre():
    form = ChambreForm()
    if form.validate_on_submit():
        if Chambre.query.filter_by(numero=form.numero.data).first():
            flash("Une chambre avec ce numéro existe déjà.", "danger")
            return render_template("chambres/form.html", form=form, titre="Ajouter une chambre")

        chambre = Chambre(
            numero=form.numero.data,
            superficie=form.superficie.data,
            loyer_mensuel=form.loyer_mensuel.data,
            description=form.description.data,
            proprietaire_id=current_user.id,
        )
        db.session.add(chambre)
        db.session.commit()
        flash(f"Chambre {chambre.numero} ajoutée avec succès.", "success")
        return redirect(url_for("chambres.list_chambres"))

    return render_template("chambres/form.html", form=form, titre="Ajouter une chambre")


@chambres_bp.route("/<int:chambre_id>/modifier", methods=["GET", "POST"])
@login_required
def modifier_chambre(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)
    form = ChambreForm(obj=chambre)

    if request.method == "GET":
        form.numero.data = chambre.numero
        form.superficie.data = chambre.superficie
        form.loyer_mensuel.data = chambre.loyer_mensuel
        form.description.data = chambre.description

    if form.validate_on_submit():
        doublon = Chambre.query.filter(
            Chambre.numero == form.numero.data, Chambre.id != chambre.id
        ).first()
        if doublon:
            flash("Une autre chambre porte déjà ce numéro.", "danger")
            return render_template("chambres/form.html", form=form, titre="Modifier la chambre", chambre=chambre)

        chambre.numero = form.numero.data
        chambre.superficie = form.superficie.data
        chambre.loyer_mensuel = form.loyer_mensuel.data
        chambre.description = form.description.data
        db.session.commit()
        flash("Chambre modifiée avec succès.", "success")
        return redirect(url_for("chambres.list_chambres"))

    return render_template("chambres/form.html", form=form, titre="Modifier la chambre", chambre=chambre)


@chambres_bp.route("/<int:chambre_id>/supprimer", methods=["POST"])
@login_required
def supprimer_chambre(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)
    if chambre.statut == "occupee":
        flash("Impossible de supprimer une chambre actuellement occupée.", "danger")
        return redirect(url_for("chambres.list_chambres"))

    db.session.delete(chambre)
    db.session.commit()
    flash("Chambre supprimée.", "info")
    return redirect(url_for("chambres.list_chambres"))


@chambres_bp.route("/<int:chambre_id>")
@login_required
def detail_chambre(chambre_id):
    chambre = Chambre.query.get_or_404(chambre_id)
    return render_template("chambres/list.html", chambres=[chambre], filtre="detail")