# Guide des fonctionnalités de Baluchon

Ce guide explique comment utiliser Baluchon au quotidien, une fois l'application installée et lancée. Pour l'installation, voir `GUIDE_INSTALLATION.md`.

---

## Connexion

Baluchon est protégé par un identifiant et un mot de passe (créés à l'installation). À l'ouverture, vous arrivez sur la page de connexion. Une fois connecté·e, vous le restez jusqu'à la déconnexion (icône en haut à droite).

---

## La page d'accueil

C'est votre tableau de bord. Elle réunit en un coup d'œil :

- **Compteurs cliquables** : projets en cours, projets en attente, tâches ouvertes, événements à venir. Chaque compteur mène à la liste correspondante.
- **Projets en cours** : les projets actifs les plus récents.
- **Tâches ouvertes** : vos tâches non terminées, avec leur statut en couleur et leur échéance.
- **Prochains événements** : ce qui arrive, affichable en liste ou en **vue calendrier** (bouton en haut du bloc).

Le menu en haut donne accès à tout moment aux grandes sections : Projets, Événements, Tâches, Infos, Stats.

---

## Les projets

### Créer et organiser
Un projet a un **nom**, une **description**, des **tags** (optionnels), un **chemin** vers un fichier main, c'est-à-dire le fichier principal du projet (optionnel), et un **statut** :
- **En cours** — projet actif
- **En attente** — mis en pause
- **Archivé** — terminé
- **Abandonné** — arrêté

Le statut se change depuis la page « Éditer le projet ».

### Les tags
Les tags servent à classer les projets par thème ou par méthode (par exemple « single cell », « RNA-seq », « métagénomique »). Dans le formulaire du projet, saisissez-les **séparés par des virgules** ; les tags déjà utilisés ailleurs sont proposés en dessous, un clic les ajoute. Un tag peut contenir des espaces (« single cell »). Les majuscules et minuscules ne font pas de différence : « Single cell » et « single cell » sont le même tag. Maximum 20 tags par projet et 40 caractères par tag.

Les tags apparaissent sous la description du projet et dans la liste des projets. Cliquer sur un tag (sur le projet) ou le choisir dans la ligne **Tag** de la liste des projets n'affiche que les projets qui le portent ; le filtre se combine avec celui du statut. Dans les **Statistiques**, la colonne optionnelle « Tags » (bouton Colonnes) les ajoute au tableau et à l'export CSV.

### La page d'un projet (tableau de bord)
Elle rassemble tout ce qui concerne ce projet :

- **Infos** : raccourcis épinglés vers ce qui est utile (dossier, fichier local, fichier uploadé, lien web ou personne), chacun avec un intitulé et un commentaire, et coloré selon son type. Le fichier principal du projet (« fichier main ») s'ouvre directement depuis ici.
- **Avancement** : deux barres de progression — les **tâches** réalisées / restantes, et le **temps** passé / restant (voir « Estimer le temps » plus bas).
- **Tâches en cours** : avec ajout rapide (description + date butoir), la durée estimée de chaque tâche et un lien (icône chronomètre) vers « Estimer le temps ».
- **Aujourd'hui et à venir** : les événements du jour et futurs.
- **Fichiers uploadés** : accès à tous les fichiers importés pour ce projet.

### La liste de tous les projets
Triés du plus récent au plus ancien, filtrables par statut, paginés (10 par page). Chaque projet affiche son statut, sa date de création, son nombre d'événements à venir et de tâches ouvertes.

---

## Les infos

Les « infos » centralisent tout ce qui est utile à un projet sans encombrer. Chaque info a un **type**, reconnaissable à sa **couleur** :

| Type | Couleur | À renseigner |
|---|---|---|
| **Dossier** (local) | 🟢 vert | intitulé (ex : données brutes), chemin du dossier |
| **Fichier local** | 🟢 vert | intitulé (ex : rapport), chemin du fichier sur votre disque |
| **Fichier uploadé** | 🔵 bleu | intitulé, fichier à importer dans Baluchon (jusqu'à 16 Mo) |
| **Lien web** | 🟠 orange | intitulé (ex : lien Github), URL |
| **Personne** | 🟣 violet | **nom et prénom** (intitulé), **email**, **rôle** (dans le champ commentaire) |

Les textes d'exemple du formulaire « Ajouter une info » s'adaptent au type choisi. Le « fichier main » du projet est lui aussi vert, comme les autres éléments locaux.

Chaque ajout ou suppression d'info crée automatiquement un **événement** de type « information » qui en garde la trace.

### Ce qu'on peut faire d'une info
- **Fichier uploadé** : l'icône **œil** l'affiche directement dans le navigateur, l'icône flèche le télécharge.
- **Personne** : l'icône enveloppe ouvre votre messagerie pour écrire à la personne.
- **Dossier / fichier local** : les icônes d'ouverture lancent le dossier ou le fichier sur votre ordinateur. Cela ne fonctionne que si Baluchon tourne **directement sur votre machine** (et non dans un conteneur ou sur un serveur distant) ; dans le cas contraire, un message d'erreur s'affiche.

### Épingler / désépingler
Les infos épinglées apparaissent sur le tableau de bord du projet. Pour éviter d'en avoir trop sous les yeux, vous pouvez **désépingler** une info (elle reste accessible, mais disparaît du tableau de bord).

### La page « Toutes les infos » d'un projet
Accessible depuis le projet, elle liste toutes les infos (épinglées ou non), y compris le fichier main, sous forme de tableau. Des boutons permettent de **filtrer par type** (avec le nombre d'infos de chaque type). Vous pouvez :
- **vérifier** si un lien est encore fonctionnel (bouton par ligne, ou « Vérifier tous les liens ») — une pastille verte ou rouge indique l'état ; pour une personne, on vérifie que l'adresse email est valide,
- **éditer** l'intitulé, le commentaire (ou le rôle) ou la valeur,
- épingler/désépingler, ou supprimer.

### La page « Infos » du menu
L'entrée **Infos** du menu en haut réunit les infos de **tous les projets**. Elle se filtre par projet et par type, et se parcourt par pages de 20. C'est l'endroit pour retrouver, par exemple, tous les fichiers uploadés (filtre « Fichier uploadé ») ou toutes les personnes (filtre « Personne »).

---

## Les événements

Un événement représente quelque chose qui s'est passé ou qui va se passer sur un projet : une note, une communication, une réunion, un envoi, etc. Il a une **date**, un **type**, un **contenu**, et peut porter des **fichiers** et des **tâches**.

### Consulter
- **Par projet** : la page événements d'un projet, filtrable par type, par période (passés / à venir) et par dates.
- **Tous les événements** : la vue globale, tous projets confondus.
- **Vue calendrier** : sur ces pages comme sur l'accueil, basculez en calendrier mensuel ; les jours avec événements sont marqués d'un point, cliquez sur un jour pour voir le détail.

Les événements à venir et passés sont séparés visuellement.

### Créer
Depuis un projet, ou depuis la vue globale (en choisissant le projet concerné). À la création, vous pouvez déjà associer des tâches, puis ajouter des fichiers.

---

## Les tâches

Une tâche a une **description**, un **statut**, une **priorité**, une **date butoir**, une **durée estimée** et des **tags** (ces trois derniers sont optionnels).

### Statuts (modifiables d'un clic, en couleur)
À faire · En cours · En attente · Terminé · **Abandonné**

Une tâche **abandonnée** (qu'on ne fera finalement pas) est « close » comme une tâche terminée : elle n'apparaît plus dans la matrice, dans les « tâches en cours » du tableau de bord ni dans le compteur de tâches ouvertes de l'accueil, et elle **sort de l'avancement** (ni réalisée, ni restante, et sa durée n'est pas comptée dans le temps). Elle reste consultable dans la liste des tâches (filtre « Abandonné ») et peut être remise en cours à tout moment. Dans la vue « Estimer temps », elle apparaît grisée, « hors total ».

### Priorités — la matrice d'Eisenhower
Chaque tâche reçoit une priorité :
- **Urgent & important**
- **Important**
- **Urgent**
- **À planifier**

Dans la **matrice**, la priorité se change directement sur la carte de la tâche pour la déplacer d'un quadrant à l'autre. Dans la **liste**, la priorité et la durée sont simplement affichées : pour les modifier, cliquez sur le petit **crayon** de la tâche (le statut, lui, se change toujours d'un clic).

### Indicateur d'échéance
Indépendamment de la priorité, une tâche dont la date butoir approche (≤ 2 jours) ou est dépassée est signalée par un liseré et une pastille « Bientôt » ou « Dépassée ».

### Les tags des tâches
Comme les projets, les tâches peuvent porter des **tags** (par exemple « QC », « alignement », « single cell ») : séparés par des virgules, sans différence de majuscules, 20 au maximum par tâche. On les saisit à la création rapide d'une tâche (champ « Tags ») ou dans le formulaire du crayon (avec les tags déjà utilisés en suggestions cliquables).

Ils s'affichent à côté de la description dans la liste, la matrice et les « tâches en cours » du tableau de bord. Cliquer sur un tag affiche toutes les tâches qui le portent, tous projets confondus. Dans la **liste** des tâches, le menu **Tag** filtre ; il se combine avec les filtres de statut, de dates et de priorité, et reste actif en changeant de page. La **matrice** propose aussi une rangée de tags pour ne garder qu'une thématique.

### Estimer le temps
Chaque tâche peut recevoir une **durée estimée**, en **jours** et en **% de jour** (par exemple 2 jours et 50 % = 2,5 jours). Elle s'affiche sous la forme d'un petit badge chronomètre (« 2 j 50 % ») dans la liste, la matrice et sur le tableau de bord du projet.

Pour saisir ou modifier une durée :
- **tâche par tâche** : via le crayon d'édition de la tâche (champ « Durée estimée »),
- **toutes d'un coup** : la vue **Estimer temps** (bouton à côté de « Vue matrice », ou icône chronomètre sur le tableau de bord du projet). Elle liste les tâches avec, en face de chacune, deux champs *Jours* et *% de jour*, un total par ligne et un total général qui se met à jour pendant la saisie. Un seul bouton enregistre toute la page. Par défaut elle montre toutes les tâches, terminées comprises ; un bouton permet de ne garder que les tâches non terminées.

Laisser les deux champs vides efface l'estimation. Le champ « % de jour » accepte de 0 à 99.

### Avancement d'un projet
Sur le tableau de bord d'un projet, le bloc **Avancement** montre deux barres :
- **Tâches** : réalisées (statut « Terminé ») / restantes ;
- **Temps** : *passé* / *restant*. Attention : Baluchon ne mesure pas le temps réellement travaillé. Le **temps passé** est la somme des durées estimées des tâches terminées, le **temps restant** celle des tâches non terminées. Les tâches sans estimation ne comptent pas dans le temps (leur nombre est indiqué sous la barre).

### Les vues
- **Liste** : par projet ou globale, avec filtres (statut, priorité, dates) et ajout rapide.
- **Estimer temps** : voir ci-dessus.
- **Matrice** : les tâches réparties dans les 4 quadrants d'Eisenhower, pour les classer visuellement. On peut changer la priorité d'une tâche directement dans la matrice pour la déplacer d'un quadrant à l'autre.

---

## Les fichiers

Les fichiers importés sont des infos de type **Fichier uploadé** (ou des pièces jointes d'événements). Ils sont consultables :
- **Par projet** : le bloc « Fichiers uploadés » du tableau de bord mène à la liste des fichiers du projet.
- **Globalement** : la page **Infos** du menu, filtrée sur « Fichier uploadé ». (L'ancienne entrée « Fichiers » du menu a été remplacée par « Infos » ; l'ancienne adresse redirige vers cette page filtrée.)

Dans toutes ces listes, l'icône **œil** affiche le fichier dans le navigateur, et l'icône de téléchargement l'enregistre.

Formats acceptés : txt, pdf, html, images (png, jpg, gif), doc(x), xls(x), csv, r, rmd, rdata, rds — jusqu'à 16 Mo. Au-delà, mieux vaut référencer le fichier par un lien plutôt que de l'importer.

---

## Les statistiques

La page Stats est un **bilan d'activité sur une période** (par défaut, du 1ᵉʳ janvier de l'année en cours à aujourd'hui — dates ajustables).

- **Compteurs** : projets actifs sur la période, en cours actuellement, terminés, et nombre d'événements.
- **Diagramme de Gantt** : chaque projet est une barre allant de sa création à aujourd'hui (s'il est actif) ou à sa dernière activité (s'il est archivé/abandonné). Des repères marquent les événements (bleu) et les créations de tâches (marron), et le nom des mois sert d'échelle.
- **Avancement des projets** : pour l'ensemble des projets de la période, puis pour chacun, les deux barres *tâches* (réalisées / restantes) et *temps* (passé / restant). C'est l'état **actuel** des tâches, quelle que soit la période ; les tâches sans estimation sont signalées et ne comptent pas dans le temps.
- **Tableau récapitulatif** : pour chaque projet de la période — son état (nouveau, toujours en cours, terminé, abandonné), sa durée d'activité, son nombre d'événements et de tâches créées, ainsi que son **% de tâches réalisées** et son **% de temps passé**, trié du plus actif au moins actif.

### Choisir les colonnes du tableau
Le bouton **Colonnes** (au-dessus du tableau) permet de cocher les statistiques à afficher. Aux colonnes par défaut s'ajoutent des colonnes optionnelles : tâches réalisées, tâches restantes, temps passé, temps restant, temps estimé total. « Rétablir par défaut » remet la sélection d'origine. Votre choix est **mémorisé dans votre navigateur** (il est propre à chaque navigateur et n'est pas enregistré dans la base).

### Exporter le tableau
Le bouton **Exporter CSV** télécharge le tableau pour la période affichée, avec **les colonnes cochées**. Le fichier s'ouvre dans Excel ou LibreOffice (séparateur point-virgule, accents et virgules décimales compatibles avec la version française).

C'est l'outil adapté pour préparer un bilan d'activité (par ex. un entretien annuel) : savoir sur quoi vous avez travaillé, ce qui a démarré, ce qui s'est terminé.

---

## Sauvegarder vos données

Vos données vivent dans deux endroits du dossier de l'application :
- `baluchon.db` (projets, événements, tâches, infos)
- `uploads/` (fichiers importés)

Copiez-les régulièrement ailleurs pour les sauvegarder (voir la section correspondante du guide d'installation), et **toujours avant une mise à jour**.

---

Bonne utilisation ! 🎒
