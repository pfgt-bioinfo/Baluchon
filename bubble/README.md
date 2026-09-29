# baluchon-bubble

Lancer Baluchon sur un nœud de calcul du cluster (gnomic) et l'utiliser dans son navigateur, comme en local.

Inspiré de [`pfgt-bubble-cli`](https://gitlab.com/pfgt/apps/pfgt-bubble-cli) : même principe (job Slurm + image Singularity + tunnel SSH), mais c'est Baluchon qui tourne sur le nœud à la place de RStudio. Il n'y a pas de serveur `pfgt-bubble` côté cluster : le script fait lui-même le `sbatch` via SSH.

```
   votre poste                 frontale du cluster          nœud de calcul
   ┌──────────┐  tunnel SSH   ┌──────────────┐   Slurm    ┌──────────────┐
   │navigateur│ ─────────────▶│    sbatch    │ ──────────▶│   Baluchon   │
   │  :8000   │               │              │            │  Singularity │
   └──────────┘               └──────────────┘            └──────────────┘
```

## Prérequis

- sur votre poste : `ssh`, `jq`, `rsync` (et `xdg-utils` sous Linux pour ouvrir le navigateur)
- une clé SSH configurée pour se connecter au cluster sans mot de passe
- sur le cluster : Slurm et `singularity` ou `apptainer`

## Ce que baluchon-bubble écrit sur le cluster

| Chemin (par défaut) | Contenu |
|---|---|
| `~/baluchon-bubble/app/` | le code de Baluchon, `.env`, `baluchon.db`, `uploads/` |
| `~/baluchon-bubble/app/venv/` | les dépendances Python (Flask, gunicorn…) |
| `~/baluchon-bubble/app/bubble-state/` | le script du job, `session.json`, les logs (`logs/<jobid>.out`) |
| `~/baluchon-bubble/images/python-3.11.sif` | l'image Singularity (Python officiel) |

Tout est rangé dans `~/baluchon-bubble/`, à part de `~/bubbles/` qui est géré par pfgt-bubble pour les projets R. Les chemins sont modifiables dans `~/.config/baluchon-bubble/config`.

## L'image Singularity

L'image est l'image Python officielle (`docker://python:3.11-slim-bookworm`). Singularity peut la récupérer **sans droits root**, contrairement à une image construite à partir d'un fichier `.def`. Les dépendances de Baluchon (`requirements.txt`) sont installées à côté, dans `~/baluchon-bubble/app/venv/`, sur le même principe que `renv` pour les bubbles R : l'image fournit Python et le venv fournit les paquets.

`baluchon-bubble pull-image` se charge de la récupérer : rien à construire ni à copier à la main.

`baluchon.def` décrit une image complète (Python + dépendances), qu'on pourra utiliser si quelqu'un qui a les droits (root ou fakeroot) la construit un jour :

```bash
sudo singularity build baluchon.sif bubble/baluchon.def   # depuis la racine du repo
```

## 1. Installer le client

```bash
chmod +x bubble/baluchon-bubble
cp bubble/baluchon-bubble ~/.local/bin/    # optionnel
```

## 2. Première utilisation

```bash
baluchon-bubble configure   # hôte, identifiant, port local, chemins sur le cluster
baluchon-bubble pull-image  # récupère l'image Python sur le cluster (quelques minutes)
baluchon-bubble deploy      # copie le code sur le cluster (rsync)
baluchon-bubble init        # installe les dépendances, crée .env, la base et le compte
```

`pull-image`, `deploy` et `init` s'exécutent sur la frontale, qui a accès à internet (Docker Hub, PyPI). Les nœuds de calcul n'ont pas internet.

`deploy` n'utilise jamais `--delete` et ne copie ni `.env`, ni `*.db`, ni `uploads/` : les données déjà présentes sur le cluster ne sont jamais écrasées. Relancez `deploy` après chaque mise à jour du code, puis redémarrez la session. Si `requirements.txt` a changé, lancez aussi `baluchon-bubble deps`.

## 3. Au quotidien

```bash
baluchon-bubble start                          # 2 CPU, 4G, 10h par défaut
baluchon-bubble start --cpus 2 --mem 4G --time 12:00:00 --partition NAME

# Ctrl+C dans le terminal ferme la session et annule le job, ou depuis ailleurs :
baluchon-bubble stop

baluchon-bubble status      # session en cours
baluchon-bubble attach      # rouvrir le tunnel et le navigateur (autre terminal, autre poste)
baluchon-bubble logs        # fin du log du dernier job
```

Le navigateur s'ouvre sur `http://localhost:8000`. Connectez-vous avec le compte créé par `init`.

## Limites connues

- **Une seule session à la fois** (job Slurm `baluchon-bubble`).
- **SQLite sur NFS** : gunicorn tourne avec un seul worker (et plusieurs threads) pour éviter les problèmes de verrou. N'ouvrez pas Baluchon en même temps depuis une autre installation qui utiliserait la même base.
- **Boutons « Ouvrir le projet / le dossier »** : ils appellent `open` sur la machine qui fait tourner Baluchon, ici le nœud de calcul, où ça ne peut pas fonctionner.
- Gunicorn écoute sur `0.0.0.0` du nœud, pour que le tunnel puisse l'atteindre : Baluchon est joignable depuis le réseau interne du cluster pendant la session, protégé par sa page de connexion.
