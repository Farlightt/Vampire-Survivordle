# Vampire Survivordle

Un Wordle sur les armes de **Vampire Survivors** : devine l'arme secrète à partir des indices révélés à chaque proposition.

## Jouer

- **En ligne / via un serveur** : la page charge `data.csv` automatiquement.
- **En local (double-clic sur `index.html`)** : le navigateur bloque le chargement automatique, la page propose alors de sélectionner `data.csv` à la main. Pour éviter ça : `python3 -m http.server` dans le dossier puis ouvrir http://localhost:8000.

## Règles

| Colonne | Indice |
|---|---|
| Nom | 🟩 si c'est la bonne arme |
| Tags | 🟩 tous identiques · 🟧 au moins un en commun · 🟥 aucun |
| Dégâts | 🟩 identiques, sinon ▲ (l'arme secrète fait plus) / ▼ (moins) |
| Source | 🟩 même DLC / jeu de base |

- **Arme du jour** : la même pour tout le monde, change à minuit. La progression est sauvegardée dans le navigateur.
- **Partie libre** : une arme au hasard, rejouable à volonté.
- Après 6 essais, un **indice** (la description de l'arme) se débloque.
- Bouton **Partager** : copie une grille d'emojis sans spoiler.

## Données

`data.csv` — une ligne par arme :

```
Nom,Tags,Base Damage,Source,Description
```

Les tags sont séparés par des virgules (entourer le champ de guillemets). Utiliser des tags cohérents : un même concept = un seul mot (ex. `Explosive`, pas `Explosion`/`Explosions`), sinon les indices partiels perdent leur intérêt.
