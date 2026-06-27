from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models.user import User
from app.forms import RegisterForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Cette adresse email est déjà utilisée.", "danger")
            return render_template("auth/register.html", form=form)

        user = User(
            nom=form.nom.data,
            email=form.email.data,
            telephone=form.telephone.data,
        )
        user.set_password(form.mot_de_passe.data)
        db.session.add(user)
        db.session.commit()

        flash("Compte créé avec succès. Vous pouvez vous connecter.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.mot_de_passe.data):
            login_user(user)
            flash(f"Bienvenue, {user.nom} !", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard.index"))
        flash("Email ou mot de passe incorrect.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/")
def root():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))