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

## Prérequis

- **Python 3.10+** installé (vérifier avec `python --version` ou `py --version`)
- **MySQL** accessible (via WAMP, XAMPP, ou une installation MySQL autonome)
- Un terminal (PowerShell, CMD, ou terminal intégré de VS Code)

## 1. Installation des dépendances

Ouvre un terminal dans le dossier `LocaGest/`, puis :

### Sous Windows (PowerShell)
```bash
cd LocaGest
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Sous Linux / macOS
```bash
cd LocaGest
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Création de la base de données MySQL
## Base de données MySQL

1. Créer la base en executant la ligne de commande suivante:
   ```bash
   mysql -u root -p < schema.sql
   ```


## 3. Lancement de l'application

```bash
python run.py
```

Application disponible sur http://localhost:5000

<!-- Compte test:
login: apoussie@gmail.com
mot de passe: Diane123 -->