# Guide d'installation de Baluchon

Ce guide vous accompagne pas à pas pour installer Baluchon sur un Mac ou un ordinateur Linux, et démarrer avec une base de données vierge. Aucune connaissance technique avancée n'est requise — il suffit de recopier les commandes.

---

## 1. Ce dont vous avez besoin

- Un Mac ou un ordinateur Linux
- **Python 3.8 ou plus** (les développements et tests récents ont été faits avec Python 3.11). Pour vérifier s'il est installé, ouvrez le **Terminal** et tapez :
  ```bash
  python3 --version
  ```
  Si une version s'affiche (ex : `Python 3.11.5`), c'est bon. Sinon, installez Python depuis https://www.python.org/downloads/

---

## 2. Placer le dossier Baluchon

Décompressez l'archive `baluchon.tar.gz` que l'on vous a transmise. Vous obtenez un dossier `baluchon`. Placez-le où vous voulez, par exemple dans votre dossier personnel.

Ouvrez le **Terminal** et déplacez-vous dans ce dossier. Par exemple, s'il est dans votre dossier personnel :

```bash
cd ~/baluchon
```

> 💡 Astuce : vous pouvez taper `cd ` (avec un espace) puis glisser-déposer le dossier depuis le Finder dans la fenêtre du Terminal, et appuyer sur Entrée.

---

## 3. Installation automatique

Lancez le script d'installation :

```bash
./install.sh
```

Ce script fait tout automatiquement :
- crée un environnement isolé pour l'application,
- installe les composants nécessaires,
- génère une configuration sécurisée,
- crée une base de données vierge,
- vous demande de **choisir votre identifiant et votre mot de passe** de connexion.

> Si le terminal répond `permission denied`, donnez les droits d'exécution une fois pour toutes :
> ```bash
> chmod +x install.sh start.sh
> ```
> puis relancez `./install.sh`.

À la fin, vous verrez le message **« Installation terminée ! »**.

---

## 4. Démarrer Baluchon

```bash
./start.sh
```

Vous verrez s'afficher :
```
🎒 Baluchon démarre sur http://localhost:8000
```

Ouvrez votre navigateur et allez à l'adresse **http://localhost:8000**.

Connectez-vous avec l'identifiant et le mot de passe choisis à l'étape 3.

> Pour **arrêter** l'application, revenez dans le Terminal et appuyez sur `Ctrl + C`.

> Pour utiliser un autre port (par exemple si le 8000 est déjà pris) :
> ```bash
> ./start.sh 8001
> ```

---

## 5. Utilisation quotidienne

Chaque fois que vous voulez utiliser Baluchon :

1. Ouvrez le Terminal
2. Déplacez-vous dans le dossier : `cd ~/baluchon`
3. Lancez : `./start.sh`
4. Ouvrez http://localhost:8000 dans le navigateur

C'est tout. Vos données sont enregistrées localement dans le fichier `baluchon.db`, à la racine du dossier de l'application.

---

## 6. Sauvegarder ses données

Toutes vos données tiennent dans deux endroits, à l'intérieur du dossier `baluchon` :
- le fichier **`baluchon.db`** (projets, événements, tâches, infos), à la racine du dossier
- le dossier **`uploads/`** (fichiers que vous avez importés)

Pour faire une sauvegarde, il suffit de copier ces deux éléments ailleurs (disque externe, cloud…). Par exemple :

```bash
cp baluchon.db ~/Desktop/baluchon-sauvegarde.db
cp -r uploads ~/Desktop/baluchon-uploads-sauvegarde
```

> ℹ️ Si votre installation est plus ancienne, la base peut se trouver dans `instance/baluchon.db`. L'emplacement exact est celui indiqué par `DATABASE_URI` dans le fichier `.env` ; en cas de doute, cherchez le fichier avec `ls *.db instance/*.db`.

---

## 7. Mettre à jour Baluchon

