# Guide de migration de Baluchon

Ce guide explique comment **passer une installation existante de Baluchon à la nouvelle version** sans perdre de données : sauvegarde, mise à jour de la base, vérifications, et retour en arrière si besoin.

Il s'adresse à la personne qui déploie la mise à jour (sur le Mac/serveur où Baluchon tourne réellement). Pour une première installation, voir plutôt `GUIDE_INSTALLATION.md`.

---

## En bref

1. **Sauvegardez** `baluchon.db` et le dossier `uploads/`.
2. **Remplacez les fichiers** de l'application (liste en annexe), sans toucher à `baluchon.db`, `uploads/`, `.env` ni `venv/`.
3. **Lancez `./start.sh`** : la base est mise à jour automatiquement (sinon : `python migrer_base.py`, puis redémarrer).
4. **Vérifiez** (section 5).

La mise à jour de la base **ajoute seulement trois colonnes vides**. Elle ne modifie ni ne supprime aucune donnée, et peut être relancée sans risque.

---

## 1. Ce qui change

### Pour les utilisateurs

| Domaine | Nouveauté |
|---|---|
| **Menu** | « Fichiers » devient **« Infos »** : toutes les infos de tous les projets, filtrables par projet et par type. L'ancienne adresse `/fichiers` redirige vers cette page. |
| **Infos** | Nouveau type **Personne** (nom, email, rôle) ; fichiers uploadés de nouveau proposés dans « Ajouter une info » ; **code couleur** par type (local, uploadé, web, personne) ; icône œil sur les fichiers uploadés ; textes d'exemple adaptés au type. |
| **Tâches** | **Durée estimée** (jours et % de jour), vue **« Estimer temps »**, statut **« Abandonné »**, **tags**. Dans la liste, priorité et durée se modifient désormais par le crayon. |
| **Projets** | **Tags** filtrables, bloc **Avancement** (barres tâches et temps) sur le tableau de bord. |
| **Statistiques** | Avancement des projets, colonnes % tâches / % temps, **colonnes au choix** et **export CSV**. |
| **Divers** | Les boutons « Ouvrir le dossier / fichier » affichent un message clair s'ils ne peuvent pas agir (ils ne fonctionnent que si Baluchon tourne sur l'ordinateur de l'utilisateur). |

Le détail d'usage est dans `GUIDE_FONCTIONNALITES.md`.

### Pour la base de données

Trois colonnes **ajoutées**, toutes vides au départ pour les données existantes :

| Table | Colonne | Contenu | Pour quelle fonctionnalité |
|---|---|---|---|
| `tache` | `duree_jours` | nombre (ex : 2.5 = 2 j + 50 %) | durée estimée des tâches |
| `projet` | `tags` | texte, tags séparés par des virgules | tags des projets |
| `tache` | `tags` | texte, tags séparés par des virgules | tags des tâches |

Rien d'autre n'est modifié : aucune table créée, supprimée ou renommée ; aucune donnée déplacée. Les autres nouveautés (type « Personne », statut « Abandonné », code couleur…) n'ont aucun impact sur la structure de la base.

### Ce qui ne change pas

- `requirements.txt` : **identique** — pas de `pip install` à refaire.
- `.env` et `install.sh` : inchangés.
- Vos fichiers uploadés et vos identifiants de connexion.

---

## 2. Avant de commencer

### 2.1 Vérifier la version de Python

Baluchon a été développé et testé avec **Python 3.11**. Si votre serveur utilise une version plus ancienne (par exemple 3.7), le code a été vérifié *statiquement* (syntaxe et dépendances compatibles), mais **n'a pas été exécuté** sur cette version. Faites donc ce test, **sans risque pour vos données** (il n'ouvre pas la base) :

```bash
cd ~/baluchon        # le dossier de l'application, avec les NOUVEAUX fichiers
python3 -m venv /tmp/test-baluchon
/tmp/test-baluchon/bin/pip install -r requirements.txt
/tmp/test-baluchon/bin/python -c "import app; print('import ok')"
```

