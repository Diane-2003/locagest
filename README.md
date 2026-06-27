# LocaGest — Gestion de Location de Chambres

Application Flask + MySQL pour la gestion de location des chambres .

## Fonctionnalités
1. Enregistrement des locataires et des chambres (numéro, superficie, loyer mensuel)
2. Suivi des paiements mensuels avec indication des retards
3. Visualisation des chambres disponibles / occupées
4. Génération de reçus de loyer imprimables
5. Alertes pour les loyers en retard (date d'échéance dépassée)
6. Historique complet des paiements par locataire
7. Authentification du propriétaire (inscription / connexion)
8. Un locataire peut louer plusieurs chambres simultanément

## Installation

```bash
cd LocaGest
python -m venv venv
source venv/bin/activate        ou venv\Scripts\activate sur Windows
pip install -r requirements.txt
```

## Base de données MySQL

1. Créer la base (ou laisser Flask-Migrate le faire) :
   ```bash
   mysql -u root -p < schema.sql
   ```


## Lancement

```bash
python run.py
```

Application disponible sur http://localhost:5000

<!-- Compte test:
login: apoussie@gmail.com
mot de passe: Diane123 -->