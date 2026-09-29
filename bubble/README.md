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
| `~/bubbles/baluchon/` | le code de Baluchon, `.env`, `baluchon.db`, `uploads/` |
| `~/bubbles/baluchon/bubble-state/` | le script du job, `session.json`, les logs (`logs/<jobid>.out`) |
| `~/bubbles/images/baluchon.sif` | l'image Singularity (à copier vous-même, voir plus bas) |

Les deux chemins sont modifiables dans `~/.config/baluchon-bubble/config`.

## 1. Construire l'image Singularity

L'image contient seulement Python et les dépendances de `requirements.txt`. Le code n'y est pas : il reste dans `~/bubbles/baluchon/` et se met à jour avec `deploy`. Il ne faut donc reconstruire l'image que si `requirements.txt` change.

Depuis la racine du repo Baluchon, sur une machine où Singularity/Apptainer est installé :

```bash
sudo singularity build baluchon.sif bubble/baluchon.def
# ou, sans sudo, si le fakeroot est autorisé (par ex. sur la frontale) :
apptainer build --fakeroot baluchon.sif bubble/baluchon.def
```

Puis copiez-la sur le cluster :

```bash
ssh <user>@<cluster> 'mkdir -p ~/bubbles/images'
scp baluchon.sif <user>@<cluster>:~/bubbles/images/
```

Les fichiers `*.sif` sont ignorés par git.

## 2. Installer le client

```bash
chmod +x bubble/baluchon-bubble
cp bubble/baluchon-bubble ~/.local/bin/    # optionnel
```

## 3. Première utilisation

```bash
baluchon-bubble configure   # hôte, identifiant, port local, chemins sur le cluster
baluchon-bubble deploy      # copie le code sur le cluster (rsync)
baluchon-bubble init        # crée .env, la base et le compte de connexion
```

`deploy` n'utilise jamais `--delete` et ne copie ni `.env`, ni `*.db`, ni `uploads/` : les données déjà présentes sur le cluster ne sont jamais écrasées. Relancez `deploy` après chaque mise à jour du code, puis redémarrez la session.

## 4. Au quotidien

```bash
baluchon-bubble start                          # 2 CPU, 4G, 8h par défaut
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
