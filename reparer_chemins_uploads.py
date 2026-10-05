"""
Répare les chemins des fichiers uploadés après avoir copié la base et le dossier `uploads/` dans un autre dossier.

Pourquoi : Baluchon enregistre, pour chaque fichier uploadé, son chemin COMPLET sur le disque
(ex : /ancien/dossier/uploads/projet_3/liens/rapport.pdf). Si vous reprenez la base ailleurs, ces chemins
pointent vers l'ancien emplacement et les fichiers ne s'ouvrent plus. Ce script les réécrit pour qu'ils
pointent vers le dossier `uploads/` de l'application actuelle.

Sans danger : par défaut c'est une SIMULATION (rien n'est modifié). Ne touche qu'aux fichiers uploadés,
et seulement si le fichier existe bien dans le dossier `uploads/` actuel. Peut être relancé sans risque.

Usage :
    python reparer_chemins_uploads.py              # simulation : affiche ce qui serait corrigé
    python reparer_chemins_uploads.py --appliquer  # écrit les corrections dans la base
"""
import os
import sys
from app import app
from models import db, LienProjet

MARQUEUR = '/uploads/'

def nouveau_chemin(ancien, dossier_uploads):
    """/ancien/dossier/uploads/projet_3/liens/a.pdf -> <dossier_uploads>/projet_3/liens/a.pdf (None si pas de marqueur)."""
    normalise = (ancien or '').replace('\\', '/')
    i = normalise.rfind(MARQUEUR)
    if i < 0:
        return None
    reste = [morceau for morceau in normalise[i + len(MARQUEUR):].split('/') if morceau]
    return os.path.join(dossier_uploads, *reste) if reste else None

def main():
    appliquer = '--appliquer' in sys.argv
    with app.app_context():
        dossier = os.path.abspath(app.config['UPLOAD_FOLDER'])
        liens = LienProjet.query.filter_by(type='upload').all()
        deja_bons, a_corriger, introuvables = 0, [], []
        for lien in liens:
            cible = nouveau_chemin(lien.valeur, dossier)
            if lien.valeur and os.path.abspath(lien.valeur) == (os.path.abspath(cible) if cible else None) and os.path.exists(lien.valeur):
                deja_bons += 1
            elif cible and os.path.exists(cible):
                a_corriger.append((lien, cible))
            else:
                introuvables.append(lien)

        print("Dossier uploads de cette installation : %s" % dossier)
        print("Fichiers uploadés en base : %d" % len(liens))
        print("  ✓ déjà corrects            : %d" % deja_bons)
        print("  → à corriger               : %d" % len(a_corriger))
        print("  ✗ introuvables dans uploads/ : %d" % len(introuvables))
        for lien, cible in a_corriger[:10]:
            print("      #%d  %s\n        -> %s" % (lien.id, lien.valeur, cible))
        if len(a_corriger) > 10:
            print("      … et %d autres" % (len(a_corriger) - 10))
        for lien in introuvables[:10]:
            print("      MANQUANT #%d  %s  (« %s »)" % (lien.id, lien.valeur, lien.intitule))
        if introuvables:
            print("  → Les fichiers manquants n'ont pas été copiés dans uploads/ : recopiez le dossier uploads/ complet de l'ancienne installation.")

        if not a_corriger:
            print("Rien à corriger.")
            return
        if not appliquer:
            print("\nSimulation : rien n'a été modifié. Pour appliquer : python reparer_chemins_uploads.py --appliquer")
            return
        for lien, cible in a_corriger:
            lien.valeur = cible
        db.session.commit()
        print("\n✓ %d chemin(s) corrigé(s)." % len(a_corriger))

if __name__ == '__main__':
    main()
