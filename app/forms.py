
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, FloatField, DecimalField,
    SelectField, DateField, TextAreaField, SubmitField
)
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from wtforms import (
    StringField, PasswordField, FloatField, DecimalField,
    SelectField, DateField, TextAreaField,
    SubmitField, IntegerField
)

class RegisterForm(FlaskForm):
    nom = StringField("Nom complet", validators=[DataRequired(), Length(max=100)])
    email = StringField("Adresse email", validators=[DataRequired(), Email()])
    telephone = StringField("Téléphone", validators=[Optional(), Length(max=20)])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=6)])
    confirmer_mot_de_passe = PasswordField(
        "Confirmer le mot de passe",
        validators=[DataRequired(), EqualTo("mot_de_passe", message="Les mots de passe ne correspondent pas.")],
    )
    submit = SubmitField("Créer mon compte")


class LoginForm(FlaskForm):
    email = StringField("Adresse email", validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class ChambreForm(FlaskForm):
    numero = StringField("Numéro de chambre", validators=[DataRequired(), Length(max=20)])
    superficie = FloatField("Superficie (m²)", validators=[DataRequired(), NumberRange(min=1)])
    loyer_mensuel = DecimalField("Loyer mensuel (FCFA)", validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Enregistrer")


class LocataireForm(FlaskForm):
    nom = StringField("Nom", validators=[DataRequired(), Length(max=100)])
    prenom = StringField("Prénom", validators=[DataRequired(), Length(max=100)])
    telephone = StringField("Téléphone", validators=[DataRequired(), Length(max=20)])
    email = StringField("Email", validators=[Optional(), Email()])
    cni = StringField("N° CNI", validators=[DataRequired(), Length(max=50)])
    adresse = StringField("Adresse", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Enregistrer")


class LocationForm(FlaskForm):
    locataire_id = SelectField("Locataire", coerce=int, validators=[DataRequired()])
    chambre_id = SelectField("Chambre disponible", coerce=int, validators=[DataRequired()])
    date_debut = DateField("Date de début", validators=[DataRequired()])
    submit = SubmitField("Attribuer la chambre")


class PaiementForm(FlaskForm):
    mois = SelectField(
        "Mois concerné",
        choices=[],
        validators=[DataRequired()]
    )

    nombre_mois = IntegerField(
        "Nombre de mois",
        default=1,
        validators=[
            DataRequired(),
            NumberRange(min=1)
        ]
    )

    mode_paiement = SelectField(
        "Mode de paiement",
        choices=[
            ("especes", "Espèces"),
            ("orange_money", "Orange Money"),
            ("mtn_momo", "MTN Mobile Money"),
            ("virement", "Virement bancaire"),
        ],
        validators=[DataRequired()]
    )

    submit = SubmitField("Confirmer le paiement")