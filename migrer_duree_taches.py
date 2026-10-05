"""Ancien nom du script de mise à jour de la base : fait maintenant la même chose que `python migrer_base.py`
(toutes les colonnes manquantes sont ajoutées). Conservé pour que les anciennes commandes continuent de fonctionner."""
from migrer_base import main

if __name__ == '__main__':
    main()
