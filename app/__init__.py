"""
Factory de l'application Flask LocaGest.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from app.config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "warning"

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Enregistrement des blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.chambres import chambres_bp
    from app.routes.locataires import locataires_bp
    from app.routes.locations import locations_bp
    from app.routes.paiements import paiements_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(chambres_bp, url_prefix="/chambres")
    app.register_blueprint(locataires_bp, url_prefix="/locataires")
    app.register_blueprint(locations_bp, url_prefix="/locations")
    app.register_blueprint(paiements_bp, url_prefix="/paiements")

    # Tâche utilitaire accessible dans les templates
    from datetime import datetime
    app.jinja_env.globals["now"] = datetime.utcnow

    return app