Si `import ok` s'affiche, l'application se charge correctement avec votre Python. Supprimez ensuite `/tmp/test-baluchon`.

### 2.2 Localiser la base

Le fichier de base de données est indiqué par `DATABASE_URI` dans le fichier `.env`. Avec la configuration par défaut (`sqlite:///baluchon.db`), c'est le fichier `baluchon.db` **à la racine du dossier de l'application** (sur d'anciennes installations, parfois `instance/baluchon.db`).

```bash
ls *.db instance/*.db 2>/dev/null
grep DATABASE_URI .env
```

### 2.3 Sauvegarder

```bash
cp baluchon.db baluchon.db.avant-migration
cp -r uploads uploads.avant-migration
```

(Adaptez le nom si votre base est ailleurs.) **Ne passez pas à la suite sans cette copie.**

---

## 3. Test à blanc sur une copie (recommandé)

Pour voir ce que fait la migration **sans toucher à la vraie base**, lancez-la sur une copie. `DATABASE_URI` passé en ligne de commande prend le dessus sur le `.env`. Le chemin doit être **absolu**, avec **quatre barres** après `sqlite:`.

```bash
cp baluchon.db /tmp/copie-test.db
DATABASE_URI=sqlite:////tmp/copie-test.db python migrer_base.py
```

Résultat attendu sur une base à migrer :

```
✓ Colonne 'tache.duree_jours' ajoutée (estimation du temps des tâches).
✓ Colonne 'projet.tags' ajoutée (tags des projets).
✓ Colonne 'tache.tags' ajoutée (tags des tâches).
```

Vous pouvez même démarrer l'application sur cette copie pour la parcourir : `DATABASE_URI=sqlite:////tmp/copie-test.db ./start.sh 8001`. Supprimez la copie ensuite.

---

## 4. Migration

1. **Arrêtez** Baluchon s'il tourne (`Ctrl + C` dans le Terminal où il a été lancé, ou arrêt du service).
2. **Remplacez les fichiers** de l'application par ceux de la nouvelle version (annexe A). **Conservez** `baluchon.db`, `uploads/`, `.env` et `venv/`.
3. **Démarrez** :
   ```bash
   ./start.sh
   ```
   (Si vous reprenez la base dans un **autre dossier** que l'ancienne installation, lisez d'abord l'annexe C.)
   `start.sh` met la base à jour avant de lancer l'application et affiche le résultat de la migration (voir ci-dessus).

   > Si vous ne démarrez pas avec `./start.sh` (service, gestionnaire de processus…), lancez la migration **à la main avant de redémarrer** :
   > ```bash
   > source venv/bin/activate
   > python migrer_base.py
   > ```

Un deuxième passage affiche simplement `✓ Rien à faire : … existe déjà` pour chaque colonne : c'est normal et sans danger.

---

## 5. Vérifier que tout est en ordre

**Dans le navigateur** (connectez-vous avec vos identifiants habituels) :

- [ ] La page d'accueil s'affiche et vos projets, tâches et événements sont toujours là.
- [ ] Le menu du haut propose **Infos** (et plus « Fichiers »).
- [ ] Sur un projet : le formulaire « Éditer » contient un champ **Tags**, et le tableau de bord affiche un bloc **Avancement**.
- [ ] Sur la page **Tâches** : le bouton **Estimer temps** s'ouvre, et le crayon d'une tâche propose durée, tags et statut « Abandonné ».
- [ ] Vos fichiers uploadés s'ouvrent toujours (page Infos, filtre « Fichier uploadé », icône œil).

**Côté base** (sans outil particulier, avec Python seul) :

```bash
source venv/bin/activate
python -c "
import sqlite3
c = sqlite3.connect('baluchon.db')
for t, col in [('tache','duree_jours'), ('projet','tags'), ('tache','tags')]:
    print(t + '.' + col, 'OK' if col in [r[1] for r in c.execute('pragma table_info(' + t + ')')] else 'MANQUANT')
print('projets:', c.execute('select count(*) from projet').fetchone()[0], '| tâches:', c.execute('select count(*) from tache').fetchone()[0])"
```

Les trois colonnes doivent afficher `OK`, et les nombres de projets et de tâches doivent être **identiques à ceux d'avant la migration**.

---

## 6. Revenir en arrière

### Option A — Remettre l'ancien code, garder la base migrée (le plus simple)

Remettez les fichiers de l'ancienne version et redémarrez. **L'ancien code fonctionne avec la base migrée** : il ignore simplement les colonnes en plus (testé : pages et écritures normales). Vos données ne sont pas touchées.

À savoir : ce que vous avez saisi avec les nouvelles fonctions (durées, tags, personnes, tâches abandonnées) reste dans la base mais n'est plus géré par l'ancienne version. En particulier, les tâches « abandonnées » y réapparaissent comme des tâches ouvertes, et les infos « Personne » s'affichent sans icône dédiée.

### Option B — Tout restaurer (base d'avant migration)

```bash
cp baluchon.db.avant-migration baluchon.db
```

et remettez l'ancien code. **Attention : tout ce qui a été saisi dans Baluchon depuis la sauvegarde est perdu** (nouveaux projets, tâches, événements, uploads). Réservez cette option au cas où la base elle-même poserait problème.

---

## 7. Problèmes courants

| Symptôme | Cause et solution |
|---|---|
| **« Internal Server Error »** sur presque toutes les pages, et dans le Terminal `no such column: tache.duree_jours` (ou `projet.tags`, `tache.tags`) | Le nouveau code tourne sur une base **non migrée**. Lancez `python migrer_base.py`, puis redémarrez. |
| `attempt to write a readonly database` pendant la migration | L'utilisateur qui lance la commande n'a pas le droit d'écrire dans le fichier `.db` ni dans son dossier. Vérifiez les permissions (`ls -l baluchon.db`). |
| `· Table 'tache' absente : base vierge, lancez plutôt python init_db.py.` | La base ne contient encore aucune table : lancez `python init_db.py` (installation neuve), pas la migration. |
| La migration annonce `✓ Rien à faire` partout, mais l'erreur persiste | Vous migrez un **autre fichier** que celui utilisé par l'application. Comparez `DATABASE_URI` dans `.env` avec le fichier que vous avez sauvegardé/migré (voir 2.2). |
| `permission denied` en lançant `./start.sh` | `chmod +x start.sh install.sh`, puis relancez. |
| La page « Infos » ou « Estimer temps » reste introuvable (404) après la mise à jour | Le serveur tourne encore avec l'**ancien code** : arrêtez-le complètement et redémarrez. |

---

## Annexe A — Fichiers à déployer

Par rapport à la version de départ (commit `b9064bc`, « Ajout du guide des fonctionnalités »).

**Modifiés**
- Code : `app.py`, `models.py`, `start.sh`
- Modèles de pages (`templates/`) : `base.html`, `macros.html`, `ajouter_projet.html`, `editer_projet.html`, `editer_tache.html`, `editer_lien.html`, `matrice.html`, `projet_dashboard.html`, `stats.html`, `taches.html`, `tous_les_projets.html`, `toutes_les_infos.html`
- Documentation : `README.md`, `GUIDE_INSTALLATION.md`, `GUIDE_FONCTIONNALITES.md`

**Nouveaux**
- Migration : `migrer_base.py` (et `migrer_duree_taches.py`, ancien nom conservé : il lance simplement `migrer_base.py`), `reparer_chemins_uploads.py` (seulement si vous déplacez l'installation, voir l'annexe C)
- Modèles de pages (`templates/`) : `temps.html`, `infos_globales.html`, `_ligne_info.html`, `_infos_script.html`
- Ce guide : `GUIDE_MIGRATION.md`

**Supprimé**
- `templates/vue_globale_fichiers.html` (remplacé par la page Infos ; le laisser en place est sans conséquence)

**À ne pas toucher** : `baluchon.db`, `uploads/`, `.env`, `venv/`.

---

## Annexe B — Pour les développeurs : ajouter une future migration

Toute évolution qui ajoute une colonne se déclare dans la liste `COLONNES_A_AJOUTER` de `migrer_base.py` :

```python
COLONNES_A_AJOUTER = [
    ('tache', 'duree_jours', 'FLOAT', "estimation du temps des tâches"),
    ('projet', 'tags', 'TEXT', "tags des projets"),
    ('tache', 'tags', 'TEXT', "tags des tâches"),
    # ('table', 'nouvelle_colonne', 'TYPE SQL', "à quoi ça sert"),
]
```

Règles pour que la migration reste simple et sûre :
- **Ajouter, jamais supprimer ni renommer** : une colonne ajoutée et facultative (`NULL` par défaut) n'empêche pas l'ancien code de fonctionner, donc le retour en arrière reste possible.
- Déclarer aussi la colonne dans `models.py` : les installations neuves la reçoivent directement via `init_db.py`.
- **Tester d'abord sur une copie** d'une vraie base (section 3), et vérifier que le nombre de lignes de chaque table est inchangé.
- Compléter le tableau de la section 1 et la liste de l'annexe A.

Une nouvelle *table* (et non une colonne) se crée avec `db.create_all()` — appelé par `init_db.py` — qui ne touche pas aux tables existantes ; seules les modifications de tables déjà présentes passent par `migrer_base.py`. Il n'y a pas d'outil de migration plus lourd (type Flask-Migrate) dans ce projet.

---

## Annexe C — Reprendre une base existante dans un autre dossier (ou sur une autre machine)

Cas typique : vous avez une nouvelle copie de l'application (autre dossier, autre ordinateur) et vous voulez y reprendre la base et les fichiers uploadés de l'installation en service.

> ⚠️ **Piège** : Baluchon enregistre, pour chaque fichier uploadé, son **chemin complet** sur le disque (ex : `/Users/vous/ancien-dossier/uploads/projet_3/liens/rapport.pdf`). Après une copie ailleurs, ces chemins pointent vers l'ancien emplacement : les fichiers donnent une erreur « introuvable » ou « interdit ». Le script `reparer_chemins_uploads.py` les corrige.

1. **Arrêtez l'ancienne installation** (ou au moins n'y écrivez plus) pendant la copie : copier une base SQLite pendant qu'elle est utilisée peut donner un fichier incohérent.
2. **Dans la nouvelle copie**, retirez les données de test éventuelles : `rm -f baluchon.db` et `rm -rf uploads/*` (en gardant le dossier `uploads/`).
3. **Copiez la base et les fichiers** depuis l'ancienne installation (adaptez les chemins ; l'emplacement exact de la base est indiqué par `DATABASE_URI` dans le `.env` de l'ancienne installation) :
   ```bash
   cp /ancien/dossier/baluchon.db ./baluchon.db
   cp -R /ancien/dossier/uploads/. ./uploads/
   cp baluchon.db baluchon.db.avant-migration      # sauvegarde de la copie
   ```
   L'ancienne installation reste intacte : vous n'avez fait que lire dedans.
4. **Préparez l'environnement** si ce n'est pas déjà fait (voir `GUIDE_INSTALLATION.md`), sans écraser votre base : `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, puis un fichier `.env` contenant `DATABASE_URI=sqlite:///baluchon.db` et une `SECRET_KEY` (générée par `./install.sh`, ou à créer avec `python3 -c "import secrets; print(secrets.token_hex(32))"`). Vos identifiants de connexion sont dans la base : ils fonctionnent tels quels.
5. **Réparez les chemins** (simulation d'abord, puis application) :
   ```bash
   source venv/bin/activate
   python reparer_chemins_uploads.py              # simulation : liste ce qui sera corrigé
   python reparer_chemins_uploads.py --appliquer  # écrit les corrections
   ```
   Si des fichiers sont signalés `MANQUANT`, ils n'ont pas été copiés dans `uploads/` : recopiez le dossier `uploads/` complet de l'ancienne installation, puis relancez.
6. **Migrez la base** : `python migrer_base.py` (ou simplement `./start.sh`), puis suivez les vérifications de la section 5 de ce guide. Pensez à comparer les nombres de lignes avec ceux de l'ancienne base.
