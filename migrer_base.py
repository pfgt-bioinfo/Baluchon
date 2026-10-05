"""
Met la base de données à jour : ajoute les colonnes qui manquent, sans toucher aux données existantes.

Sans danger : ne fait rien pour une colonne déjà présente, ne supprime ni ne modifie jamais rien.
À lancer après une mise à jour du code, AVANT de redémarrer Baluchon (start.sh le fait automatiquement).

Usage :
    python migrer_base.py

Conseil : copiez d'abord votre fichier .db (ex : cp baluchon.db baluchon.db.bak).
"""
from sqlalchemy import inspect, text
from app import app
from models import db

# (table, colonne, type SQL, à quoi ça sert) — à compléter à chaque évolution de la base
COLONNES_A_AJOUTER = [
    ('tache', 'duree_jours', 'FLOAT', "estimation du temps des tâches"),
    ('projet', 'tags', 'TEXT', "tags des projets"),
    ('tache', 'tags', 'TEXT', "tags des tâches"),
]

def main():
    with app.app_context():
        inspecteur = inspect(db.engine)
        for table, colonne, type_sql, role in COLONNES_A_AJOUTER:
            if not inspecteur.has_table(table):
                print("· Table '%s' absente : base vierge, lancez plutôt python init_db.py." % table)
                continue
            if colonne in [c['name'] for c in inspecteur.get_columns(table)]:
                print("✓ Rien à faire : '%s.%s' existe déjà (%s)." % (table, colonne, role))
                continue
            db.session.execute(text('ALTER TABLE %s ADD COLUMN %s %s' % (table, colonne, type_sql)))
            db.session.commit()
            print("✓ Colonne '%s.%s' ajoutée (%s)." % (table, colonne, role))

if __name__ == '__main__':
    main()
