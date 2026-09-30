"""
Initialise une base de données Baluchon vierge avec toutes les tables.
À lancer une seule fois, à la première installation.

Usage :
    python init_db.py              # create missing tables
    python init_db.py --no-hint    # same, without the create_admin.py hint
"""
import sys
from app import app
from models import db, User

def main():
    with app.app_context():
        db.create_all()
        print("✅ Base de données initialisée : toutes les tables ont été créées.")
        # the hint is only useful when no account exists yet
        if '--no-hint' not in sys.argv[1:] and User.query.first() is None:
            print("   Vous pouvez maintenant créer votre compte avec : python create_admin.py")

if __name__ == '__main__':
    main()