> 📘 Pour une migration complète et prudente (test à blanc, vérifications, retour en arrière, liste des fichiers), suivez le **`GUIDE_MIGRATION.md`**. Cette section en est la version courte.

Quand vous recevez une nouvelle version de l'application :

1. **Arrêtez** Baluchon s'il tourne (`Ctrl + C` dans le Terminal).
2. **Sauvegardez** vos données (voir l'étape 6) : le fichier `baluchon.db` et le dossier `uploads/`. C'est la seule précaution indispensable.
3. **Remplacez les fichiers de l'application** par ceux de la nouvelle version. Ne touchez pas à `baluchon.db`, `uploads/`, `.env` ni au dossier `venv/` : ils contiennent vos données et votre configuration.
4. **Relancez** :
   ```bash
   ./start.sh
   ```

La base de données est mise à jour automatiquement au démarrage. Cette mise à jour est **sans danger** : elle ne fait que *ajouter* ce qui manque, ne supprime ni ne modifie aucune de vos données, et ne fait rien si elle a déjà été faite.

Vous verrez, selon le cas, l'un de ces messages :
```
✓ Colonne 'tache.duree_jours' ajoutée (estimation du temps des tâches).   ← la base vient d'être mise à jour
✓ Rien à faire : 'tache.tags' existe déjà (tags des tâches).               ← déjà à jour
```

### Si vous ne démarrez pas avec `./start.sh`

Si vous lancez Baluchon autrement (service, gestionnaire de processus…), lancez la mise à jour de la base **à la main, avant de redémarrer l'application** :

```bash
source venv/bin/activate
python migrer_base.py
```

> ⚠️ Si vous oubliez cette étape, l'application affiche une *Internal Server Error* sur presque toutes les pages, avec dans le Terminal un message du type `no such column: tache.duree_jours` (ou `projet.tags`). Il suffit alors de lancer la commande ci-dessus, puis de redémarrer.

### Que contient cette mise à jour ?

Un seul script, `migrer_base.py`, ajoute toutes les colonnes manquantes. Il ne fait que des *ajouts* (colonnes vides pour les données existantes) :

| Fonctionnalité | Changement de la base |
|---|---|
| Estimation du temps des tâches | colonne `duree_jours` ajoutée à la table `tache` |
| Tags sur les projets | colonne `tags` ajoutée à la table `projet` |
| Tags sur les tâches | colonne `tags` ajoutée à la table `tache` |

Les autres évolutions (statut « Abandonné » des tâches, type d'info « Personne », code couleur, page Infos, export des statistiques…) n'ont **aucun impact sur la base** : rien à migrer.

> L'ancienne commande `python migrer_duree_taches.py` fonctionne toujours : elle lance simplement `migrer_base.py`.

### Revenir en arrière

Si besoin, remettez l'ancienne version des fichiers : elle fonctionne avec la colonne en plus (elle l'ignore). En cas de problème, restaurez votre sauvegarde de `baluchon.db`.

---

## 8. En cas de souci

**« command not found: python3 »** → Python n'est pas installé. Voir l'étape 1.

**« permission denied » en lançant un script** → tapez `chmod +x install.sh start.sh` puis réessayez.

**« Address already in use »** → le port est déjà utilisé. Démarrez sur un autre port : `./start.sh 8001`.

**« Internal Server Error » après une mise à jour, avec `no such column` dans le Terminal** → la base n'a pas été mise à jour. Voir l'étape 7 : `python migrer_base.py`, puis redémarrez.

**J'ai oublié mon mot de passe** → recréez un compte (ou changez le mot de passe d'un compte existant) :
```bash
source venv/bin/activate
python create_admin.py
```

**Réinitialiser complètement (effacer toutes les données)** → supprimez le fichier `baluchon.db` (et vider `uploads/` si vous voulez aussi effacer les fichiers importés), puis relancez :
```bash
source venv/bin/activate
python init_db.py
python create_admin.py
```

---

Bonne utilisation ! 🎒
