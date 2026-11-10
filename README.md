# Vampire Survivordle

Un Wordle sur **Vampire Survivors** : devine l'arme, le personnage ou l'évolution secrète à partir des indices révélés à chaque proposition.

## Jouer

- **En ligne / via un serveur** : la page charge les fichiers CSV automatiquement.
- **En local (double-clic sur `index.html`)** : le navigateur bloque le chargement automatique, la page propose alors de sélectionner le fichier CSV à la main. Pour éviter ça : `python3 -m http.server` dans le dossier puis ouvrir http://localhost:8000.

## Catégories

Chaque proposition affiche son nom puis une case par caractéristique : 🟩 correct · 🟧 au moins un élément en commun (les éléments communs sont soulignés) · 🟥 faux. Pour les nombres et les dates, ▲ = la réponse est plus haute / plus récente, ▼ = plus basse / plus ancienne.

| Catégorie | Colonnes |
|---|---|
| **Armes** | Tags · Objet d'évolution · Dégâts de base · Année de sortie · Source |
| **Personnages** | Arme de départ · Source · Secret · PV max · Stats modifiées (abrégées) · Date de sortie |
| **Évolutions** | L'objet requis est donné. Type (évolution / union) · Armes de base · Source |
| **Descriptions** | La description du jeu est donnée. Type (arme / personnage) · Source · Année de sortie |

## Règles

- **Défi du jour** : le même pour tout le monde, un par catégorie, renouvelé à minuit. Il exclut les éléments obscurs (armes « sélecteurs », personnages secrets, unions). La progression et les statistiques sont sauvegardées dans le navigateur.
- **Bonus croisé** : trouver l'arme du jour révèle la source du personnage du jour, et inversement.
- **Partie libre** : au hasard, rejouable à volonté. Le **mode difficile** inclut aussi les éléments exclus du défi du jour.
- **Indices progressifs** : un indice se débloque après 3, 5 puis 7 essais (première lettre, description ou forme du nom, puis évolution / condition de déblocage / arme de base). Ils sont comptés dans le partage (💡).
- **Partager** : copie une grille d'emojis sans spoiler.

## Données

Extraites du [Vampire Survivors Wiki](https://vampire.survivors.wiki/) (infobox des fiches et historique des mises à jour).

| Fichier | Colonnes |
|---|---|
| `data.csv` | `Nom,Tags,Evolution Item,Base Damage,Release,Source,Evolution,Description` |
| `characters.csv` | `Nom,Arme,Source,Secret,Max Health,Bonus,Release,Description,Unlock` |
| `evolutions.csv` | `Nom,Type,Armes,Objets,Source` |

- Les listes (tags, armes, objets, stats) sont séparées par des virgules, champ entre guillemets.
- `Release` : année pour les armes, date `AAAA-MM-JJ` pour les personnages. L'année d'une arme vient de son historique sur le wiki ; à défaut, de la sortie du personnage qui la porte au départ, puis de son DLC.
- `Bonus` liste les stats qu'un personnage modifie au départ, `Aucun` sinon.
- Garder des tags cohérents : un même concept = un seul mot (ex. `Explosive`, pas `Explosion`/`Explosions`), sinon les indices partiels perdent leur intérêt.
