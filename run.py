"""
Point d'entrée de l'application LocaGest.
Lancement : python run.py
"""
from app import create_app, db
from app.models.user import User
from app.models.locataire import Locataire
from app.models.chambre import Chambre
from app.models.location import Location
from app.models.paiement import Paiement

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Locataire": Locataire,
        "Chambre": Chambre,
        "Location": Location,
        "Paiement": Paiement,
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)