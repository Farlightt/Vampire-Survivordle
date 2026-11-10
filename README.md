# Vampire Survivordle

Un Wordle sur **Vampire Survivors** : devine l'arme, le personnage ou l'évolution secrète à partir des indices révélés à chaque proposition.

## Jouer

- **En ligne / via un serveur** : la page charge les fichiers CSV automatiquement.
- **En local (double-clic sur `index.html`)** : le navigateur bloque le chargement automatique, la page propose alors de sélectionner le fichier CSV à la main. Pour éviter ça : `python3 -m http.server` dans le dossier puis ouvrir http://localhost:8000.

## Catégories

Chaque proposition affiche son nom puis une case par caractéristique : 🟩 correct · 🟧 au moins un élément en commun (les éléments communs sont soulignés) · 🟥 faux. Pour les nombres et les dates, ▲ = la réponse est plus haute / plus récente, ▼ = plus basse / plus ancienne.

| Catégorie | Colonnes |
|---|---|
| **Armes** | Tags · Couleurs de l'icône · Objet d'évolution · Dégâts de base · Moment de déblocage (tôt / milieu / tard) · Source |
| **Personnages** | Arme de départ (🟧 si un tag d'arme en commun) · Source · Type de déblocage · PV max · Stats modifiées (abrégées) · Date de sortie |
| **Évolutions** | L'objet requis est donné. Armes de base · Tags de l'arme de base · Année de sortie · Source |
| **Descriptions** | La description du jeu est donnée. Type (arme / personnage) · Tags de l'arme · Source · Année de sortie |

## Règles

- **Défi du jour** : le même pour tout le monde, un par catégorie, renouvelé à minuit **heure de Paris** (quel que soit le fuseau du joueur). Les réponses sont fixées à l'avance dans `daily.json`. Il exclut les éléments obscurs (armes « sélecteurs », personnages secrets, unions). La progression et les statistiques sont sauvegardées dans le navigateur.
- **Bonus croisé** : trouver l'arme du jour révèle la source du personnage du jour, et inversement.
- **Partie libre** : au hasard, rejouable à volonté. Le **mode difficile** inclut aussi les éléments exclus du défi du jour.
- **Indices progressifs** : un indice se débloque après 3, 5 puis 7 essais (première lettre, description ou forme du nom, puis évolution / condition de déblocage / arme de base). Ils sont comptés dans le partage (💡).
- **Réponses indiscernables** : une proposition qui a exactement les mêmes caractéristiques que la réponse (ex. Peachone et Ebony Wings) compte comme gagnante.
- **Archives** : rejouer les défis des 30 derniers jours (✓ / ✗ selon le résultat).
- **Options** : mode difficile, essais limités à 8, liste des réponses encore compatibles avec les indices, **mode daltonien** (bleu / orange / gris + symboles ✓ ~ ✗), **transfert de progression** entre appareils (code à copier-coller, pas de serveur).
- **Partager** : copie une grille d'emojis sans spoiler, ou la publie sur X.
- **Langues** : français, anglais, espagnol (menu en haut à gauche ; langue du navigateur par défaut).
- **Habillage** : icônes des armes et des objets, flèches dessinées, effets sonores (option, coupés par défaut), confettis à la victoire.

## Données

Extraites du [Vampire Survivors Wiki](https://vampire.survivors.wiki/) (infobox des fiches et historique des mises à jour).

| Fichier | Colonnes |
|---|---|
| `data.csv` | `Nom,Tags,Colors,Evolution Item,Base Damage,Max Level,Unlock Time,Release,Source,Evolution,Description` |
| `characters.csv` | `Nom,Arme,Source,Secret,Max Health,Bonus,Release,Description,Unlock,Unlock Type,Weapon Tags` |
| `evolutions.csv` | `Nom,Type,Armes,Objets,Source,Base Tags,Release` |

- Les listes (tags, armes, objets, stats) sont séparées par des virgules, champ entre guillemets.
- `Release` : année pour les armes, date `AAAA-MM-JJ` pour les personnages. L'année d'une arme vient de son historique sur le wiki ; à défaut, de la sortie du personnage qui la porte au départ, puis de son DLC.
- `Bonus` liste les stats qu'un personnage modifie au départ, `Aucun` sinon.
- `Unlock Type` est déduit du texte de déblocage (cercueil, évolution, ennemis vaincus, survie 20 min, boss, exploit, énigme…).
- `Weapon Tags` / `Base Tags` : tags des armes de base (via `data.csv`, en remontant les évolutions) ; `Release` des évolutions = année de leur arme de base la plus récente.
- Les tags des 30 armes ajoutées depuis le wiki (Bloodmoon, Ante Chamber, thons…) ont été rédigés d'après leur description en jeu.
- `Colors`, `Unlock Time` (Early / Mid / Late) et `Max Level` viennent de la version locale du projet ; pour les 30 armes ajoutées depuis, couleurs et moment de déblocage ont été estimés d'après leur icône et leur condition de déblocage sur le wiki.
- Garder des tags cohérents : un même concept = un seul mot (ex. `Explosive`, pas `Explosion`/`Explosions`), sinon les indices partiels perdent leur intérêt.

## Mettre à jour les données

Quand le jeu sort du nouveau contenu :

```
python3 tools/update_data.py      # télécharge le wiki, ajoute les nouveautés, recalcule les colonnes déduites
python3 tools/build_calendar.py   # prolonge le calendrier des défis sans toucher aux dates déjà prévues
```

- Les armes et personnages existants gardent leurs champs rédigés à la main ; les écarts avec le wiki sont listés (`--overwrite` pour les remplacer).
- Les nouvelles armes arrivent avec le tag `À compléter` : remplir leur colonne `Tags` puis lancer `python3 tools/update_data.py --derive`.
- `--dry-run` affiche le rapport sans rien écrire. Tests : `python3 tools/test_update_data.py`.
- Relancer `build_calendar.py` au moins une fois par an (le calendrier couvre deux ans).

## Icônes et traductions

- `images/weapons/`, `images/items/`, `images/characters/` : icônes nommées d'après le nom en minuscules (`guardian_s_targe.webp`), listées dans `images/icons.json`. Un nom sans icône affiche une pastille avec son initiale.
- `python3 tools/fetch_icons.py` télécharge depuis le wiki les icônes manquantes (armes récentes, objets, portraits de personnages) et met à jour `images/icons.json`. Avec Pillow installé, elles sont converties en WebP.
- `lang/fr.js`, `lang/en.js`, `lang/es.js` : tous les textes de l'interface. Ajouter une langue = copier un fichier, traduire les valeurs, l'ajouter au menu dans `index.html`.
