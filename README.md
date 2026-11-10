# Vampire Survivordle

Un Wordle sur **Vampire Survivors** : devine l'arme ou le personnage secret à partir des indices révélés à chaque proposition.

## Jouer

- **En ligne / via un serveur** : la page charge `data.csv` et `characters.csv` automatiquement.
- **En local (double-clic sur `index.html`)** : le navigateur bloque le chargement automatique, la page propose alors de sélectionner le fichier CSV à la main. Pour éviter ça : `python3 -m http.server` dans le dossier puis ouvrir http://localhost:8000.

## Règles

Deux catégories : **Armes** et **Personnages**.

| Armes | Indice |
|---|---|
| Nom | 🟩 si c'est la bonne arme |
| Tags | 🟩 tous identiques · 🟧 au moins un en commun · 🟥 aucun |
| Dégâts | 🟩 identiques, sinon ▲ (la réponse fait plus) / ▼ (moins) |
| Source | 🟩 même DLC / jeu de base |

| Personnages | Indice |
|---|---|
| Nom | 🟩 si c'est le bon personnage |
| Arme | arme(s) de départ : 🟩 identiques · 🟧 au moins une en commun · 🟥 aucune |
| Source | 🟩 même DLC / jeu de base |
| Secret | 🟩 même statut (personnage secret ou non) |
| PV max | 🟩 identiques, sinon ▲ / ▼ |
| Stats | stats modifiées au départ : 🟩 identiques · 🟧 au moins une en commun · 🟥 aucune |

- **Défi du jour** : le même pour tout le monde, change à minuit, un par catégorie. La progression et les statistiques sont sauvegardées dans le navigateur.
- **Partie libre** : une arme ou un personnage au hasard, rejouable à volonté.
- Après 6 essais, un **indice** (la description) se débloque.
- Bouton **Partager** : copie une grille d'emojis sans spoiler.

## Données

`characters.csv` — une ligne par personnage, extrait des fiches du [Vampire Survivors Wiki](https://vampire.survivors.wiki/w/Characters) (modèle *Infobox Character*) :

```
Nom,Arme,Source,Secret,Max Health,Bonus,Description
```

`Bonus` liste les stats que le personnage modifie au départ (champ non vide dans l'infobox), `Aucun` sinon.

`data.csv` — une ligne par arme :

```
Nom,Tags,Base Damage,Source,Description
```

Les tags sont séparés par des virgules (entourer le champ de guillemets). Utiliser des tags cohérents : un même concept = un seul mot (ex. `Explosive`, pas `Explosion`/`Explosions`), sinon les indices partiels perdent leur intérêt.
