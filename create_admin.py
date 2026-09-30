"""
Crée (ou met à jour) le compte unique de connexion à Baluchon.
À exécuter après la migration, avant le premier lancement avec gunicorn.

Usage :
    python create_admin.py           # create an account or change its password
    python create_admin.py --list    # print existing usernames, one per line
"""
import getpass
import sys
from app import app
from models import db, User

def list_users():
    with app.app_context():
        for user in User.query.order_by(User.username).all():
            print(user.username)

def main():
    with app.app_context():
        username = input("Identifiant souhaité : ").strip()
        if not username:
            print("Identifiant vide, abandon.")
            return

        password = getpass.getpass("Mot de passe : ")
        password2 = getpass.getpass("Confirmer le mot de passe : ")
        if password != password2:
            print("Les mots de passe ne correspondent pas. Abandon.")
            return
        if len(password) < 6:
            print("Le mot de passe doit faire au moins 6 caractères.")
            return

        user = User.query.filter_by(username=username).first()
        if user:
            user.set_password(password)
            db.session.commit()
            print(f"✓ Mot de passe mis à jour pour '{username}'.")
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"✓ Compte '{username}' créé avec succès.")

if __name__ == '__main__':
    if '--list' in sys.argv[1:]:
        list_users()
    else:
        main()
