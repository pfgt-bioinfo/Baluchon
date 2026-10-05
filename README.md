# 🎒 Baluchon

**Baluchon** est une application web (Flask) pour suivre ses projets, événements, tâches, fichiers et informations associées — pensée à l'origine pour des projets de bio-informatique, mais utilisable pour tout suivi de projets.

## Fonctionnalités principales

- **Projets** avec statut (en cours, en attente, archivé, abandonné), description, tags (filtrables), avancement (barres tâches et temps) et infos épinglées.
- **Événements** datés et typés, avec pièces jointes et tâches associées. Vue liste ou calendrier.
- **Tâches** avec statut, priorité (matrice d'Eisenhower), date butoir, tags (filtrables) et **durée estimée** (en jours et % de jour). Vues liste, matrice et « Estimer temps ».
- **Infos** : centralisez dossiers, fichiers locaux, fichiers uploadés, liens web et personnes (nom, email, rôle) pour chaque projet, avec code couleur par type et vérification des liens. Une page « Infos » réunit celles de tous les projets.
- **Statistiques** : diagramme de Gantt, avancement des projets et bilan d'activité sur une période, avec colonnes au choix et export CSV (utile pour un bilan annuel).
- **Connexion sécurisée** par identifiant / mot de passe.

## Documentation

- **[GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)** — installer et démarrer l'application, pas à pas.
- **[GUIDE_FONCTIONNALITES.md](GUIDE_FONCTIONNALITES.md)** — comment utiliser Baluchon au quotidien.
- **[GUIDE_MIGRATION.md](GUIDE_MIGRATION.md)** — passer une installation existante à la nouvelle version (base de données, sauvegarde, retour en arrière).

## Installation

Voir le **[GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)** pour la procédure pas à pas.

En résumé (Mac / Linux) :

```bash
./install.sh   # installe tout et crée votre compte
./start.sh     # démarre l'application sur http://localhost:8000
```

## Mise à jour

Pour passer à une nouvelle version (nouvelles fonctionnalités, évolution de la base de données), voir le **[GUIDE_MIGRATION.md](GUIDE_MIGRATION.md)** (version détaillée) ou la section « Mettre à jour Baluchon » du [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md) (version courte). En bref : sauvegardez `baluchon.db` et `uploads/`, remplacez les fichiers de l'application, puis relancez `./start.sh` — la base est mise à jour automatiquement.

## Prérequis

- Python 3.8 ou plus (les développements et tests récents ont été faits avec Python 3.11)
- macOS ou Linux

## Licence

Voir le fichier `LICENSE`.
